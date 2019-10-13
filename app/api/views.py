# -*- coding:utf-8 -*-

from . import bp
from flask import render_template,request,jsonify, redirect, url_for, flash
from app.utils import pretty_url, pretty_json, convert_time, generate_id
import json
from app.models import TestSuite, TestCase, Response, Project
from app.suite_manager import TestSuiteManager
from app.project_manager import ProjectManager
from app.case_manager import TestCaseManager
from app.clients import HttpSession
from app import db
from pymysql import DatabaseError
import traceback


suiteManager = TestSuiteManager()
projectManager = ProjectManager()
caseManager = TestCaseManager()


@bp.route("/add_test_suite", methods=["GET","POST"])
def add_test_suite():
    if request.method == "POST":
        name = request.form.get("suite_name")
        creater = request.form.get("suite_creater")
        description = request.form.get("suite_desc")
        prescripts = request.form.get("suite_pre_scripts")
        variables = request.form.get("suite_variables")
        project_id = request.form.get("project_id")
        content = suiteManager.add_test_suite(project_id, name, creater, description, prescripts, variables)
        return jsonify(content)

    project_info = projectManager.find_project()
    projects = project_info.get("data")
    return render_template("add_test_suite.html", projects = projects)


@bp.route("/delete_test_suite/<suite_id>")
def delete_test_suite(suite_id):
    content = suiteManager.delete_test_suite(suite_id)
    suite_info = content.get("data")
    if content.get("status") == "success":
        flash("Delete test suite success!")
    else:
        flash("Delete test suite fail")
    return redirect(url_for("project.detail", project_id = suite_info.get("project").id))


@bp.route("/add_test_case/<suite_id>", methods=["GET","POST"])
def add_test_case(suite_id):
    if request.method == "POST":
        name = request.form.get("case_name")
        creater = request.form.get("case_creater")
        description = request.form.get("case_desc")
        method = request.form.get("method", "get")
        url = request.form.get("url")
        params = request.form.get("params")
        headers = request.form.get("headers")
        data = request.form.get("data")
        files = request.form.get("files")
        prescripts = request.form.get("prescripts")
        postscripts = request.form.get("postscripts")

        content = caseManager.add_test_case(name, creater, method, url, suite_id, generate_id(),
                                            description, params, headers, data, files, prescripts, postscripts)
        return jsonify(content)
    suite_obj = TestSuite.query.filter_by(id = suite_id).first()
    suite_info = suiteManager.get_test_suite_info(suite_obj)
    return render_template("add_test_case.html", s_id = suite_id, case_info = None,
                           project = suite_info.get("project"), suite_name = suite_obj.name)


@bp.route("/edit_test_case/<case_id>", methods=["POST"])
def edit_test_case(case_id):
    name = request.form.get("case_name")
    creater = request.form.get("case_creater")
    description = request.form.get("case_desc")
    method = request.form.get("method", "get")
    url = request.form.get("url")
    params = request.form.get("params")
    headers = request.form.get("headers")
    data = request.form.get("data")
    files = request.form.get("files")
    prescripts = request.form.get("prescripts")
    postscripts = request.form.get("postscripts")
    content = caseManager.edit_test_case(case_id, name, creater, method, url,
                                      description, params, headers, data, files, prescripts, postscripts)
    return jsonify(content)


@bp.route("/test_case/<case_id>")
def show_test_case(case_id):
    case = TestCase.query.filter_by(id = case_id).first()
    case_info = caseManager.get_test_case_info(case)
    suite_id = case_info.get("suite_id")
    suite_obj = TestSuite.query.filter_by(id = suite_id).first()
    suite_info = suiteManager.get_test_suite_info(suite_obj)

    return render_template("add_test_case.html", s_id = suite_id, case_info = case_info,
                           project = suite_info.get("project"), suite_name = suite_obj.name)


@bp.route("/delete_test_case/<case_id>")
def delete_test_case(case_id):
    content = caseManager.delete_test_case(case_id)
    if content.get("status") == "success":
        flash("Delete test case sucess!")
    else:
        flash("Delete test case fail!")
    case_info = content.get("data")
    return redirect(url_for("api.show_test_cases", suite_id = case_info["suite_id"]))


@bp.route("/test_cases/<suite_id>")
def show_test_cases(suite_id):
    cases = list()
    suite = TestSuite.query.filter_by(id = suite_id).first()
    suite_info = suiteManager.get_test_suite_info(suite)
    all_case = suite_info.get("cases")
    for case_uid in set([case.uid for case in all_case]):
        case = TestCase.query.filter_by(uid = case_uid).order_by(TestCase.create_time.desc()).first()
        cases.append(case)

    return render_template("test_cases.html", cases = cases, project = suite_info.get("project"), suite = suite)


@bp.route("/history/<case_id>")
def history(case_id):
    case = TestCase.query.filter_by(id=case_id).first()
    suite = case.suite
    responses = case.responses.all()
    response_list = list()
    for response in responses:
        response_dict = dict()
        response_dict["id"] = response.id
        response_dict["case_name"] = case.name
        response_dict["status"] = response.status
        response_dict["start_time"] = convert_time(response.start_time)
        response_dict["end_time"] = convert_time(response.end_time)
        response_dict["case_id"] = response.case_id
        response_list.append(response_dict)
    return render_template("history.html", responses = response_list, case = case)


