# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     gameApplication
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'

import tornado.web
import random
from handlers import MainHandler
from threads import  MainThread
from config.settings import DEBUG


class GameApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            #游戏主逻辑
            (r"/", MainHandler.MainGameHandler),
        ]

        tornado.web.Application.__init__(self,handlers,debug=DEBUG)

        self.workerThreads = []

        for i in range(0,4):
            t = MainThread.MainThread()
            t.start()
            self.workerThreads.append(t)


    def stopApplication(self):
        for t in self.workerThreads:
            t.pushToThead(None)
            t.join()


    def pushToWorkThread(self,handler):
        t = random.choice(self.workerThreads)
        t.pushToThead(handler)