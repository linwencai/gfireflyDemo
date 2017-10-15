#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2015/5/8
@author: Linwencai
"""

from gevent import monkey; monkey.patch_os()
import json,sys
from gfirefly.server.server import FFServer


from gtwisted.core import reactor
from gfirefly.netconnect.protoc import LiberateFactory
from flask import Flask
#from gtwisted.core.protocols import BaseProtocol,ServerFactory
#from twisted.internet.protocol import Factory, Protocol, ServerFactory
#from firefly.netconnect.protoc import DefferedErrorHandle
import hashlib, struct, base64
from datetime import datetime
from json import loads

from gtwisted.utils import log
from gtwisted.core import protocols

class Broadcaster(protocols.BaseProtocol):
    buff = ""
    sockets = None
##    def __init__(self, sockets, arg):
##        print sockets,arg
##        self.sockets = sockets

    def connectionMade(self):
        address = self.transport.getAddress()
        log.msg('Client %d login in.[%s,%d]'%(self.transport.sessionno,\
                address[0],address[1]))
        self.factory.connmanager.addConnection(self)
        self.factory.doConnectionMade(self)
##        if not self.sockets.has_key(self):
##            self.sockets[self] = {}
##        print datetime.now(), "connect:", self.transport.sessionno, "count:", len(self.sockets)
        # self.transport.loseConnection()

    def dataReceived(self, msg):
        if msg.lower().find('upgrade: websocket') != -1:
            self.hand_shake(msg)
        else:
            raw_str = self.parse_recv_data(msg)
            # from json import dumps
            # from time import time
            # try:
            #     data = {"time": time(), "data": str(raw_str)}
            #     data = dumps(data)
            # except BaseException as err:
            #     print "Err:", err, "Raw_str:", raw_str
            #     data = "Error code:%s" % repr(raw_str)
            # self.send_data(data)
            if not raw_str:
                return

            key, dataStr = raw_str.split(" ", 1)
            deferred = GlobalObject().remote['gate'].callRemote("forwarding", int(key), self.transport.sessionno, dataStr)

            if deferred:
                #deferred.addCallback(self.send_data)
                #deferred.addErrback(DefferedErrorHandle)
                self.send_data(deferred)
                
            return deferred
            # self.send_data(str(message))
            # return message

    def connectionLost(self, reason):
##        if self.sockets.has_key(self):
##            del self.sockets[self]
##        print datetime.now(), "lost:", self.transport.sessionno
##        return
        log.msg('Client %d login out.'%(self.transport.sessionno))
        self.factory.doConnectionLost(self)
        self.factory.connmanager.dropConnectionByID(self.transport.sessionno)
        

    def closeConnection(self):
##        if self.sockets.has_key(self):
##            del self.sockets[self]
        print datetime.now(), "close:", self.transport.sessionno
        return

    def generate_token(self, key1, key2, key3):
        num1 = int("".join([digit for digit in list(key1) if digit.isdigit()]))
        spaces1 = len([char for char in list(key1) if char == " "])
        num2 = int("".join([digit for digit in list(key2) if digit.isdigit()]))
        spaces2 = len([char for char in list(key2) if char == " "])

        combined = struct.pack(">II", num1/spaces1, num2/spaces2) + key3
        return hashlib.md5(combined).digest()

    def generate_token_2(self, key):
        key = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ser_key = hashlib.sha1(key).digest()

        return base64.b64encode(ser_key)

    def send_data(self, raw_str):
        if self.sockets:
            back_str = []
            back_str.append('\x81')
            data_length = len(raw_str)

            if data_length <= 125:
                back_str.append(chr(data_length))
            else:
                back_str.append(chr(126))
                back_str.append(chr(data_length >> 8))
                back_str.append(chr(data_length & 0xFF))

            back_str = "".join(back_str) + raw_str

            self.transport.sendall(back_str)
        else:
            back_str = '\x00%s\xFF' % (raw_str)
            self.transport.sendall(back_str)

    def parse_recv_data(self, msg):
        raw_str = ''

        if self.sockets:
            code_length = ord(msg[1]) & 127

            if code_length == 126:
                masks = msg[4:8]
                data = msg[8:]
            elif code_length == 127:
                masks = msg[10:14]
                data = msg[14:]
            else:
                masks = msg[2:6]
                data = msg[6:]

            i = 0
            for d in data:
                raw_str += chr(ord(d) ^ ord(masks[i%4]))
                i += 1
        else:
            raw_str = msg.split("\xFF")[0][1:]

        return raw_str

    def hand_shake(self, msg):
        headers = {}
        header, data = msg.split('\r\n\r\n', 1)
        for line in header.split('\r\n')[1:]:
            key, value = line.split(": ", 1)
            headers[key] = value

        headers["Location"] = "ws://%s/" % headers["Host"]

        if headers.has_key('Sec-WebSocket-Key1'):
            key1 = headers["Sec-WebSocket-Key1"]
            key2 = headers["Sec-WebSocket-Key2"]
            key3 = data[:8]

            token = self.generate_token(key1, key2, key3)

            handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Origin: %s\r\n\
Sec-WebSocket-Location: %s\r\n\r\n\
' %(headers['Origin'], headers['Location'])

            self.transport.sendall(handshake + token)

            self.sockets = False
        else:
            key = headers['Sec-WebSocket-Key']
            token = self.generate_token_2(key)

            handshake = '\
HTTP/1.1 101 Switching Protocols\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n\
' % (token)
            self.transport.sendall(handshake)

            self.sockets = True

##class BroadcastFactory(ServerFactory):
##    def __init__(self, *arg):
##        print arg
##        self.sockets = {}
##
##    def buildProtocol(self, addr):
##        print "buildProtocol:", addr
##        return Broadcaster(self.sockets)
from gfirefly.netconnect.manager import ConnectionManager
class BroadcastFactory(protocols.ServerFactory):
    '''协议工厂'''
    
    sockets = {}
    protocol = Broadcaster
    
    def __init__(self, *arg):
        '''初始化
        '''
        protocols.ServerFactory.__init__(self)
        self.service = None
        self.connmanager = ConnectionManager()
        
    def setDataProtocl(self,dataprotocl):
        '''
        '''
        self.dataprotocl = dataprotocl
        
    def doConnectionMade(self,conn):
        '''当连接建立时的处理'''
        pass
    
    def doConnectionLost(self,conn):
        '''连接断开时的处理'''
        pass
    
    def addServiceChannel(self,service):
        '''添加服务通道'''
        self.service = service
    
    def doDataReceived(self,conn,commandID,data):
        '''数据到达时的处理'''
        response = self.service.callTarget(commandID,conn,data)
        return response
    
    def produceResult(self,command,response):
        '''产生客户端需要的最终结果
        @param response: str 分布式客户端获取的结果
        '''
        return self.dataprotocl.pack(command,response)
    
    def loseConnection(self,connID):
        """主动端口与客户端的连接
        """
        self.connmanager.loseConnection(connID)
    
    def pushObject(self,topicID , msg, sendList):
        '''服务端向客户端推消息
        @param topicID: int 消息的主题id号
        @param msg: 消息的类容，protobuf结构类型
        @param sendList: 推向的目标列表(客户端id 列表)
        '''
        self.connmanager.pushObject(topicID, msg, sendList)
        


from gfirefly.distributed.root import PBRoot,BilateralFactory
from gfirefly.distributed.node import RemoteObject
from gfirefly.dbentrust.dbpool import dbpool
from gfirefly.dbentrust.memclient import memcached_connect
from gfirefly.server.logobj import loogoo
from gfirefly.server.globalobject import GlobalObject
from gtwisted.utils import log
from gfirefly.utils import services
import os,sys,affinity


def config(self, config, servername=None, dbconfig=None,
            memconfig=None, masterconf=None):
    '''配置服务器
    '''
    GlobalObject().json_config = config
    webSocketPost = config.get("webSocketPort")  # webSocket端口
    GlobalObject().remote_connect = self.remote_connect
    netport = config.get('netport')#客户端连接
    webport = config.get('webport')#http连接
    rootport = config.get('rootport')#root节点配置
    self.remoteportlist = config.get('remoteport',[])#remote节点配置列表
    if not servername:
        servername = config.get('name')#服务器名称
    logpath = config.get('log')#日志
    hasdb = config.get('db')#数据库连接
    hasmem = config.get('mem')#memcached连接
    app = config.get('app')#入口模块名称
    cpuid = config.get('cpu')#绑定cpu
    mreload = config.get('reload')#重新加载模块名称
    self.servername = servername

    if netport:
        self.netfactory = LiberateFactory()
        netservice = services.CommandService("netservice")
        self.netfactory.addServiceChannel(netservice)
        reactor.listenTCP(netport,self.netfactory)

    if webport:
        self.webroot = Flask("servername")
        GlobalObject().webroot = self.webroot
        reactor.listenWSGI(webport, self.webroot)

    if rootport:
        self.root = PBRoot()
        rootservice = services.Service("rootservice")
        self.root.addServiceChannel(rootservice)
        reactor.listenTCP(rootport, BilateralFactory(self.root))

    if webSocketPost:
        reactor.listenTCP(webSocketPost, BroadcastFactory())

    for cnf in self.remoteportlist:
        rname = cnf.get('rootname')
        self.remote[rname] = RemoteObject(self.servername)

    if hasdb and dbconfig:
        if dbconfig.has_key("user") and dbconfig.has_key("host") and dbconfig.has_key("host"):
            dbpool.initPool({"default":dbconfig})
        else:
            dbpool.initPool(dbconfig)

    if hasmem and memconfig:
        urls = memconfig.get('urls')
        memcached_connect(urls)
        from gfirefly.dbentrust.util import M2DB_PORT,M2DB_HOST,ToDBAddress
        ToDBAddress().setToDBHost(memconfig.get("pubhost",M2DB_HOST))
        ToDBAddress().setToDBPort(memconfig.get("pubport",M2DB_PORT))
    if logpath:
        log.addObserver(loogoo(logpath))#日志处理
    log.startLogging(sys.stdout)

    if cpuid:
        affinity.set_process_affinity_mask(os.getpid(), cpuid)
    GlobalObject().config(netfactory = self.netfactory, root=self.root,
                remote = self.remote)
    if app:
        __import__(app)
    if mreload:
        _path_list = mreload.split(".")
        GlobalObject().reloadmodule = __import__(mreload,fromlist=_path_list[:1])

    if masterconf:
        masterport = masterconf.get('rootport')
        masterhost = masterconf.get('roothost')
        self.master_remote = RemoteObject(servername)
        GlobalObject().masterremote = self.master_remote
        from gfirefly.server import admin
        addr = ('localhost',masterport) if not masterhost else (masterhost,masterport)
        self.master_remote.connect(addr)        
        		
    GlobalObject().remote_connect = self.remote_connect

FFServer.config = config


if __name__=="__main__":
    args = sys.argv
    servername = None
    config = None
    if len(args)>2:
        servername = args[1]
        config = json.load(open(args[2],'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(servername)
    ser = FFServer()
    ser.config(serconfig, servername=servername, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
    
    
