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
    """
    ヒヤリハットを扱うAPIのクライアントクラス。
    """

    @staticmethod
    def get_list_func():
        """
        ヒヤリハットの一覧を取得する。

        Returns
        -------
        response: dict
            ヒヤリハット一覧取得APIのレスポンス
        """

        r = requests.get(hiyari_url)
        r.raise_for_status()
        response = r.json()
        return response

    @staticmethod
    def add_report_func(request: Report):
        """
        新規ヒヤリハット報告を登録する。

        Parameters
        ----------
        request: Report
           ヒヤリハット報告内容

        Returns
        -------
        response: dict
            ヒヤリハット報告登録結果
        """

        body = json.dumps(request, cls=report.ReportSerializer)
        response = requests.post(url=hiyari_url, json=body, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_detail_func(h_id):
        """
        ヒヤリハットの詳細を取得する。

        Parameters
        ------
        h_id: int
            ヒヤリハットID

        Returns
        -------
        response: dict
            ヒヤリハット詳細取得APIのレスポンス
        """

        r = requests.get(hiyari_by_id_url.format(h_id))
        r.raise_for_status()
        response = r.json()
        return response

    @staticmethod
    def update_detail_func(h_id, request: Report):
        """
        ヒヤリハットの詳細を修正する。

        Parameters
        ------
        h_id: int
            ヒヤリハットID
        request: Report
            ヒヤリハット報告内容

        Returns
        -------
        response: dict
            ヒヤリハット報告修正結果
        """

        body = json.dumps(request, cls=report.ReportSerializer)
        r = requests.put(url=hiyari_by_id_url.format(h_id), json=body, headers={'Content-Type': 'application/json'})
        r.raise_for_status()
        return r.json()


class IClient:
    """
    インシデントを扱うAPIのクライアントクラス。
    """

    @staticmethod
    def get_list_func():
        """
        インシデントの一覧を取得する。

        Returns
        -------
        response: dict
            インシデント一覧取得APIのレスポンス
        """

        r = requests.get(incident_url)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def add_report_func(file_name, file):
        """
        新規インシデント報告を登録する。

        Parameters
        ----------
        file_name: str
           インシデント報告ファイルのファイルパス
        file: byte
            インシデント報告ファイル

        Returns
        -------
        response: dict
            インシデント報告登録結果
        """

        r = requests.post(url=incident_url,
                          data=file,
                          headers={
                              'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                              'file_name': file_name}
                          )
        r.raise_for_status()
        return r.json()

    @staticmethod
    def get_detail_func(i_id):
        """
        インシデントの詳細を取得する。

        Parameters
        ------
        i_id: int
            インシデントID

        Returns
        -------
        response: dict
            インシデント詳細取得APIのレスポンス
        """

        r = requests.get(incident_by_id_url.format(i_id))
        r.raise_for_status()
        return r.headers['file_name'], r.content

    @staticmethod
    def update_detail_func(i_id, file_name, file):
        """
        インシデントの詳細を修正する。

        Parameters
        ------
        i_id: int
            インシデントID
        file_name: str
           インシデント報告ファイルのファイルパス
        file: byte
            インシデント報告ファイル

        Returns
        -------
        response: dict
            インシデント報告修正結果
        """

        r = requests.put(
            url=incident_by_id_url.format(i_id),
            data=file,
            headers={
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'file_name': file_name
            }
        )
        r.raise_for_status()
