#coding:utf8
"""
Created on 2014-07-21
@author: Linwencai
"""
from json import loads
from gtwisted.utils import log
from gfirefly.server.globalobject import rootserviceHandle, GlobalObject
from app.gate.GateApp import localservice

@rootserviceHandle
def forwarding(key, dynamicId, data):
    if not data:
        dataDict = {}
    else:
        dataDict = loads(data)  # json转dict

    if key in localservice._targets:
        return localservice.callTarget(key, key, dynamicId, dataDict)
    else:
        return GlobalObject().root.callChild("game", key, key, dynamicId, dataDict)


@rootserviceHandle
def netconnlost(dynamicId):
    """ 客户端断线 net转发给game
    """
    log.msg('%s connlost' % dynamicId)
    GlobalObject().root.callChild("game", 103, 103, dynamicId, None)
    return


@rootserviceHandle
def pushObject(topicID, msg, dynamicIdList):
    """ 推送消息 game转发给net
    """
    GlobalObject().root.callChild("net", "pushObject", topicID, msg, dynamicIdList)
    return

