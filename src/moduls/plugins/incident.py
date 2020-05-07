# coding: utf-8

import os
import re

import requests
from slackbot import settings
from mako.lookup import TemplateLookup
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from slacker import Slacker

from .client.clinet import IClient as client
from .error_handler import error_handler
from .id_util import get_id

templates = TemplateLookup(directories=[os.path.join('plugins', 'template', 'incident')])


@listen_to(r'(?:事故|インシデント)(?=.*(?:一覧))', flags=re.S)
@respond_to(r'(?:事故|インシデント)(?=.*(?:一覧))', flags=re.S)
@error_handler
def list_func(message):
    """
    登録済みの事故報告の一覧を返答する。

    Parameters
    ----------
    message : Message
       Slackから送られてきたMessageObject
    """

    template = templates.get_template('list.txt')
    elms = client.get_list_func()['response']
    message.reply(template.render(elms=elms))


@listen_to(r'(?:事故|インシデント)(?=.*(?:新規|登録))', flags=re.S)
@respond_to(r'(?:事故|インシデント)(?=.*(?:新規|登録))', flags=re.S)
@error_handler
def add_func(message):
    """
    新規事故の報告を受け付ける。
    ファイル添付がある場合は新規登録。
    ファイル添付がない場合は報告用フォーマットを返答する。

    Parameters
    ----------
    message : Message
       Slackから送られてきたMessageObject
    """

    if 'files' in message.body:
        if __is_excel_file(message.body['files'][0]['mimetype']):
            url = message.body['files'][0]['url_private_download']
            file_name = message.body['files'][0]['name']
            template = templates.get_template('report.txt')
            file = __file_download(url)
            response = client.add_report_func(file_name, file)
            i_id = response['id']
            message.reply(
                template.render(
                    user_name=message.user["profile"]["display_name"],
                    id=i_id))
        else:
            message.reply('エクセルじゃないよ')

    else:
        slacker = Slacker(settings.API_TOKEN)
        template = templates.get_template('default_new.txt')
        file = open(os.path.join('plugins', 'template', 'incident', 'CSM_Guideline_app_C.xlsx'), 'rb')
        slacker.files.upload(
            file_=file,
            channels=message.body['channel'],
            initial_comment=template.render(user_name=message.user["profile"]["display_name"]))


@listen_to(r'(?:事故|インシデント)(?=.*(?:\d+))', flags=re.S)
@respond_to(r'(?:事故|インシデント)(?=.*(?:\d+))', flags=re.S)
@error_handler
def detail_func(message):
    """
    登録済み事故報告の詳細を扱う。
    ファイル添付がある場合は事故報告の修正。
    ファイル添付がない場合は事故情報の詳細を表示する。

    Parameters
    ----------
    message : Message
       Slackから送られてきたMessageObject
    """

    i_id = get_id(message.body['text'])

    if 'files' in message.body:
        if __is_excel_file(message.body['files'][0]['mimetype']):
            url = message.body['files'][0]['url_private_download']
            file_name = message.body['files'][0]['name']
            template = templates.get_template('edit.txt')
            file = __file_download(url)

            client.update_detail_func(i_id, file_name, file)
            message.reply(
                template.render(
                    user_name=message.user["profile"]["display_name"],
                    id=i_id))
    else:
        slacker = Slacker(settings.API_TOKEN)
        file_name, file = client.get_detail_func(i_id)
        template = templates.get_template('detail.txt')
        slacker.files.upload(
            file,
            channels=message.body['channel'],
            initial_comment=template.render(id=i_id),
            filename=file_name,
            filetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def __is_excel_file(mime_type):
    """
    パラメータのMimeTypeがエクセルのものか判定する。

    Parameters
    ----------
    mime_type: str
        添付されたファイルのMimeType

    Returns
    -------
    is_excel_file: bool
        True: エクセルファイル, False: エクセル以外
    """

    return mime_type \
           in ['application/vnd.ms-excel',
               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']


def __file_download(url):
    """
    添付されたファイルをダウンロードする。

    Parameters
    ----------
    url: str
       Messageで連携されたプライベートダウンロードURL

    Returns
    -------
    file: byte
        ファイルデータ
    """

    r = requests.get(url,
                     allow_redirects=True,
                     headers={
                         'Authorization': 'Bearer {}'.format(settings.API_TOKEN)},
                     stream=True)
    return r.content
