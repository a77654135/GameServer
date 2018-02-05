# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     runGameserver
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import gameApplication
import threading
import signal
import os
import time

from config.settings import SERVER_PORT,DEBUG,APP_NAME
from common.ColorLogger import getUZWLogger

keepRunning = True
logger = None
serverApp = None


def startTornado():
    global serverApp
    global logger
    ioloopInst = tornado.ioloop.IOLoop.instance()
    serverApp = gameApplication.GameApplication()
    http_server =  tornado.httpserver.HTTPServer(serverApp)
    http_server.listen(SERVER_PORT)

    logger.info("start server successfully, listen on port: {}".format(SERVER_PORT))
    ioloopInst.start()


def stopTornado():
    global keepRunning
    global serverApp
    global logger

    logger.warning("shutdown................")
    lopper = tornado.ioloop.IOLoop.instance()
    lopper.add_callback(lambda x:x.stop(),lopper)
    serverApp.stopApplication()
    keepRunning = False
    logger.warning("shutdown success...")



def main():
    global logger
    global keepRunning
    os.system("cls")
    logger = getUZWLogger("DEBUG" if DEBUG else "ERROR")
    tornado.options.options.logging = "debug"

    logger.info("Starting {} ...".format(APP_NAME))

    t = threading.Thread(target=startTornado)
    t.start()
    signal.signal(signal.SIGINT,stopTornado)
    signal.signal(signal.SIGTERM,stopTornado)

    try:
        while keepRunning:
            time.sleep(1)
    except:
        pass

    t.join()
    logger.info("{} stopped,bye.".format(APP_NAME))



if __name__ == "__main__":
    main()