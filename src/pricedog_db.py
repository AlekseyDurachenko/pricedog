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

import sqlite3

class DB:
    """This class used for access the database. The database structure:
	
--------------------------------------------------------------|
| TShop (the shop table)                                      |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| name      | string   | unique         | short unique name   |
| comment   | string   |                | description         |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TTask (the iten in the shop)                                |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| TShopId   | integer  | unique         |                     |
| link      | string   | unique         | link                |
| active    | integer  |                | 0 - inative         |
| comment   | string   |                | description         |
--------------------------------------------------------------|

--------------------------------------------------------------|
| TPrice (the price of the readout)                           |
--------------------------------------------------------------|
| id        | integer  | primary key    |                     |
| TTaskId   | integer  |                |                     |
| dt        | integer  |                | unix timestamp      |
| price     | real     |                |                     |
| currency  | string   |                | (rur,eur,e.t.c.)    |
| comment   | string   |                | description         |
--------------------------------------------------------------|
    """
    __conn = None
    def __init__(self):
        self.__conn = sqlite3.connect('pricedog.db')
    def createTables(self):
        cursor = self.__conn.cursor();
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TShop(
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
                comment TEXT NOT NULL);""");     
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TTask(
                id INTEGER PRIMARY KEY NOT NULL,
                TShopId INTEGER NOT NULL,
                link TEXT NOT NULL,
                active INTEGER NOT NULL,
                comment TEXT NOT NULL,
                UNIQUE(TShopId, link));""")     
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TPrice(
                id INTEGER PRIMARY KEY NOT NULL,
                TTaskId INTEGER NOT NULL,
                dt INTEGER NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                comment TEXT NOT NULL);""")
        self.__conn.commit()
    # The shop operations #
    def shopAdd(self, name, comment = ""):
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO TShop(name, comment) VALUES(?, ?)", (name, comment));
        self.__conn.commit()
    def shopExists(self, name):
        cursor = self.__conn.cursor()
        for row in cursor.execute("SELECT * FROM TShop WHERE name = ?", (name,)):
            return True
        return False
    def shopList(self):
        result = []
        cursor = self.__conn.cursor()
        for row in cursor.execute("SELECT name, comment FROM TShop"):
            result.append([row[0], row[1]])
        return result   
    def taskAdd(self, shop_name, link):
        cursor = self.__conn.cursor();
        cursor.execute("""INSERT INTO TTask(TShopId, link, active, comment) 
                VALUES((SELECT id FROM TShop WHERE name = ?), ?, 1, \"\")""", 
                (shop_name, link))
        self.__conn.commit()
    def taskExists(self, shop_name, link):
        cursor = self.__conn.cursor()
        for row in cursor.execute("""SELECT * FROM TTask 
                WHERE TShopId = (SELECT id FROM TShop WHERE name = ?)
                AND link = ?""", (shop_name, link)):
            return True
        return False
    def taskList(self):
        result = []
        cursor = self.__conn.cursor()
        for row in cursor.execute("SELECT name, link, (SELECT COUNT(*) FROM TPrice WHERE TTaskId = TTask.id) FROM TShop, TTask WHERE TTask.TShopId = TShop.id"):
            result.append([row[0], row[1], row[2]])
        return result
    def taskRemove(self, shop_name, link):
        cursor = self.__conn.cursor()
        cursor.execute("""DELETE FROM TPrice WHERE TTaskId = 
                (SELECT id FROM TTask WHERE TShopId = 
                    (SELECT id FROM TShop WHERE name = ?) AND link = ?)""",
                (shop_name, link))
        cursor.execute("""DELETE FROM TTask WHERE 
                TShopId = (SELECT id FROM TShop WHERE name = ?) AND link = ?""",
                (shop_name, link))
        self.__conn.commit()
    def priceAdd(self, shop_name, link, dt, price, currency):
        cursor = self.__conn.cursor()
        cursor.execute("""INSERT INTO TPrice(TTaskId, dt, price, currency, comment)
                VALUES((SELECT id FROM TTask WHERE TShopId = (SELECT id FROM TShop WHERE name = ?) 
                AND link = ?), ?, ?, ?, ?)""", (shop_name, link, dt, price, currency, ""))
        self.__conn.commit()
 