@bp.route("/delete_response/<response_id>")
def delete_response(response_id):
    response = Response.query.filter_by(id=response_id).first()
    c_id = response.test_case.id
    try:
        db.session.delete(response)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        flash("Delete response error!")
        return redirect(url_for("api.history", case_id = c_id))

    flash("Delete response success!")
    return redirect(url_for("api.history", case_id = c_id))


@bp.route("/run_single_interface",methods=["GET","POST"])
def run_single_interface():
    if request.method == "POST":
        rs = HttpSession()
        url = request.form.get("url")
        method = request.form.get("method", "get")
        params = request.form.get("params") and json.loads(request.form.get("params"))
        headers = request.form.get("headers") and json.loads(request.form.get("headers"))
        data = request.form.get("data")
        cookies = request.form.get("cookies")
        files = request.form.get("files")
        auth = request.form.get("auth")
        timeout = request.form.get("timeout")
        allow_redirects = request.form.get("allow_redirects")
        proxies = request.form.get("proxies")
        hooks = request.form.get("hooks")
        stream = request.form.get("stream")
        verify = request.form.get("verify")
        cert = request.form.get("cert")
        json_str = request.form.get("josn")

        resp = rs.request(url, method, params = params, data = data, headers = headers,
                   cookies = cookies, files = files, auth = auth, timeout = timeout,
                   allow_redirects = allow_redirects, proxies = proxies, hooks = hooks,
                   stream = stream, verify = verify, cert = cert, json = json_str)

        content_type = rs.request_meta.get("content_type")
        print rs.request_meta

        if content_type:
            if "application/json" in content_type:
                return jsonify({
                    "code": rs.request_meta.get("status_code"),
                    "response_headers": dict(resp.headers),
                    "cookies": dict(resp.cookies),
                    "response_content": resp.json(),
                    "status": rs.request_meta.get("status"),
                    "start_time": rs.request_meta.get("start_time"),
                    "end_time": rs.request_meta.get("end_time"),
                    "content_type": content_type,
                    "message": rs.request_meta.get("message"),
                })
            elif "text/html" in content_type:
                if resp.encoding == "ISO-8859-1":
                    resp.encoding = resp.apparent_encoding
                return jsonify({
                    "code": rs.request_meta.get("status_code"),
                    "response_headers": dict(resp.headers),
                    "cookies": dict(resp.cookies),
                    "response_content": pretty_url(resp.text),
                    "status": rs.request_meta.get("status"),
                    "start_time": rs.request_meta.get("start_time"),
                    "end_time": rs.request_meta.get("end_time"),
                    "content_type": content_type,
                    "message": rs.request_meta.get("message"),
                })
        return jsonify({
            "code": rs.request_meta.get("status_code"),
            "response_headers": dict(resp.headers),
            "cookies": dict(resp.cookies),
            "status": rs.request_meta.get("status"),
            "start_time": rs.request_meta.get("start_time"),
            "end_time": rs.request_meta.get("end_time"),
            "message": rs.request_meta.get("message"),
            "content_type": content_type,
        })

    return render_template("index.html")


@bp.route("/run_test_cases/<suite_id>")
def run_test_cases(suite_id):
    s_id = suite_id
    rs = HttpSession()
    cases = TestCase.query.filter_by(suite_id=s_id)
    if cases:
        for case in cases:
            url = case.url
            method = case.method
            params = case.params and json.loads(case.params)
            headers = case.headers and json.loads(case.headers)
            data = case.data
            cookies = case.cookies and json.loads(case.cookies)
            auth = case.auth
            timeout = case.timeout
            files = case.files
            allow_redirects = case.allow_redirects
            proxies = case.proxies
            hooks = case.hooks
            stream = case.stream
            verify = case.verify
            cert = case.cert
            json_str = case.json_str
            resp = rs.request(url, method, params = params, data = data, headers = headers,
                                      cookies = cookies, files = files, auth = auth, timeout = timeout,
                                      allow_redirects = allow_redirects, proxies = proxies, hooks = hooks,
                                      stream = stream, verify = verify, cert = cert, json = json_str)

            try:
                case.status = rs.request_meta.get("status")
                db.session.add(case)
                db.session.commit()
            except DatabaseError:
                db.session.rollback()
                return jsonify({"status": "error", "reason": traceback.format_exc(), "msg": "update test case error"})

            try:
                # update response to db
                response = Response()
                response.status_code = rs.request_meta.get("status_code")
                response.content_size = rs.request_meta.get("content_size")
                response.status = rs.request_meta.get("status")
                response.start_time = rs.request_meta.get("start_time")
                response.end_time = rs.request_meta.get("end_time")
                if resp.headers:
                    response.headers = pretty_json(dict(resp.headers))
                if resp.cookies:
                    response.cookies = pretty_json(dict(resp.cookies))
                content_type = rs.request_meta.get("content_type")
                response.content_type = content_type
                if content_type:
                    if "application/json" in content_type:
                        response.content = pretty_json(resp.json())
                    elif "text/html" in content_type:
                        if resp.encoding == "ISO-8859-1":
                            resp.encoding = resp.apparent_encoding
                        response.content = pretty_url(resp.text)

                response.error = rs.request_meta.get("message")
                response.case_id = case.id
                db.session.add(response)
                db.session.commit()
            except DatabaseError:
                db.session.rollback()
                return redirect(url_for("api.show_test_cases", suite_id = s_id))
        return redirect(url_for("api.show_test_cases", suite_id = s_id))
    return redirect(url_for("api.show_test_cases", suite_id = s_id))