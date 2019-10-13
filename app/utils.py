# -*- coding:utf-8

from bs4 import BeautifulSoup
from datetime import datetime
import json
import uuid


def pretty_url(url_str):
    soup = BeautifulSoup(url_str,"html.parser")
    return soup.prettify()


def pretty_json(obj):
    return json.dumps(obj,indent=4)

def convert_time(times):
    time_stamp = float(times)
    return datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def generate_id():
    uid = str(uuid.uuid4())
    return uid.replace("-", "")