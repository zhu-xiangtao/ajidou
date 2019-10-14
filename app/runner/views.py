# -*- coding:utf-8 -*-

import traceback
from . import bp
from flask import render_template, request, jsonify, redirect, url_for
from app.models import TestSuite, TestCase, TestRunner, Project
from app.project_manager import ProjectManager
from app import db
from pymysql import DatabaseError

projectManager = ProjectManager()

@bp.route("/add_test_runner/<project_id>", methods = ["GET", "POST"])
def add_test_runner(project_id):
    if request.method == "POST":
        runner = TestRunner()
        name = request.form.get("runner_name")
        creater = request.form.get("runner_creater")
        description = request.form.get("runner_desc")
        suite_id = request.form.get("suite_id")
        all_case = TestCase.query.filter_by(suite_id = suite_id).all()
        print all_case
        for case_uid in set([case.uid for case in all_case]):
            print case_uid
            case = TestCase.query.filter_by(uid=case_uid).order_by(TestCase.create_time.desc()).first()
            runner.name = name
            runner.creater = creater
            runner.description = description
            runner.status = "waiting"
            runner.project_id = project_id
            runner.test_cases.append(case)

        try:
            db.session.add(runner)
            db.session.commit()
        except DatabaseError:
            db.session.rollback()
            return jsonify({"status": "fail", "msg": "Add test runner fail", "reason": traceback.format_exc()})
        return jsonify({"status": "success", "msg": "Add test runner success"})

    return render_template("add_test_runner.html", project_name = project_name, cases = cases)


@bp.route("/show_test_runner/<project_id>")
def show_test_runner(project_id):
    project = Project.query.filter_by(id = project_id).first()
    runners = project.runners
    return render_template("test_runner.html", runners = runners, project_name = project.name)


@bp.route("/runner_detail/<runner_id>")
def runner_detail(runner_id):
    runner = TestRunner.query.filter_by(id = runner_id).first()
    cases = runner.test_cases
    project_name = cases[0].suite.project.name
    project_id = cases[0].suite.project.id
    return render_template("test_runner_detail.html", project_name = project_name,
                           cases = cases, project_id = project_id, runner_name = runner.name)