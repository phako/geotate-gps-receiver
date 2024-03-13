# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

from . import GeotateDevice
from . import FileBackend

if __name__ == "__main__":
    d = GeotateDevice(FileBackend("/home/jens/bilora/deviceinfo"))
    d.find_capture_data_start()
    print(d)
