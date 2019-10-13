# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 16:22
# @Author  : zhuxiangtao
# @FileName: case_manager.py
# @Software: PyCharm

import traceback
from app import db
from app.models import TestCase
from pymysql import DatabaseError


class TestCaseManager(object):

    def add_test_case(self, name, creater, method, url, suite_id, uid, description = None,
                      params = None, headers = None, data = None, files = None, prescripts = None, postscripts = None):
        case = TestCase()
        case.name = name
        case.creater = creater
        case.method = method
        case.url = url
        case.suite_id = suite_id
        case.uid = uid
        if description: case.description = description
        if params: case.params = params
        if headers: case.headers = headers
        if data: case.data = data
        if files: case.files = files
        if prescripts: case.prescripts = prescripts
        if postscripts: case.postscripts = postscripts

        try:
            db.session.add(case)
            db.session.commit()
            return {"status": "success", "msg": "Add test case success"}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Add or edit test case fail", "reason": traceback.format_exc()}


    def edit_test_case(self, case_id, name, creater, method, url, description = None,
                      params = None, headers = None, data = None, files = None, prescripts = None, postscripts = None):
        case = TestCase.query.filter_by(id=case_id).first()
        return self.add_test_case(name, creater, method, url, case.suite_id, case.uid, description, params,
                           headers, data, files, prescripts, postscripts)


    def delete_test_case(self, case_id):
        case = TestCase.query.filter_by(id = case_id).first()
        case_info = self.get_test_case_info(case)
        try:
            db.session.delete(case)
            db.session.commit()
            return {"status": "success", "msg": "Delete test case success", "data": case_info}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Delete case suite fail", "data": case_info, "reason": traceback.format_exc()}


    def find_test_case(self, case_id = None):
        if case_id:
            case = TestCase.query.filter_by(id = case_id).first()
            case_info = self.get_test_case_info(case)
            return {"status": "success", "msg": "Query test case success", "data": case_info}
        else:
            case_info_list = list()
            cases = TestCase.query.all()
            for case in cases:
                case_info = self.get_test_case_info(case)
                case_info_list.append(case_info)
            return {"status": "fail", "msg": "Query test case fail", "data": case_info_list}

    def get_test_case_info(self, case_obj):
        case_info = dict()
        case_info["id"] = case_obj.id
        case_info["name"] = case_obj.name
        case_info["creater"] = case_obj.creater
        case_info["description"] = case_obj.description
        case_info["method"] = case_obj.method
        case_info["url"] = case_obj.url
        case_info["params"] = case_obj.params
        case_info["headers"] = case_obj.headers
        case_info["data"] = case_obj.data
        case_info["files"] = case_obj.files
        case_info["prescripts"] = case_obj.prescripts
        case_info["postscripts"] = case_obj.postscripts
        case_info["suite_id"] = case_obj.suite_id
        case_info["uid"] = case_obj.uid
        case_info["responses"] = case_obj.responses.all()
        return case_info