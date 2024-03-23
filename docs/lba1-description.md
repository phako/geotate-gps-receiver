# LBA 1

The software calls this "Sector Zero data", in reality it contains the
information necessary to download all the other information from the device

The information documented here is just the ones that were needed to download
the capture data on our own.

## Important bytes

|Bytes | Description|
|--- | --- |
|d0-d3 | The device version in big endian notation (e.g. 0x08030004 for 8.3.0.4)
|80-8f | The so-called NXP GUID. Vendor id that the software checks against to make sure its a genuine device
|9c-9f | Maximum number of GPS captures the device can store
|a0-a3 | The first LBA where the raw binary data for captures is stored
|a4-a7 | The first LBA where the binary header data (called GRE by the software) is stored
|a8-ab | The first LBA where meta-information about the captures is stored
|cc-cf | Bitset of capture capabilities


## Capture capabilties bitset

|Bit | Description
|--- | --- 
| 0  | Capture interval can be changed
| 1  | Capture quality can be changed
| 2  | Device can do one-shot captures
| 3  | Device can do periodic captures
| 4  | Device can do continous captures
| 5  | Battery can report multiple levels
| 6  | Capture delay is configurable
| 7  | No-motion interval is configurable
| 8  | Capture divider (whatever that means) can be set

The capability set for the Bilora devices is one-shot captures with configurable
capture delay.