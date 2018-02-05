# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     settings
   Author :       talus
   date：          2018/2/5 0005
   Description :settings
-------------------------------------------------

"""
__author__ = 'talus'

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


DEBUG = True
APP_NAME = "SheepGame"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if DEBUG:
    """
    测试地址
    """
    REDIS_ADDR = r"127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0

    MONGO_ADDR = r"127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB = "game"

    LOG_FILE = ""
    # 服务器端口
    SERVER_PORT = 6678
else:
    """
    上线地址
    """
    REDIS_ADDR = r"127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0

    MONGO_ADDR = r"127.0.0.1"
    MONGO_PORT = 27017
    MONGO_DB = "game"

    LOG_FILE = os.path.join(BASE_DIR,*["log","log.txt"])
    # 服务器端口
    SERVER_PORT = 6678


