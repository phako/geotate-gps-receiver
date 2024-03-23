# Device structure

The device represents itself as an USB mass storage device. All communication
is done through SCSI Read10 and Write10 commands to specific LBAs. Some of which
have a well-known location, some of which are configured on the device and need
to be read before any interaction.

## Overview

The device has roughly three classes of LBAs:

1. Compatibilty LBAs which are there for pretending to be a mass storage device
2. Well-known "control" LBAs which contain specific data on specific numbers
3. "Dynamic" LBAs which contain information about the GPS captures. Their
address can be read from one of the other LBAs, or even chained within a dynamic
LBA

The control LBAs are usually "signed" with a shared secret. The term "signed"
has to be taken literally here, not cryptographically. It is only checked that
the last bytes of a LBA match the well-known device UUID.

Data is usually stored in little endian, with the notable exception of the
device version.

It seems that older versions of the firmware had a bug that caused the bytes of
the captured GPS data to be stored in reverse bit order.

### LBA 0

Generic bootsector. See (lba0-description.md) for details.

### LBA 1

Device information, such as the device version, some UUIDs used for
"verification" that the device is genuine and LBA numbers where to find the
capture information. See (lba1-description.md) for details.

### LBA 2

Used to get and set the on-device real-time clock. See (lba2-description.md)
for details.

### LBA 3

The battery level. See (lba3-description.md) for details.

### LBA 4

Configuration of the capture parameters. See (lba4-description.md) for details.

### LBA 5

Used to erase capture data. Currently no details available.

### LBA 6

Trigger a capture. See (lba6-description.md) for details.

### LBA 7

Entrypoint for querying the currently available captures. See
(lba7-description.md) for details.

### LBA 8

Write operation status. Used by the device to signalize a set operation is
finished. See (lba8-description.md) for details.

### LBA 9

Currently Unknown

### LBA 10

Currently Unknown

### LBA 11

Device id. See (lba11-description.md) for details.

### LBA 12

Used in clearing all capture data from the device. Currently no details
available.

The following offsets are specific for the devices I own, but could in theory
be different for other devices, since they are stored in LBA1

### LBA 2048 (0x800)

Start of the capture information. This again contains pointers to the rest of
the information regarding information about the captures.

### LBA 4096 (0x1000)

Start of the so-called GRE data. This is a binary header that, together with the
capture data forms the contents of the SDF file as produced by the original
downloading tool

### LBA 8192 (0x2000)

Start of the actual binary capture data