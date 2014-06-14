#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright 2014, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pricedog_db import *
from pricedog_factory import *
import time, sys

if __name__ == "__main__":
    db = DB()
    factory = Factory()
    timestamp = int(time.time())
    for row in db.taskList():
        shop_name = row[0]
        link = row[1]
        fun = factory.fun(shop_name)
        fun(db, shop_name, link, timestamp)
    sys.exit(0)
    