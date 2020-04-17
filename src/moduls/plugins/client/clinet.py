# coding: utf-8

import json
import requests

from . import config
from ..resource import report
from ..resource.report import Report

hiyari_url = config.HOST + config.Url.HIYARI
hiyari_by_id_url = config.HOST + config.Url.HIYARI_BY_ID


def get_list_func():
    r = requests.get(hiyari_url)
    response = r.json()
    return response


def add_report_func(request: Report):
    body = json.dumps(request, cls=report.ReportSerializer)
    response = requests.post(url=hiyari_url, json=body, headers={'Content-Type': 'application/json'})
    return response.json()


def get_detail_func(h_id):
    r = requests.get(hiyari_by_id_url.format(h_id))
    response = r.json()
    return response


def update_detail_func(h_id, request: Report):
    body = json.dumps(request, cls=report.ReportSerializer)
    r = requests.put(url=hiyari_by_id_url.format(h_id), json=body, headers={'Content-Type': 'application/json'})
    return r.json()
