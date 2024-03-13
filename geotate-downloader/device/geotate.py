import gi

from gi.repository import GLib, Gio, GObject

import abc
import datetime as dt
from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils import init_device
import struct
import time
import typing 
import uuid
from . import util

from pyscsi.pyscsi.scsi_device import SCSIDevice

class Backend:
    def read(self, lba: int) -> type[bytearray]:
        raise NotImplementedError
    
    def write(self, lba:int, data: typing.ByteString, wait_for_completion:bool = True) -> bool:
        raise NotImplementedError


class SCSIBackend(Backend):
    def __init__(self, devpath: str, path: str):
        super().__init__()
        self.devpath = devpath
        self.path = "/dev/" + path

        # Manually creating the SCSI device to be able to disable buffering
        # necessary for readwrite = True
        device = SCSIDevice(self.path, readwrite=True, buffering = 0)
        self.scsi_device = SCSI(device, blocksize=512)

    def read(self, lba:int) -> type[bytearray]:
        return self.scsi_device.read10(lba, 1).datain
    
    def write(self, lba:int, data: typing.ByteString, wait_for_completion:bool = True) -> bool:
        self.scsi_device.write10(lba, 1, data)
        if wait_for_completion:
            return self._wait_for_complete()
        return True
    
    def _wait_for_complete(self):
        r = self.read(GeotateDevice.STATUS)
        if r[0] == 0:
            return True
        
        for i in range(0, 150):
            time.sleep(0.05)
            r = self.read(GeotateDevice.STATUS)
            if r[0] == 0:
                return True
        
        return r[0] == 0
    
    def __str__(self):
        return f"Geotate device backend {self.devpath} {self.path}"


class FileBackend(Backend):
    def __init__(self, lba_folder: str):
        self.lba_folder = lba_folder

    def read(self, lba:int) -> type[bytearray]:
        path = f"{self.lba_folder}/lba_{lba}.bin"
        print(f"Reading from {path}")
        with open(path, "rb") as f:
            return f.read()
        
    def write(self, lba: int, data: typing.ByteString, wait_for_completion: bool = True) -> bool:
        return True

    def __str__(self):
        return f"Geotate file backend feeding from {self.lba_folder}"


class _CaptureCapabilities:
    INTERVAL_SETABLE = 0
    QUALITY_SETABLE = 1
    ONE_SHOT_CAPABLE = 2
    PERIODIC_CAPABLE = 3
    CONTINOUS_CAPABLE = 4
    BATTERY_MULTILEVEL = 5
    CAPTURE_DELAY_SETABLE = 6
    NO_MOTION_INTERVAL_AVAILABLE = 7
    CAPTURE_DIVIDER = 8

    def __init__(self, flags: int):
        self.flags = flags
    
    def __getitem__(self, index):
        return (self.flags & (1 << index)) != 0
    
    def __str__(self):
        b = ('no', 'yes')
        return f"Capture interval setable: {b[self[_CaptureCapabilities.INTERVAL_SETABLE]]}\n" \
               f"Capture quality setable: {b[self[_CaptureCapabilities.QUALITY_SETABLE]]}\n" \
               f"Supports one shot capture: {b[self[_CaptureCapabilities.ONE_SHOT_CAPABLE]]}\n" \
               f"Supports periodic capture: {b[self[_CaptureCapabilities.PERIODIC_CAPABLE]]}\n" \
               f"Supports continuos capture: {b[self[_CaptureCapabilities.CONTINOUS_CAPABLE]]}\n" \
               f"Battery supports multiple levels: {b[self[_CaptureCapabilities.BATTERY_MULTILEVEL]]}\n" \
               f"Capture delay is setable: {b[self[_CaptureCapabilities.CAPTURE_DELAY_SETABLE]]}\n" \
               f"No motion interval is available: {b[self[_CaptureCapabilities.NO_MOTION_INTERVAL_AVAILABLE]]}\n" \
               f"Capture divider available: {b[self[_CaptureCapabilities.CAPTURE_DIVIDER]]}"


class CaptureData1:
    def __init__(self, record: typing.ByteString):
                
        record_size = int(record[0])
        #print("==> ", record_size)

        self.binary_size = struct.unpack("<L", record[24:28])[0]
        if self.binary_size == 0:
            self.binary_size = struct.unpack("<H", record[0x1e:0x20])[0] << 9

        f = bytearray(record[4:7])
        f.append(0)
        #print(struct.unpack("<L", f)[0])
        
        self.track_id = int(record[7])
        #print(int(record[2]))
        #print(int(record[3]))

        self.timestamp = util.mktime(record[8:15])
        #print(self._mktime(record[8:15]))

        #print("==d")
        #print(struct.unpack("<L", record[0x14:0x18])[0])
        #print("0x18:" , struct.unpack("<L", record[0x18:0x1c])[0])
        #print(struct.unpack("<H", record[0x1c:0x1e])[0])
        #print(struct.unpack("<H", record[0x1e:0x20])[0])
        self.capture_binary_data_offset = struct.unpack("<L", record[0x14:0x18])[0]
        self.capture_binary_header_size = struct.unpack("<H", record[0x1c:0x1e])[0]

    def __str__(self):
        return f"Capture {self.track_id}, binary offset: {self.capture_binary_data_offset}, binary data size: {self.capture_binary_header_size}, full binary size: {self.capture_binary_header_size + self.binary_size}"


class GeotateDevice(GObject.Object):
    __gtype_name__ = "GeotateDevice"

    DEVICE_INFO = 1
    RTC = 2
    BATTERY_LEVEL = 3
    CAPTURE_CONFIG = 4
    DO_CAPTURE = 6
    CAPTURE_DATA_ENTRY = 7
    STATUS = 8
    DEVICE_ID = 0xb

    COMMAND_GUID = bytes(b'\x0f\x00@\xbe0~QA\x9c\xc6\xf3\x02py\x15\x90')


    def __init__(self, backend: Backend):
        super().__init__()

        self.device_version_string = "Unknown"
        self.device_version = 0
        self.device_id = "Unknown"

        self.capture_cache = []
        self.track_to_capture_count = {}
        self.captures_per_track = dict([(0, 0)])
        self.track_count = 0

        self.backend = backend
        print(self.backend)

        self.get_device_info()
        #self.get_capture_config()

    def get_device_info(self):
        r = self.backend.read(GeotateDevice.DEVICE_INFO)
        self.device_version = struct.unpack(">L", r[0xd0:0xd4])[0]
        self.device_version_string = f"{r[0xd0]}.{r[0xd1]}.{r[0xd2]}.{r[0xd3]}"
        self.nxp_guid = str(uuid.UUID(bytes = bytes(r[0x80:0x90])))
        self.maximum_capture_count = struct.unpack("<L", r[0x9c:0xa0])[0]
        self.binary_capture_base_lba = struct.unpack("<L", r[0xa4:0xa8])
        self.capture_data_base_lba = struct.unpack("<L", r[0xa8:0xac])[0]
        self.capture_capabilites = _CaptureCapabilities(struct.unpack("<L", r[0xcc:0xd0])[0])

    def get_device_id(self):
        r = self.backend.read(GeotateDevice.DEVICE_ID)
        value = struct.unpack("<L", r[2:6])[0]
        self.device_id = "{:02x}-{:02x}-{:08x}".format(r[0], r[1], value)

    def get_battery_level(self):
        r = self.backend.read(GeotateDevice.BATTERY_LEVEL)
        return int(r[0])
    
    def get_capture_config(self):
        r = self.backend.read(GeotateDevice.CAPTURE_CONFIG)
        interval = struct.unpack("<L", r[:4])
        quality = r[4]
        mode = r[5]
        continous = struct.unpack("<L", r[6:10])
        delay = struct.unpack("<H", r[10:12])
        no_motion_interval = struct.unpack("<H", r[12:14])
        print(f"{interval} {quality} {mode} {continous} {delay} {no_motion_interval}")


    def get_rtc(self):
        r = self.backend.read(GeotateDevice.RTC)
        return util.mktime(r[0:7])
    
    def do_capture(self):
        # untested...
        data = bytearray(512 - len(GeotateDevice.COMMAND_GUID))
        data += GeotateDevice.COMMAND_GUID
        if self.device_version >= 0x08030004:
            data[3] = 6
            if self._write(GeotateDevice.STATUS, data):
                return self.backend.read(GeotateDevice.DO_CAPUTRE)[0] == 0
            return False
        else:
            return self.backend.write(GeotateDevice.DO_CAPTURE, data)

    def set_rtc(self):
        now = dt.datetime.now(dt.timezone.utc)
        data = bytearray(512 - len(GeotateDevice.COMMAND_GUID))
        data[0] = now.year - 2000
        data[1] = now.month - 1
        data[2] = now.day
        data[3] = now.hour
        data[4] = now.minute
        data[5] = now.second
        data[6] = int(now.microsecond / 1000 / 10)

        # Append signature
        data += GeotateDevice.COMMAND_GUID
        self.backend.write(GeotateDevice.RTC, data)

    def find_capture_data_start(self):
        r = self.backend.read(GeotateDevice.CAPTURE_DATA_ENTRY)
        tmp = struct.unpack("<L", r[:4])[0]
        record_number = tmp & 0xf
        current_lba = tmp >> 4
        r = self.backend.read(self.capture_data_base_lba + current_lba)
        data_offset = record_number * 4
        local_258 = 0
        while record_number < 0x10:
            header_data = r[data_offset:]
            record_size = int(r[0])
            data_offset = int(r[1])

            # FIXME: Do we need to check for the error cases here as well or does that
            # belong to the capture entry parsing
            record_number += 1

            # FIXME: What is this counted up for
            local_258 += 1

        self.capture_count = 0
        keep_parsing = True
        while keep_parsing:
            current_lba += 1

            # Now start reading capture data. Fixme: Do we ever get up to the
            # header thingy? Maybe if the device has many captures?
            print(f"{current_lba} {local_258}")
            record = self.backend.read(self.capture_data_base_lba + current_lba)
            record_number = 0
            data_offset = 0
            while record_number < 0x10 and len(record) > 0x20:
                record_offset = current_lba * 0x10 + record_number
                #print(f"Record offset : {record_offset}")
                record = record[data_offset:]
                # FIXME: End of data markers...
                if record[0] == 0xff:
                    keep_parsing = False
                    break;
                
                data_offset = int(record[1])
                d = CaptureData1(record[0:0x20])
                d.record_offset = record_offset
                self.capture_cache.append(d)
                print(d)
                record_number += 1
                self.capture_count += 1

        current_capture = 0
        self.track_count = 0
        current_track = -1
        for c in self.capture_cache:
            if c.track_id == 0:
                self.track_to_capture_count[0] = current_capture
                self.captures_per_track[0] += 1
            elif current_track == c.track_id:
                self.captures_per_track[self.track_count] += 1
            else:
                self.track_count += 1
                self.track_to_capture_count[self.track_count] = current_capture
                self.captures_per_track[self.track_count] = 1
                current_track = c.track_id
        if 0 < self.track_count or 0 < self.captures_per_track[0]:
            self.track_count += 1

    def __str__(self):
        return f"Geotate device with backend {self.backend}\n" \
                f"Device version: {self.device_version_string}\n" \
                f"Capture flags:\n {self.capture_capabilites}"
