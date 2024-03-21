# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

from . import GeotateDevice
from . import FileBackend
from . import SCSIBackend

if __name__ == "__main__":
    #d = GeotateDevice(FileBackend("/home/jens/bilora/deviceinfo"))
    d = GeotateDevice(SCSIBackend("", "sg1"))
    r = d.backend.read(2)
    with open("lba_2.bin", "wb") as f:
        f.write(r)
    #d.find_capture_data_start()
    d.get_capture_config()
    d.get_capture(2)
    print(d)

    print(f"Captures: {d.capture_count}")
