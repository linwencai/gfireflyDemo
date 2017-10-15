#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""

class User:
    def __init__(self, data):
        self.data = data
        return

    def getData(self):
        """ 获取用户数据
        """
        return self.data

    def getAcc(self):
        """ 获取帐号名
        """
        return self.data.get("acc")
