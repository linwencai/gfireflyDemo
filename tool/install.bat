pip install affinity==0.1.0
pip install six==1.11.0
pip install zope.interface==4.4.3
pip install Twisted==14.0.0
pip install python-memcached
easy_install MySQL-python
pip install DBUtils
pip install firefly
@rem easy_install https://ncu.dl.sourceforge.net/project/pywin32/pywin32/Build%20220/pywin32-220.win32-py2.7.exe
pip install pypiwin32

pip install itsdangerous
pip install Jinja2
pip install Werkzeug
pip install flask==0.10.1
pip install greenlet
pip install gevent==1.0.2
easy_install pyzmq==2.2.0
@rem easy_install https://pypi.doubanio.com/packages/84/4e/0475be450df4b3dba2d30fe92f2af579177cee71790da90d2d9e7be278d9/pyzmq-2.2.0-py2.7-win32.egg
pip install gevent-zeromq
pip install gfirefly

@echo import sql?
@pause
mysql -uroot -p < mysql.sql
@echo success!