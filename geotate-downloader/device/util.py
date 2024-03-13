# SPDX-FileCopyrightText: 2023 Jens Georg <mail@jensge.org>
# SPDX-License-Identifier: GPL-3.0-or-later

import datetime as dt
import typing

def mktime(data: typing.ByteString) -> dt.datetime:
    return dt.datetime(int(data[0]) + 2000, int(data[1]) + 1, int(data[2]), int(data[3]), int(data[4]), int(data[5]),
                       int(data[6]) * 10 * 1000, tzinfo=dt.timezone.utc)
