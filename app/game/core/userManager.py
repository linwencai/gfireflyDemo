#coding:utf8
"""
Created on 2015/5/8
@author: Linwencai
"""
from gfirefly.utils.singleton import Singleton
from gfirefly.dbentrust.madminanager import MAdminManager
from gfirefly.dbentrust.mmode import MAdmin
from app.game.core.user import User


class UserManager:
    __metaclass__ = Singleton  # 单例

    def __init__(self):
        self._users = {}  # 玩家字典
        self.memUsers = MAdmin("tb_user", "acc")  # 玩家表mem实例
        self.memUsers.insert()
        MAdminManager().registe(self.memUsers)
        return

    def createUser(self, dynamicId, acc, pwd):
        """ 创建用户
        """
        if self.memUsers.getObj(str(acc)):
            return False
        userData = {"acc": acc, "pwd": pwd}
        memUser = self.memUsers.new(userData)  # 创建mem对象
        user = User(userData)  # 实例化用户
        self._users[dynamicId] = user  # 添加到管理器
        return user.getData()  # 返回用户数据

    def addUser(self, dynamicId, acc, pwd):
        """ 添加用户到管理器
        """
        userData = self.memUsers.getObjData(str(acc))  # 从mem中获取用户数据
        if not userData:  # mem中无数据
            return False
        if userData.get("pwd") != pwd:  # 密码错了
            return False
        user = User(userData)  # 实例化用户
        self._users[dynamicId] = user  # 添加到管理器
        return user  # 返回用户实例

    def getUser(self, dynamicId):
        """ 获取用户
        """
        return self._users.get(dynamicId)  # 返回用户实例

    def dropUser(self, dynamicId):
        """ 从管理器删除用户
        """
        user = self.getUser(dynamicId)  # 获取用户实例
        if not user:
            return 0
        acc = user.getAcc()  # 获取帐号名
        memUser = self.memUsers.getObj(str(acc))  # 获取mem对象
        if not memUser:
            return 0
        memUser.update_multi(user.data)  # 更新数据
        memUser.syncDB()  # 保存到数据库
        del self._users[dynamicId]  # 从管理器删除用户
        return 1
