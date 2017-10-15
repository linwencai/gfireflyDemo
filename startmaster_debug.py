#coding:utf8

from gevent import monkey; monkey.patch_os()
import os
import json
import subprocess
from sys import argv
from time import sleep
from gtwisted.core import reactor
from gfirefly.server.server import FFServer
from gfirefly.master.master import Master, MASTER_SERVER_MODE

debugSername = ""  # 要调试的服务器名

if len(argv) == 1:
    if not debugSername:
        debugSername = raw_input("Debug Server Name:")
    cmds = 'python %s %s' % (os.path.basename(argv[0]), MASTER_SERVER_MODE)
    subprocess.Popen(cmds, shell=True)
    sleep(3)

    config = json.load(open('config.json', 'r'))
    sersconf = config.get('servers')
    for sername in sersconf.keys():
        if sername == debugSername:
            continue
        cmds = 'python %s %s %s'%('appmain.py', sername, 'config.json')
        subprocess.Popen(cmds, shell=True)

    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers',{})
    masterconf = config.get('master',{})
    serconfig = sersconf.get(debugSername)
    ser = FFServer()
    ser.config(serconfig, servername=debugSername, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
else:
    master = Master()
    master.config('config.json', 'appmain.py')
    master.masterapp()
    reactor.run()
