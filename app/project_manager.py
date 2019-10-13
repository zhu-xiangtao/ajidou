# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 14:48
# @Author  : zhuxiangtao
# @FileName: project_manager.py
# @Software: PyCharm

import traceback
from app import db
from app.models import Project
from pymysql import DatabaseError


class ProjectManager(object):

    def create_project(self, name, creater, description=None):
        project = Project()
        project.name = name
        project.creater = creater
        if description: project.description = description

        try:
            db.session.add(project)
            db.session.commit()
            return {"status": "success", "msg": "Create project success"}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Create project fail", "reason": traceback.format_exc()}


    def edit_project(self, project_id, name, creater, description):
        project = Project.query.filter_by(id = project_id).first()
        project.name = name
        project.creater = creater
        project.description = description

        try:
            db.session.add(project)
            db.session.commit()
            return {"status": "success", "msg": "Edit project success"}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Edit project fail", "reason": traceback.format_exc()}


    def delete_project(self, project_id):
        project = Project.query.filter_by(id = project_id).first()

        try:
            db.session.delete(project)
            db.session.commit()
            return {"status": "success", "msg": "Delete project success"}
        except DatabaseError:
            db.session.rollback()
            return {"status": "fail", "msg": "Delete project fail", "reason": traceback.format_exc()}


    def find_project(self, project_id = None):
        if project_id:
            project = Project.query.filter_by(id = project_id).first()
            project_info = self.get_project_info(project)
            return {"status": "success", "msg": "Query project success", "data": project_info}
        else:
            project_info_list = list()
            projects = Project.query.all()
            for project in projects:
                project_info = self.get_project_info(project)
                project_info_list.append(project_info)
            return {"status": "success", "msg": "Query project success", "data": project_info_list}


    def get_project_info(self, project_obj):
        project_info = dict()
        project_info["id"] = project_obj.id
        project_info["name"] = project_obj.name
        project_info["creater"] = project_obj.creater
        project_info["description"] = project_obj.description
        project_info["suites"] = project_obj.suites.all()
        return project_info





