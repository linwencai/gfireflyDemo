#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from gfirefly.server.globalobject import GlobalObject
from gfirefly.netconnect.datapack import DataPackProtoc


# 定义包头
dataprotocl = DataPackProtoc(1, 2, 3, 4, 5, 6)
GlobalObject().netfactory.setDataProtocl(dataprotocl)


def callWhenConnCreate(conn):
    """ 连接建立时回调
    """
    return
GlobalObject().netfactory.doConnectionMade = callWhenConnCreate


def callWhenConnLost(conn):
    """ 连接断开时回调
    """
    dynamicId = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote("netconnlost", dynamicId)
    return
GlobalObject().netfactory.doConnectionLost = callWhenConnLost


def loadModule():
    import NetApp
    import GateNodeApp

