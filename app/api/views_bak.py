# -*- coding:utf-8 -*-

from . import bp
from flask import render_template,request,jsonify, redirect, url_for, flash
from app.utils import pretty_url, pretty_json, convert_time, generate_id
import json
from app.models import TestSuite, TestCase, Response, Project
from app.clients import HttpSession
from app import db
from pymysql import DatabaseError
import traceback


@bp.route("/add_test_suite", methods=["GET","POST"])
def add_test_suite():
    if request.method == "POST":
        suite = TestSuite()
        suite.name = request.form.get("suite_name")
        suite.creater = request.form.get("suite_creater")
        suite.description = request.form.get("suite_desc")
        suite.prescripts = request.form.get("suite_pre_scripts")
        suite.variables = request.form.get("suite_variables")
        suite.project_id = request.form.get("project")
        suite.status = "waiting"
        try:
            db.session.add(suite)
            db.session.commit()
            return jsonify({"msg":"insert test suite success","status":"success"})
        except DatabaseError:
            db.session.rollback()
            return jsonify({"status":"error", "msg": "insert test suite error", "reason":traceback.format_exc()})
    projects = Project.query.all()
    return render_template("add_test_suite.html", projects = projects)


@bp.route("/test_suites")
def show_test_suites():
    suites = TestSuite.query.all()
    return render_template("test_suites.html", suites=suites)


@bp.route("/delete_test_suite/<suite_id>")
def delete_test_suite(suite_id):
    suite = TestSuite.query.filter_by(id=suite_id).first()
    cases = suite.test_cases.all()
    try:
        for case in cases:
            responses = case.responses.all()
            for response in responses:
                db.session.delete(response)
                db.session.commit()

            db.session.delete(case)
            db.session.commit()
    except DatabaseError:
        db.session.rollback()
        return jsonify({"status": "error", "reason": traceback.format_exc(), "msg": "delete test suite error"})

    try:
        db.session.delete(suite)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        return jsonify({"status": "error", "reason": traceback.format_exc(), "msg": "delete test suite error"})

    flash("Delete test suite success!")
    return redirect(url_for("api.show_test_suites"))


@bp.route("/add_test_case/<suite_id>", methods=["GET","POST"])
def add_test_case(suite_id):
    if request.method == "POST":
        case = TestCase()
        case.name = request.form.get("case_name")
        case.creater = request.form.get("case_creater")
        case.description = request.form.get("case_desc")
        case.method = request.form.get("method", "get")
        case.url = request.form.get("url")

        case.params = request.form.get("params")
        case.headers = request.form.get("headers")
        case.data = request.form.get("data")
        case.files = request.form.get("files")
        case.prescripts = request.form.get("prescripts")
        case.postscripts = request.form.get("postscripts")
        case.status = "waiting"
        case.suite_id = suite_id
        case.uid = generate_id()

        try:
            db.session.add(case)
            db.session.commit()
            return jsonify({"msg": "add test case success", "status": "success"})
        except DatabaseError:
            db.session.rollback()
            return jsonify({"status": "error", "reason": traceback.format_exc(), "msg": "add test case error"})

    return render_template("add_test_case.html", s_id = suite_id)


@bp.route("/edit_test_case/<case_id>", methods=["POST"])
def edit_test_case(case_id):
    case = TestCase.query.filter_by(id = case_id).first()
    # case uuid
    case_uid = case.uid
    # suite id
    s_id = case.suite.id

    new_case = TestCase()
    new_case.name = case.name
    new_case.creater = case.creater
    new_case.description = case.description
    new_case.method = request.form.get("method", "get")
    new_case.url = request.form.get("url")

    new_case.params = request.form.get("params")
    new_case.headers = request.form.get("headers")
    new_case.data = request.form.get("data")
    new_case.files = request.form.get("files")
    new_case.prescripts = request.form.get("prescripts")
    new_case.postscripts = request.form.get("postscripts")

    new_case.suite_id = s_id
    new_case.uid = case_uid

    try:
        db.session.add(new_case)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
    return jsonify({"status": "success", "msg": "update test case success"})


@bp.route("/test_cases/<suite_id>")
def show_test_cases(suite_id):
    cases = list()
    suite = TestSuite.query.filter_by(id = suite_id).first()
    project = suite.project
    all_case = suite.test_cases
    for case_uid in set([case.uid for case in all_case]):
        case = TestCase.query.filter_by(uid = case_uid).order_by(TestCase.create_time.desc()).first()
        cases.append(case)

    return render_template("test_cases.html", cases = cases, project = project, suite = suite)


@bp.route("/test_case/<case_id>")
def show_test_case(case_id):
    case = TestCase.query.filter_by(id=case_id).first()
    response_dict = {"request":{}}
    response_dict["request"]["method"] = case.method
    response_dict["request"]["url"] = case.url
    response_dict["request"]["headers"] = case.headers and json.loads(case.headers.replace("'",'"'))
    response_dict["request"]["params"] = case.params and json.loads(case.params.replace("'","'"))
    response_dict["request"]["data"] = case.data
    response_dict["request"]["prescripts"] = case.prescripts
    response_dict["request"]["postscripts"] = case.postscripts

    return render_template("test_case.html", response = response_dict, case_id = case.id, suite_id = case.suite.id)


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


@bp.route("/delete_test_case/<case_id>")
def delete_test_case(case_id):
    case = TestCase.query.filter_by(id=case_id).first()
    s_id = case.suite.id
    responses = case.responses.all()
    try:
        for response in responses:
            db.session.delete(response)
            db.session.commit()
    except DatabaseError:
        db.session.rollback()
        flash("Delete case error!")
        return redirect(url_for("api.show_test_cases", suite_id = s_id))

    try:
        db.session.delete(case)
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        flash("Delete case error!")
        return redirect(url_for("api.show_test_cases", suite_id = s_id))

    flash("Delete case success!")
    return redirect(url_for("api.show_test_cases", suite_id = s_id))


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