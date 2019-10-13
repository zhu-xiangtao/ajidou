# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 16:15
# @Author  : zhuxiangtao
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint("runner",__name__)
from . import views