#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
from gtwisted.utils import log
from app.game.GameApp import GameServiceHandle, SendMessage
from app.game.core.userManager import UserManager


@GameServiceHandle
def register_101(key, dynamicId, argument):
    """ 注册协议.
    """
    log.msg("register_101 dynamicId:%s argument:%s" % (dynamicId, argument))
    acc = argument.get('acc')  # 获取帐号
    pwd = argument.get('pwd')  # 获取密码
    userData = UserManager().createUser(dynamicId, acc, pwd)  # 创建用户
    if userData:
        return SendMessage(1, userData)  # 创建成功，返回用户数据
    else:
        return SendMessage(0, "")  # 创建失败


@GameServiceHandle
def login_102(key, dynamicId, argument):
    """ 登录协议.
    """
    log.msg("login_102 dynamicId:%s argument:%s" % (dynamicId, argument))
    acc = argument.get('acc')
    pwd = argument.get('pwd')
    user = UserManager().addUser(dynamicId, acc, pwd)
    if user:
        return SendMessage(1, user.getData())
    else:
        return SendMessage(0, "")


@GameServiceHandle
def logout_103(key, dynamicId, argument):
    """ 下线协议.(客户端断开socket时自动调用)
    """
    log.msg("logout_103 dynamicId:%s argument:%s" % (dynamicId, argument))
    result = UserManager().dropUser(dynamicId)
    return SendMessage(result, "")

