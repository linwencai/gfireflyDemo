#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from gfirefly.server.globalobject import GlobalObject
from gfirefly.server.globalobject import netserviceHandle
from gfirefly.utils.services import CommandService
from gtwisted.utils import log

def callTarget(self, targetKey, *args, **kw):
    target = self.getTarget(0)
    return target(targetKey, *args, **kw)
CommandService.callTarget = callTarget

@netserviceHandle
def Forwarding_0(key, _conn, data):
    '''转发服务器.用来接收客户端的消息转发给其他服务
    '''
    log.msg("Recv Key:%s dynamicId:%s data:%s" % (key, _conn.transport.sessionno, data))
    message = GlobalObject().remote['gate'].callRemote("forwarding", key, _conn.transport.sessionno, data)
    return message

