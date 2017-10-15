# -*- coding: utf8 -*-

"""
#配置管理器
Created on 2014-07-21
@author: Linwencai
"""

import os
import csv
import json
import codecs
from datetime import datetime
from xml.etree import ElementTree
from firefly.utils.singleton import Singleton
from twisted.python import log

CONFIG_PATH = "config/"  # config目录
CONFIG_BASE_FILE = "config.txt"  # 基础配置文件
UTF8_TAG = codecs.BOM_UTF8  # UTF-8文件头信息
JSON_INDENT = None  # json缩进
JSON_SEPARATORS = (',', ':')  # json分隔符

# _Config = None


class Config(object):
    _filePath = None
    _dict = {}  # 数据字典
    _json = None

    def getValue(self, key, default=None, isLog=True):
        """获取key对应的值
        """
        if key not in self._dict and isLog:
            log.err("getValue error key:%s %s file:%s" % (key, type(key), os.path.basename(self._filePath)))
            return default
        return self._dict.get(key, default)

    def getDict(self):
        """获取数据字典
        """
        return self._dict

    def toJson(self):
        """获取json
        """
        if not self._json:
            self._json = json.dumps(self._dict, ensure_ascii=False, indent=JSON_INDENT,
                                    separators=JSON_SEPARATORS, default=jsonDefault)
        return self._json

    def getKeys(self):
        """获取键列表
        """
        return self._dict.keys()

    def toClient(self):
        return self._dict

    def __init__(self, fielPath):
        self._readFile(fielPath)
        return

    def _readFile(self, fielPath):
        return

    def reload(self):
        self._readFile(self._filePath)
        return


def jsonDefault(obj):
    """json.dumps支持CodeType类型
    """
    import types
    if isinstance(obj, types.CodeType):
        return obj.co_filename
    else:
        raise TypeError('%r is not JSON serializable' % obj)


class ConfigIni(Config):
    """ini配表（一维表）
    """
    def _readFile(self, filePath, isEval=True):
        self._filePath = filePath
        fp = open(filePath)
        lines = fp.readlines()
        fp.close()

        self._dict = {}
        firstLine = True
        for line in lines:
            # 去除多余的字符
            line = line.strip()
            if firstLine:
                line = line.replace(UTF8_TAG, "")
                firstLine = False

            # 跳过空行和注释行
            if not line or line[0] == "#":
                continue

            # 分割1次“=”
            data = line.split("=", 1)
            if len(data) != 2:
                continue

            # 获取key和value
            key = data[0].strip()
            if isEval:
                try:
                    value = eval(data[1].strip())
                except BaseException:
                    value = data[1].strip()
            else:
                value = data[1].strip()

            # 放入字典
            if key in self._dict:
                print("ConfigIni error: %s have same key %s" % (filePath, key))
            self._dict[key] = value
            #self.__dict__.update(self._dict)
        return


