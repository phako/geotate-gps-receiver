# LBA 6

This section can apparently used to trigger a GPS capture through software.
This is untested and only based on information gathered from the orignal
software.

For firmware below 8.3.0.4, a capture seems to be triggered by just writing
to this LBA.

For later firmwares, byte 3 of the data needs to be 6. The capture is then
triggered by writing the data to LBA 8, the status register and checking that
byte 0 of this LBA is 0.

Note: This looks like a bug in the original software: A mix-up of the two LBAs

## Important bytes

|Bytes | Description|
|--- | --- |
| 3 | Set to 6, starting with firmware 8.3.0.4

