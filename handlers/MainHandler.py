# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MainHandler
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'

import tornado.web
import json
from main import gameGlobal
from common.ColorLogger import getUZWLogger

class MainGameHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        self.application.pushToWorkThread(self)

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.application.pushToWorkThread(self)


    def process(self):
        return json.dumps(gameGlobal.process(self))

