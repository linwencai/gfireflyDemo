#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""
import time
import json
import struct
from time import sleep
from thread import start_new
from socket import AF_INET, SOCK_STREAM, socket

HOST = raw_input("host:")
if not HOST:
    HOST = "127.0.0.1"

PORT = 10000
BUFSIZE = 1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

HEAD_0 = chr(1)
HEAD_1 = chr(2)
HEAD_2 = chr(3)
HEAD_3 = chr(4)
ProtoVersion = chr(5)
ServerVersion = 6
HEAD = struct.pack('!sssssI', HEAD_0, HEAD_1, HEAD_2, HEAD_3, ProtoVersion, ServerVersion)


def sendData(sendstr, commandId):
    dataInfo = struct.pack('!2I', len(sendstr) + 4, commandId)
    return HEAD + dataInfo + sendstr


def resolveRecvdata(data):
    index = 0
    while index < len(data):
        index = data.find(HEAD, index)
        if index == -1:
            break
        index += len(HEAD) + 8
        length, key = struct.unpack('!2I', data[index -8: index])
        dataStr = data[index: index + length]
        index += length - 4
        try:
            dataDict = json.loads(dataStr, "utf-8")
            dataJson = json.dumps(dataDict, ensure_ascii=False, indent=2, sort_keys=True)
            print "!!!!!!!!!!recv:%s!!!!!!!!!!\n%s" % (key, dataJson)
        except BaseException:
            dataStr = unicode(dataStr, "utf-8")
            print '!!!!!!!!!!recv:%s!!!!!!!!!!\n%s' % (key, dataStr)
    return data


def recv():
    while True:
        try:
            message = client.recv(BUFSIZE)
            resolveRecvdata(message)
        except BaseException, e:
            time.sleep(1)
            print e


def send():
    def _send(key):
        if key == 0:
            return True
        elif key == 101:
            msg = sendData('{"acc":"hiac","pwd":"123"}', key)
        elif key == 102:
            msg = sendData('{"acc":"hiac","pwd":"123"}', key)
        else:
            msg = raw_input("json:")
            msg = sendData(msg, key)
        client.sendall(msg)
        return

    while True:
        try:
            key = int(raw_input("key:"))
            if _send(key):
                break
            sleep(0.3)
        except Exception as e:
            print(e)
    return


if __name__ == "__main__":
    start_new(recv, ())
    send()

