# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     MainThreads
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'

import threading
import tornado.ioloop
import Queue
import db.GameDb as GameDb
from common.ColorLogger import getUZWLogger
from common.ExceptCallStack import print_call_stack

logger = getUZWLogger()

class MainThread(threading.Thread):
    THREAD_ID = 0
    def __init__(self):
        threading.Thread.__init__(self)
        MainThread.THREAD_ID += 1
        self.name = r"[ MainThread #{} ]".format(MainThread.THREAD_ID)
        self.dataQueue = Queue.Queue()
        logger.info("start thread: {}".format(self.name))


    def pushToThead(self,handlerInst):
        """
        把一个handler实例推入工作线程
        如果推进None，将会结束该工作线程
        :param handlerInst:
        :return:
        """
        self.dataQueue.put(handlerInst)

    def finishHandler(self,handler,response):
        try:
            if response is None:
                handler.send_error(404)
            else:
                handler.finish(response)
        except Exception,e:
            handler.send_error(500)

    def run(self):
        try:
            mongo = GameDb.connectToMongo()
        except Exception,e:
            logger.error(r"{0}: connect to mongo err: {1}".format(self.name, e.message))
            return

        try:
            redis = GameDb.connectToRedis()
        except Exception,e:
            logger.error(r"{0}: connect to redis err: {1}".format(self.name, e.message))
            return

        while True:
            try:
                handler = self.dataQueue.get(True,0.5)
            except Queue.Empty,e:
                continue

            if handler is None:
                logger.warning(r"{}: get None handler,break processing. ".format(self.name))
                break

            try:
                setattr(handler,"_mongo",mongo)
                setattr(handler,"_redis",redis)
                response = handler.process()
            except Exception,e:
                print_call_stack()
                response = None

            try:
                tornado.ioloop.IOLoop.instance().add_callback(self.finishHandler,handler,response)
            except Exception,e:
                print_call_stack(logger)