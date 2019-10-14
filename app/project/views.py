# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 17:10
# @Author  : zhuxiangtao
# @FileName: views.py
# @Software: PyCharm

from . import bp
from flask import render_template,request,redirect,url_for,jsonify, flash
from app.models import Project
from app.project_manager import ProjectManager
from app.suite_manager import TestSuiteManager


projectManager = ProjectManager()


@bp.route("/")
def index():
    return redirect(url_for('project.show_project'))


@bp.route("/create_project", methods=["GET","POST"])
def create_project():
    if request.method == "POST":
        name = request.form.get("project_name")
        creater = request.form.get("project_creater")
        description = request.form.get("project_desc")
        content = projectManager.create_project(name, creater, description)
        return jsonify(content)

    return render_template("create_project.html")


@bp.route("/project_list")
def show_project():
    content = projectManager.find_project()
    projects = content.get("data")
    return render_template("project_list.html", projects = projects)


@bp.route("/delete_project/<project_id>")
def delete_project(project_id):
    content = projectManager.delete_project(project_id)
    if content.get("status") == "success":
        flash("Delete project success!")
    elif content.get("status") == "fail":
        flash("Delete project fail!")

    return redirect(url_for("project.show_project"))


@bp.route("/edit_project/<project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    p_id = project_id
    if request.method == "POST":
        name = request.form.get("project_name")
        creater = request.form.get("project_creater")
        description = request.form.get("project_desc")
        content = projectManager.edit_project(p_id, name, creater, description)
        return jsonify(content)

    project_info = projectManager.find_project(project_id = p_id)
    return render_template("edit_project.html", project=project_info.get("data"))


@bp.route("/test_suites/<project_id>")
def detail(project_id):
    content = projectManager.find_project(project_id)
    project_info = content.get("data")
    suites = project_info.get("suites")
    project_name = project_info.get("name")
    project_id = project_info.get("id")

    return render_template("test_suites.html", suites = suites, project_name = project_name, project_id = project_id)













