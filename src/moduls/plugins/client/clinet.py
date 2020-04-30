# coding: utf-8

import json
import requests

from . import config
from ..resource import report
from ..resource.report import Report

hiyari_url = config.HOST + config.Url.HIYARI
hiyari_by_id_url = config.HOST + config.Url.HIYARI_BY_ID
incident_url = config.HOST + config.Url.INCIDENT
incident_by_id_url = config.HOST + config.Url.INCIDENT_BY_ID


class HClient:
    @staticmethod
    def get_list_func():
        r = requests.get(hiyari_url)
        response = r.json()
        return response

    @staticmethod
    def add_report_func(request: Report):
        body = json.dumps(request, cls=report.ReportSerializer)
        response = requests.post(url=hiyari_url, json=body, headers={'Content-Type': 'application/json'})
        return response.json()

    @staticmethod
    def get_detail_func(h_id):
        r = requests.get(hiyari_by_id_url.format(h_id))
        response = r.json()
        return response

    @staticmethod
    def update_detail_func(h_id, request: Report):
        body = json.dumps(request, cls=report.ReportSerializer)
        r = requests.put(url=hiyari_by_id_url.format(h_id), json=body, headers={'Content-Type': 'application/json'})
        return r.json()


class IClient:
    @staticmethod
    def get_list_func():
        return requests.get(incident_url).json()

    @staticmethod
    def add_report_func(file_name, file):
        r = requests.post(url=incident_url,
                          data=file,
                          headers={
                              'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                              'file_name': file_name}
                          )
        return r.json()

    @staticmethod
    def get_detail_func(i_id):
        r = requests.get(incident_by_id_url.format(i_id))
        return r.headers['file_name'], r.content

    @staticmethod
    def update_detail_func(i_id, file_name, file):
        requests.put(
            url=incident_by_id_url.format(i_id),
            data=file,
            headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'file_name': file_name
            }
        )
