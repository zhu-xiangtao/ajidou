# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 15:14
# @Author  : zhuxiangtao
# @FileName: suite_manager.py
# @Software: PyCharm

import traceback
from app import db
from app.models import TestSuite
from pymysql import DatabaseError


class TestSuiteManager(object):

    def add_test_suite(self, project_id, name, creater, description = None, prescripts = None, variables = None):
        suite = TestSuite()
        suite.project_id = project_id
        suite.name = name
        suite.creater = creater
        if description: suite.description = description
        if prescripts: suite.prescripts = prescripts
        if variables: suite.variables = variables

        try:
            db.session.add(suite)
            db.session.commit()
            return {"status": "success", "msg": "Add test suite success"}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Add test suite fail", "reason": traceback.format_exc()}


    def find_test_suite(self, suite_id = None):
        if suite_id:
            suite = TestSuite.query.filter_by(id = suite_id).first()
            suite_info = self.get_test_suite_info(suite)
            return {"status": "success", "msg": "Query test suite success", "data": suite_info}
        else:
            suite_info_list = list()
            suites = TestSuite.query.all()
            for suite in suites:
                suite_info = self.get_test_suite_info(suite)
                suite_info_list.append(suite_info)
            return {"status": "fail", "msg": "Query test suite fail", "data": suite_info_list}


    def delete_test_suite(self, suite_id):
        suite = TestSuite.query.filter_by(id = suite_id).first()
        suite_info = self.get_test_suite_info(suite)
        try:
            db.session.delete(suite)
            db.session.commit()
            return {"status": "success", "msg": "Delete test suite success", "data": suite_info}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Delete test suite fail", "data": suite_info, "reason": traceback.format_exc()}


    def get_test_suite_info(self, suite_obj):
        suite_info = dict()
        suite_info["name"] = suite_obj.name
        suite_info["creater"] = suite_obj.creater
        suite_info["project"] = suite_obj.project
        suite_info["description"] = suite_obj.description
        suite_info["prescripts"] = suite_obj.prescripts
        suite_info["variables"] = suite_obj.variables
        suite_info["cases"] = suite_obj.test_cases.all()
        return suite_info