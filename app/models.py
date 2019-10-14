# -*- coding: utf-8 -*-
# @Time    : 2019/6/6 17:00
# @Author  : zhuxiangtao
# @FileName: models.py
# @Software: PyCharm

from app import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    creater = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(360))

    suites = db.relationship("TestSuite", backref="project", lazy="dynamic")
    runners = db.relationship("TestRunner", backref="project", lazy="dynamic")

    def __repr__(self):
        return "Project: {}".format(self.name)


class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120),nullable = False)
    creater = db.Column(db.String(120),nullable = False)
    description = db.Column(db.String(360))
    prescripts = db.Column(db.Text)
    variables = db.Column(db.String(120))
    history = db.Column(db.Text)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    status = db.Column(db.String(120))

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    test_cases = db.relationship("TestCase", backref="suite", lazy="dynamic")

    def __repr__(self):
        return "TestSuite: {}".format(self.name)


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    creater = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(360))

    method = db.Column(db.String(120), nullable = False)
    url = db.Column(db.String(360), nullable = False)
    params = db.Column(db.Text)
    data = db.Column(db.Text)
    headers = db.Column(db.Text)
    cookies = db.Column(db.Text)
    auth = db.Column(db.Text)
    allow_redirects = db.Column(db.Boolean, default = True)
    proxies = db.Column(db.Text)
    hooks = db.Column(db.Text)
    stream = db.Column(db.Boolean, default = False)
    timeout = db.Column(db.Float)
    verify = db.Column(db.Boolean, default = True)
    cert = db.Column(db.Text)
    json_str = db.Column(db.Text)
    files = db.Column(db.Text)
    prescripts = db.Column(db.Text)
    postscripts = db.Column(db.Text)
    status = db.Column(db.String(8))
    uid = db.Column(db.String(32), nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)

    suite_id = db.Column(db.Integer, db.ForeignKey("test_suite.id"))
    responses = db.relationship("Response", backref="test_case", lazy="dynamic")

    def __repr__(self):
        return "TestCase: {}".format(self.name)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer)
    error = db.Column(db.Text)
    headers = db.Column(db.Text)
    cookies = db.Column(db.Text)
    content = db.Column(db.Text)
    content_type = db.Column(db.String(32))
    content_size = db.Column(db.Integer)
    start_time = db.Column(db.String(120))
    end_time = db.Column(db.String(120))
    status = db.Column(db.String(120))

    case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"))

    def __repr__(self):
        return "Response: {}".format(self.status_code)


runner_case = db.Table("runner_case",
                       db.Column("runner_id", db.Integer, db.ForeignKey('test_runner.id'),primary_key=True),
                       db.Column("csae_id", db.Integer, db.ForeignKey('test_case.id'),primary_key=True),
                       )


class TestRunner(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    creater = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(360))
    status = db.Column(db.String(8))

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    test_cases = db.relationship("TestCase", secondary = runner_case, backref=db.backref('runners'))









