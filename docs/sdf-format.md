# SDF file format

The SDF format is equivalent to the binary header and the capture data.
No processing is done on those components after getting them from the device.

## Important bytes

|Bytes | Description|
|--- | --- |
| 0-3 | Magic 8B8B8B8B
| 4-5 | Header length
| 6-7 | File version
| 8-10 | Capture count
| 11 | Track id
| 22 | Year - 2000
| 23 | Month - 1
| 24 | Day
| 25 | Hour
| 26 | Minutes
| 27 | Seconds
| 32-35 | Firmware version
| 60-123 | Copyright Geotate BV 2008, all rights reserved
| 124-162 | UUID in text form (GRL)
| Header length... | GPS data samples