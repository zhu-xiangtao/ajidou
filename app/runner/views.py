# -*- coding:utf-8 -*-

from . import bp
from flask import render_template


@bp.route("/add_test_runner")
def add_test_runner():
    return render_template("add_test_runner.html")
