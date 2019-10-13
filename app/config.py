# -*- coding:utf-8 -*-

import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.urandom(24)
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True