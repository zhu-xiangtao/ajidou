# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 17:10
# @Author  : zhuxiangtao
# @FileName: __init__.py.py
# @Software: PyCharm

from flask import Blueprint

bp = Blueprint("project",__name__)
from . import views


