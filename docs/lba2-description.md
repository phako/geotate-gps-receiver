# LBA 2

This is used to read or set the device's real-time clock

## Important bytes

|Bytes | Description|
|--- | --- |
| 0 | Year, with 0 meaning the year 2000
| 1 | Month, with January being 0
| 2 | Day of Month
| 3 | Hours
| 4 | Minutes
| 5 | Seconds
| 7 | Centiseconds

Setting the RTC works by writing the data accordingly and then waiting for the
first byte of LBA 8 to turn 1