class Config2d(Config):
    """二维表
    """
    def _readFile(self, filePath):
        self._filePath = filePath
        fp = open(filePath)
        lines = fp.readlines()
        fp.close()

        self._dict = {}
        # 字段列表
        tagList = [tag.strip() for tag in lines[1].rstrip().split("\t")]

        # 类型列表
        typeList = [tag.strip().lower() for tag in lines[2].split("\t")]

        for line in lines[3:]:
            tmpDict = {}
            primaryKey = None
            #lineList = line.rstrip().split("\t")
            lineList = line.split("\t")
            lineList[-1] = lineList[-1].rstrip()
            if not lineList:
                continue
            for index, value in enumerate(lineList):
                valueType = typeList[index]
                if valueType == "primary":  # 主键
                    primaryKey = value
                    tmpDict[tagList[index]] = value
                elif valueType == "int":  # 整型
                    tmpDict[tagList[index]] = int(value)
                elif valueType == "float":  # 浮点型
                    tmpDict[tagList[index]] = float(value)
                elif valueType == "str":  # 字符串
                    tmpDict[tagList[index]] = value
                elif valueType == "eval":  # 列表、字典
                    tmpDict[tagList[index]] = eval(value)
                elif valueType == "compile":  # 公式
                    tmpDict[tagList[index]] = compile(value, value, "eval")
                elif valueType == "datetime":  # 日期 年/月/日 时:分
                    tmpDict[tagList[index]] = datetime.strptime(value, "%Y/%m/%d %H:%M")
                elif valueType == "datetime2":  # 日期 年-月-日 时:分:秒
                    tmpDict[tagList[index]] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                elif valueType == "date":  # 日期 年/月/日
                    tmpDict[tagList[index]] = datetime.strptime(value, "%Y/%m/%d")
                elif valueType == "date2":  # 日期 年-月-日
                    tmpDict[tagList[index]] = datetime.strptime(value, "%Y-%m-%d")
                elif valueType == "time":  # 时间 时:分:秒
                    tmpDict[tagList[index]] = datetime.strptime(value, "%H:%M:%S")
                elif valueType == "null":  # 空
                    pass
                else:
                    print("Config2d error: %s unknown type %s." % (filePath, valueType))

            # 放入字典
            if primaryKey in self._dict:
                print("Config2d error: %s have same key %s" % (filePath, primaryKey))
            self._dict[primaryKey] = tmpDict
        return

    def getTagValue(self, key, tag, default=None):
        """获取key&tag对应的值
        """
        key = str(key)
        if key not in self._dict:
            print("Config2d not have key:%s" % key)
            return
        return self._dict[key].get(tag, default)

    def getTagsValues(self, key, *tags):
        """获取key&tag列表对应的值
        @param key:键
        @param tags:标签列表
        @return 对应的值列表
        """
        key = str(key)
        valueList = self._dict.get(key)
        if not valueList:
            print("Config2d not have key:%s" % key)
            return [None] * len(tags)
        return [valueList.get(tag) for tag in tags]

    def getTagAllValue(self, tag):
        """获取tag列的所有值列表
        """
        return [tmpDict[tag] for tmpDict in self._dict.values()]

    def getLineClass(self, key):
        """获取行实例(可以用.tag取得数据)
        @param key:
        @return:
        """
        key = str(key)
        tmpDict = self.getValue(key)
        if not tmpDict:
            return None
        else:
            class tmpC:
                def __init__(self, tmpDict):
                    self.__dict__.update(tmpDict)
            return tmpC(tmpDict)

    def getValue(self, key, default=None, isLog=True):
        """获取key对应的值
        """
        key = str(key)
        if key not in self._dict and isLog:
            log.err("getValue error key:%s %s file:%s" % (key, type(key), os.path.basename(self._filePath)))
            return default
        return self._dict.get(key, default)

    def toJson(self):
        """获取json，二维表返回列表型json
        """
        if not self._json:
            self._json = json.dumps(self._dict.values(), ensure_ascii=False, indent=JSON_INDENT,
                                    separators=JSON_SEPARATORS, default=jsonDefault)
        return self._json

    def toClient(self):
        return self._dict.values()


class ConfigJson(Config):
    """json表
    """
    def _readFile(self, filePath):
        self._filePath = filePath
        fp = open(filePath)
        content = fp.read()
        fp.close()

        content = content.replace(UTF8_TAG, "")
        self._dict = json.loads(content)
        return


class ConfigEval(Config):
    """eval表
    """
    def _readFile(self, filePath):
        self._filePath = filePath
        fp = open(filePath)
        content = fp.read()
        fp.close()

        content = content.replace(UTF8_TAG, "")
        self._dict = eval(content)


class ConfigXml(Config):
    """xml表
    """
    def _readFile(self, filePath):
        self._filePath = filePath
        tree = ElementTree.parse(filePath)
        root = tree.getroot()
        self._dict = build_dict(root)
        return


class ConfigCsv(Config2d):
    """csv表
    """
    def _readFile(self, filePath):
        self._filePath = filePath
        fp = open(filePath)
        lines = [line for line in csv.reader(fp)]
        fp.close()

        self._dict = {}
        # 字段列表
        tagList = [tag.strip() for tag in lines[1]]

        # 类型列表
        typeList = [tag.strip().lower() for tag in lines[2]]

        for lineList in lines[3:]:
            tmpDict = {}
            primaryKey = None
            #lineList = line.rstrip().split("\t")
            #lineList = line.split("\t")
            lineList[-1] = lineList[-1].rstrip()
            if not lineList:
                continue
            for index, value in enumerate(lineList):
                valueType = typeList[index]
                if valueType == "primary":  # 主键
                    primaryKey = value
                    tmpDict[tagList[index]] = value
                elif valueType == "int":  # 整型
                    tmpDict[tagList[index]] = int(value)
                elif valueType == "float":  # 浮点型
                    tmpDict[tagList[index]] = float(value)
                elif valueType == "str":  # 字符串
                    tmpDict[tagList[index]] = value
                elif valueType == "eval":  # 列表、字典
                    tmpDict[tagList[index]] = eval(value)
                elif valueType == "compile":  # 公式
                    tmpDict[tagList[index]] = compile(value, value, "eval")
                else:
                    print("Config2d error: %s unknown type %s." % (filePath, valueType))

            # 放入字典
            if primaryKey in self._dict:
                print("Config2d error: %s have same key %s" % (filePath, primaryKey))
            self._dict[primaryKey] = tmpDict
        return

