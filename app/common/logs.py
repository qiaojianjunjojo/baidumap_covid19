#!/usr/bin/env python
# coding: utf-8
from flask import Flask,jsonify,request
import logging
from logging import FileHandler
# 安裝時間進行存檔
from logging.handlers import TimedRotatingFileHandler
from functools import wraps
import traceback
from datetime import date,datetime


class Logger():
    def __init__(self, app):
        self.app = app
        self.getInit()
        
    def getInit(self):
        formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(funcName)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    
        today = datetime.strftime(datetime.now(),'%Y%m%d')
        handler = TimedRotatingFileHandler(
            f"flask-{today}.log", when="D", interval=1, backupCount=7,
            encoding="UTF-8", delay=False, utc=True)
        # handler = logging.FileHandler('flask.log')
    
        self.app.logger.addHandler(handler)
        handler.setFormatter(formatter)

    def writeLog(self, detail = False):
        def writeLog1(func):
        # 保持引用的函數名字不發生變化
            @wraps(func)
            def log(*args,**kwargs):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    if detail:
                        self.app.logger.error(f"{func.__name__} :{traceback.format_exc()}")
                    else:
                        self.app.logger.error(f"{func.__name__} :{str(e)}")
            return log

        return writeLog1

# 日誌保存設定
# when=D： 表示按天进行切分
# interval=1： 每天都切分。 比如interval=2就表示两天切分一下。
# backupCount=15: 保留15天的日志
# encoding=UTF-8: 使用UTF-8的编码来写日志
# utc=True: 使用UTC+0的时间来记录 （一般docker镜像默认也是UTC+0）


# 日誌格式說明
# %(asctime)s 日志记载时间。即前面说的需要的时间，精确到毫秒。
# %(levelname)s 日志报警级别。后面会马上具体介绍。
# %(filename)s 触发日志记录的文件名。即出问题的程序代码段所在文件的文件名。
# %(funcName)s 触发日志记录的函数名。
# %(lineno)s 触发日志记录的代码行号。即引起报错的代码所在行的行号。
# %(message)s' 触发日志的具体信息。

