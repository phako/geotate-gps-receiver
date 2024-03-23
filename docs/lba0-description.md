# LBA 0

Since the device identifies itself as a disk, it tries to behave like one if
accidentally plugged into a computer while booting.

Thus it contains a rudimentary MBR. The bootsector code is very generic, it
checks for a valid partition table and then goes on to try to boot. 

The device does not come with a valid partiton table, so it will just print
"Invalid partition table" and wait infinitely.

A disassembly can be found in (lba0-disassembly.txt)