#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from json import dumps

from gtwisted.utils import log
from gfirefly.server.globalobject import GlobalObject
from gfirefly.utils.services import CommandService


GameService = CommandService("GameServer")
GlobalObject().remote['gate']._reference.addService(GameService)


def GameServiceHandle(target):
    GameService.mapTarget(target)


def SendMessage(state, message, topicID=0, dynamicIds=None):
    """ 返回消息
    :param state: 返回的状态
    :param message: 返回的消息
    :param topicID: 协议号
    :param dynamicIds: 推送的客户端Id
    :return:
    """
    jsonData = dumps({'State': state, 'Data': message}, separators=(',', ':'))
    if dynamicIds:
        GlobalObject().remote['gate'].callRemote("pushObject", topicID, jsonData, dynamicIds)
    return jsonData
    