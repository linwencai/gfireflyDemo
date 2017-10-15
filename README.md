# gfireflyDemo

[![Build Status](https://img.shields.io/travis/rust-lang/rust/master.svg)]()
[![Python](https://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/)

gfireflyDemo是一个简单的游戏服务端Demo，基于[G-Firefly](https://github.com/9miao/G-Firefly) 框架([Firefly](https://github.com/9miao/Firefly) 的协程版，性能更好)  

--------

## 环境
* Python2.7
* MySQL5.6+
* memcached


## 依赖
* affinity==0.1.0
* DBUtils==1.2
* firefly==1.3.3.dev0
* MySQL-python==1.2.5
* python-memcached==1.58
* six==1.11.0
* Twisted==14.0.0
* zope.interface==4.4.3
* Flask==0.10.1
* gevent==1.0.2
* gevent-zeromq==0.2.5
* gfirefly==0.1.9a0
* greenlet==0.4.12
* gtwisted==0.2.8a0
* itsdangerous==0.24
* Jinja2==2.9.6
* MarkupSafe==1.0
* pyzmq==2.2.0
* Werkzeug==0.12.2


## 安装
* 安装Python、MySQL、memcached
* 执行tool目录下的install脚本，自动安装依赖、导入sql  

  ``` 
  # windows
  >>> install.bat

  # linux
  >>> sh install.sh
  ```

  
## 快速开始
1. 编辑config.json，配置端口、数据库
2. 运行服务端
  ```
  >>> python startmaster.py
  ```
3. 运行客户端模拟器
  ```
  >>> python tool/clienttest.py
  ```


 :relaxed: