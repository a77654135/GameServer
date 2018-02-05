# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Gameglobal
   Author :       talus
   date：          2018/2/5 0005
   Description :
-------------------------------------------------

"""
__author__ = 'talus'


from config import ErrorCodeConf
from common.ExceptCallStack import print_call_stack
from common.ColorLogger import getUZWLogger

logger = getUZWLogger()

class GameException(BaseException):
    def __init__(self,errorCode,errorMessage):
        BaseException.__init__(self)
        self.errorCode = errorCode
        self.errorMessage = errorMessage

    def __str__(self):
        return "GameException [ errorCode: {} errorMessage: {} ]".format(self.errorCode,self.errorMessage)

    def __unicode__(self):
        return "GameException [ errorCode: {} errorMessage: {} ]".format(self.errorCode,self.errorMessage)

from main import requestLogical

def parseArgument(argument):
    """
    把参数转换成字典
    :param argument:
    :return:
    """
    obj = {}
    for k in argument:
        v = argument[k]
        if isinstance(v, str):
            obj[k] = v
        elif isinstance(v, list):
            if len(v) == 1:
                obj[k] = v[0]
            elif len(v) > 1:
                obj[k] = v[:]
        else:
            obj[k] = v
    return obj


def processHandler(handler,arguments):
    """
    逻辑处理
    :param handler:
    :return:
    """

    if arguments.has_key("cmd"):
        cmd = arguments["cmd"]
    else:
        raise GameException(ErrorCodeConf.E_REQUEST_HEADER_ERROR, r"need 'cmd' argument")

    #如果不是login，需要传token
    if cmd != "login":
        if not arguments.has_key("token"):
            raise GameException(ErrorCodeConf.E_TOKEN_LOST,r"need 'token' argument ")

    try:
        methodFunc = getattr(requestLogical, "parseRequest_{}".format(cmd))
    except AttributeError,e:
        raise GameException(ErrorCodeConf.E_REQUEST_NOT_EXIST,"request not exist.")

    response = methodFunc(handler,arguments)
    return response




def process(handler):
    """
    错误处理
    :param handler:
    :return:
    """

    #解析参数
    arguments = parseArgument(handler.request.query_arguments)

    try:
        errorCode = 0
        errorMessage = ""
        res = processHandler(handler,arguments)
    except GameException,e:
        errorCode = e.errorCode
        errorMessage = e.message
        res = {}
    except Exception,e:
        errorCode = ErrorCodeConf.E_SERVER_ERROR
        errorMessage = "server_error"
        res = {}
        print_call_stack(logger)

    obj = {
        "error":errorCode,
        "msg":errorMessage,
        "cmd": arguments.get("cmd",""),
        "serial": arguments.get("serial",0),
        #type类型 0请求  1响应   2广播
        "type": 1
    }
    for k in res:
        obj[k] = res

    return obj