# class ConfigCsv():
#     """csv表
#     """
#     _dict = {}  # 数据字典
#     _list = []
#     _json = None
#
#     def __init__(self, filePath):
#         fp = open(filePath)
#         self._list = [line for line in csv.reader(fp)]
#         fp.close()
#
#         for index, line in enumerate(self._list):
#             self._dict
#
#     def getValue(self, key, default=None):
#         """获取key对应的值
#         """
#         if key not in self._dict:
#             print("getValue error key:%s" % key)
#             return default
#         return self._dict.get(key, default)
#
#     def getDict(self):
#         """获取数据字典
#         """
#         return self._dict
#
#     def toJson(self):
#         """获取json
#         """
#         if not self._json:
#             self._json = json.dumps(self._dict, ensure_ascii=False, indent=JSON_INDENT,
#                                     separators=JSON_SEPARATORS, default=jsonDefault)
#         return self._json


class ConfigMgr:
    """配置管理器
    """
    __metaclass__ = Singleton
    _configFileDict = {}  # {配置文件路径:类型}
    _dict = {}  # {文件名:配置实例}

    def __init__(self):
        # 读取基础配置文件，获得每个配置文件路径与类型
        # print("ConfigMgr start init path:%s" % os.path.abspath(CONFIG_PATH + CONFIG_BASE_FILE))
        fpConfig = open(CONFIG_PATH + CONFIG_BASE_FILE)
        lines = fpConfig.readlines()
        fpConfig.close()
        for line in lines[1:]:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            line = line.split("\t")
            if len(line) < 2:
                continue
            if line[0] in self._configFileDict:
                print "ConfigMgr Error same file %s" % line[0]
            self._configFileDict[line[0]] = line[1]

        # 读取每个配置文件
        for fileName, fileType in self._configFileDict.items():
            #baseName, ext = os.path.splitext(fileName)
            baseName = os.path.basename(fileName)
            fileType = fileType.lower()
            if fileType == "ini":
                self._dict[baseName] = ConfigIni(CONFIG_PATH + fileName)
            elif fileType == "2d":
                self._dict[baseName] = Config2d(CONFIG_PATH + fileName)
            elif fileType == "json":
                self._dict[baseName] = ConfigJson(CONFIG_PATH + fileName)
            elif fileType == "xml":
                self._dict[baseName] = ConfigXml(CONFIG_PATH + fileName)
            elif fileType == "eval":
                self._dict[baseName] = ConfigEval(CONFIG_PATH + fileName)
            elif fileType == "csv":
                self._dict[baseName] = ConfigCsv(CONFIG_PATH + fileName)
            else:
                print("ConfigMgr Error unknown fileType:%s" % fileType)
        # print("ConfigMgr init finish %s" % self._dict.keys())
        return

    def getConfig(self, key):
        if key not in self._dict:
            print "ConfigMgr Error getConfig unknown key %s" % key
            return
        return self._dict[key]

    def getKeys(self):
        return self._dict.keys()

    def getAllJson(self):
        tmpDict = {}
        for baseName, configIns in self._dict.items():
            tmpDict[baseName] = configIns._dict
        return json.dumps(tmpDict, separators=JSON_SEPARATORS)

    def reload(self):
        self._configFileDict = {}
        self.__init__()
        return


def attr(elem, *args):
    if len(args) > 1:
        result = []
        for name in args:
            result.append(attr(elem, name))
        return result

    [name] = args
    value = elem.attrib.get(name)
    if not value:
        return value
    elif isinstance(value, unicode):
        return value.encode("GBK")
    elif value.isdigit():
        return int(value)
    elif value.lower() in ["true", "false"]:
        return value.lower() == "true"
    else:
        return value


def fix_attribs(elem):
    _dict = {}
    for key in elem.attrib:
        _dict.update({key: attr(elem, key)})
    return _dict


def build_dict(elem):
    _dict = {}
    if elem is None:
        return _dict
    for subelem in elem:
        if subelem.tag in _dict:  # 如果有相同的标签，将原有的值转为列表
            if not isinstance(_dict[subelem.tag], list):
                _dict[subelem.tag] = [_dict[subelem.tag]]
            _dict[subelem.tag].append(build_dict(subelem))
        else:
            _dict.update({subelem.tag: build_dict(subelem)})  # 递归节点
        if subelem.text and subelem.text.strip():  # 标签的内容
            _dict.update({subelem.tag: {"_text": subelem.text}})
    _dict.update(fix_attribs(elem))  # 标签的属性
    return _dict


# def init():
#     """初始化配置管理器
#     """
#     global _Config
#     _Config = configMgr()


# def getConfig(fileName):
#     """根据文件名获取配置
#     """
#     return ConfigMgr().GetConfigIns(fileName)
#
#
# def getConfigFileList():
#     """获取所有配置文件名
#     """
#     return ConfigMgr().GetKeys()
#
#
# def getAllJson():
#     return ConfigMgr().GetAllJson()


# print(u"开始读取配置 %s" % os.path.abspath(CONFIG_PATH + CONFIG_BASE_FILE))
# init()
# print(u"完成读取配置")


# if __name__ == "__main__":
#     for fileName in getConfigFileList():
#         configIns = getConfig(fileName)
#         #if fileName != "testXml.xml":continue
#         print fileName
#         #print configIns.toJson()
#         print "*" * 60
