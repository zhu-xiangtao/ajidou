# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 12:51
# @Author  : zhuxiangtao
# @FileName: runner_manager.py
# @Software: PyCharm

from app import db
from app.models import TestRunner
from pymysql import DatabaseError


class TestRunnerManager(object):

    def add_test_runner(self, name, creater, description, cases):
        runner = TestRunner()
        runner.name = name
        runner.creater = creater
        runner.description = description
        for case in cases:
            runner.case_id = case.id
            try:
                db.session.add(runner)
                db.session.commit()
            except DatabaseError:
                db.session.rollback()





