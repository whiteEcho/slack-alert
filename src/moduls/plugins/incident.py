# coding: utf-8

import os
import codecs
import re
import requests
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from slacker import Slacker
from mako.lookup import TemplateLookup
import slackbot_settings
from .client.clinet import IClient as client


templates = TemplateLookup(directories=[os.path.join('plugins', 'template', 'incident')])


@respond_to(r'(?:事故|インシデント)(?=.*(?:一覧))')
def list_func(message):
    template = templates.get_template('list.txt')
    elms = client.get_list_func()['response']
    message.reply(template.render(elms=elms))


@respond_to(r'(?:事故|インシデント)(?=.*(?:新規|登録))')
def add_func(message):
    if 'files' in message.body:
        if __is_excel_file(message.body['files'][0]['mimetype']):
            url = message.body['files'][0]['url_private_download']
            file_name = message.body['files'][0]['name']
            template = templates.get_template('report.txt')
            file = __file_download(url)
            i_id = client.add_report_func(file_name, file)['id']
            message.reply(
                template.render(
                    user_name=message.user["profile"]["display_name"],
                    id=i_id))
        else:
            message.reply('エクセルじゃないよ')

    else:
        slacker = Slacker(slackbot_settings.API_TOKEN)
        template = templates.get_template('default_new.txt')
        file = open(os.path.join('plugins', 'template', 'incident', 'CSM_Guideline_app_C.xlsx'), 'rb')
        slacker.files.upload(
            file_=file,
            channels=message.body['channel'],
            initial_comment=template.render(user_name=message.user["profile"]["display_name"]))


@respond_to(r'(?:事故|インシデント)(?=.*(?:\d+))')
def detail_func(message):
    i_id = __get_id(message.body['text'])

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
        slacker = Slacker(slackbot_settings.API_TOKEN)
        file_name, file = client.get_detail_func(i_id)
        template = templates.get_template('detail.txt')
        slacker.files.upload(
            file,
            channels=message.body['channel'],
            initial_comment=template.render(id=i_id),
            filename=file_name,
            filetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def __is_excel_file(mime_type):
    return mime_type \
           in ['application/vnd.ms-excel',
               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']


def __file_download(url):
    r = requests.get(url,
                     allow_redirects=True,
                     headers={
                         'Authorization': 'Bearer {}'.format(slackbot_settings.API_TOKEN)
                     },
                     stream=True)
    return r.content


def __get_id(request: str):
    p = re.compile(r'(\d+)')
    m = p.search(request)
    return m.group(0)
