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
import urllib, re

def fun_dns_callback(db, shop_name, link, dt):
    page = urllib.urlopen(link).read().replace(" ", "").replace(" ", "")
    for price in re.findall('<metaitemprop=\"price\"content=\"(\d+.\d+)\"', page):
        db.priceAdd(shop_name, link, dt, float(price), "rur")
    return True

def fun_dns_key():
    return "dns"

def fun_dns_comment():
    return "http://www.dns-shop.ru/"

if __name__ == "__main__":
    from pricedog_db import *
    import time, sys
    if len(sys.argv) == 2:
        fun_dns_callback(DB(), fun_dns_key(), sys.argv[1], int(time.time()))
    else:
        print "Usage:"
        print "    pricedog_mod_dns.py <link>"
        sys.exit(-1)
    sys.exit(0)
    