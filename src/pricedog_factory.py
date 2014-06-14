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
from pricedog_mod_e2e4online import *
from pricedog_mod_dns import *

class Factory:
    __fun = {}
    __comment = {}
    def __init__(self):
        self.register(fun_e2e4online_key(), fun_e2e4online_comment(), fun_e2e4online_callback)
        self.register(fun_dns_key(), fun_dns_comment(), fun_dns_callback)
    def register(self, key, comment, fun):
        self.__fun[key] = fun
        self.__comment[key] = comment
    def keys(self):
        return self.__fun.keys()
    def fun(self, key):
        return self.__fun[key]
    def comment(self, key):
        return self.__comment[key]
   