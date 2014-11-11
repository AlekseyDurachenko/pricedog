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
import sys
import datetime

def init(db):
    db.createTables()
    factory = Factory()
    for key in factory.keys():
        if not db.shopExists(key):
            db.shopAdd(key, factory.comment(key))
    sys.exit(0)

def shop_list(db):
    for shop in db.shopList():
        print "* %s (%s)" % (shop['name'], shop['comment'])
    sys.exit(0)

def task_add(db, shop_name, link):
    if not db.shopExists(shop_name):
        print "the shop is not defined"
        sys.exit(-1)
    
    if not db.taskExists(shop_name, link):
        db.taskAdd(shop_name, link)
    else:
        print "the task is already exits"
    sys.exit(0)

def task_remove(db, shop_name, link):
    db.taskRemove(shop_name, link)
    sys.exit(0)
    
def task_list(db):
    for task in db.taskList():
        print "* %s %s (%s)" % (task['shop_name'], task['link'], task['nom'])
    sys.exit(0)

def price_list(db, shop_name, link, lag_in_seconds=0):
    print "[%s] %s" % (shop_name, link)
    print "YYYY-MM-DD HH:MM:SS  MIN_PRICE  MAX_PRICE CURRENCY"
    prev_time = 0
    for price in db.priceList(shop_name, link):
        if price['dt']-prev_time > lag_in_seconds:
            print '{:s} {:10.3f} {:10.3f} {:8s}'.format(
                datetime.datetime.fromtimestamp(int(price['dt'])).strftime('%Y-%m-%d %H:%M:%S'), 
                price['min'], price['max'], price['currency'])
            prev_time = price['dt']
    sys.exit(0)

def price_machine_list(db, shop_name, link, lag_in_seconds=0):
    prev_time = 0
    for price in db.priceList(shop_name, link):
        if price['dt']-prev_time > lag_in_seconds:
            print price['dt'], price['min'], price['max']
            prev_time = price['dt']
    sys.exit(0)


def print_usage():
    print """=== pricedog cotrol v.1.0 ===
Usage:
    pricedog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                       -- init the database
    shop list                  -- show the shop list
    task add <shop> <link>     -- add the new task
    task remove <shop> <link>  -- remove the task
    task list                  -- show the task list 
    price list <shop> <link> [<step_in_days>]  -- show price list
    price_machine list <shop> <link> [<step_in_days>]  -- machine redable pricelist
"""
    sys.exit(-1)

# entry point
if len(sys.argv) > 1:
    # init
    if sys.argv[1] == "init":
        init(DB())
    # shop <command>
    elif sys.argv[1] == "shop" and len(sys.argv) > 2:
        # shop list
        if sys.argv[2] == "list":
            shop_list(DB())
    # task <command>
    elif sys.argv[1] == "task" and len(sys.argv) > 2:
        # task add <shop> <link>
        if sys.argv[2] == "add" and len(sys.argv) == 5:
            task_add(DB(), sys.argv[3], sys.argv[4])
        # task remove <shop> <link>
        elif sys.argv[2] == "remove" and len(sys.argv) == 5:
            task_remove(DB(), sys.argv[3], sys.argv[4])
        # task list
        elif sys.argv[2] == "list":
            task_list(DB())
    # price <command>
    elif sys.argv[1] == "price" and len(sys.argv) > 2:
        # price list <shop> <link>
        if sys.argv[2] == "list" and len(sys.argv) == 5:
            price_list(DB(), sys.argv[3], sys.argv[4])
        # price list <shop> <link>
        if sys.argv[2] == "list" and len(sys.argv) == 6:
            price_list(DB(), sys.argv[3], sys.argv[4], int(sys.argv[5])*24*3600)
    # price_machine <command>
    elif sys.argv[1] == "price_machine" and len(sys.argv) > 2:
        # price_machine list <shop> <link>
        if sys.argv[2] == "list" and len(sys.argv) == 5:
            price_machine_list(DB(), sys.argv[3], sys.argv[4])
        # price_machine list <shop> <link>
        if sys.argv[2] == "list" and len(sys.argv) == 6:
            price_machine_list(DB(), sys.argv[3], sys.argv[4], int(sys.argv[5])*24*3600)
# invalid
print_usage()
