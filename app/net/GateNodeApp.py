#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from gfirefly.server.globalobject import GlobalObject, remoteserviceHandle


@remoteserviceHandle('gate')
def pushObject(topicID,msg,sendList):
    GlobalObject().netfactory.pushObject(topicID, msg, sendList)
    return

