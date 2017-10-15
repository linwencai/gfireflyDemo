pip install affinity==0.1.0
pip install six==1.11.0
pip install zope.interface==4.4.3
wget https://pypi.douban.com/packages/76/38/cf8f81c1d7d84fec922d67f0d92bfa9fee59145d875d7263ceefa2bbbaf4/Twisted-14.0.0.tar.bz2
tar -jxf Twisted-14.0.0.tar.bz2
cd Twisted-14.0.0
python setup.py install 1>/dev/null
cd ..
pip install python-memcached
pip install MySQL-python
pip install DBUtils
pip install firefly

pip install itsdangerous
pip install Jinja2
pip install Werkzeug
pip install flask==0.10.1
pip install greenlet
pip install gevent==1.0.2
#yum install -y zeromq zeromq-devel
pip install pyzmq==2.2.0
pip install gevent-zeromq
pip install gfirefly

read -p "import sql?"
mysql -uroot -p < mysql.sql
echo "success!"