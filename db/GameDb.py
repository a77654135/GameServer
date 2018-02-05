# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     GameDb
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'

import redis
import pymongo
import config.settings as settings

def connectToMongo(dbName = None):
    __mongo = pymongo.MongoClient(host=settings.MONGO_ADDR,port=settings.MONGO_PORT)
    __mongo = __mongo[dbName] if dbName else __mongo[settings.MONGO_DB]
    return __mongo

def connectToRedis(dbIdx = None):
    __redis = redis.Redis(host=settings.REDIS_ADDR,port=settings.REDIS_PORT,db=dbIdx if dbIdx is not None else settings.REDIS_DB)
    __redis.ping()
    return __redis