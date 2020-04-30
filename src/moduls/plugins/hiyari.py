# coding: utf-8

import re

from slackbot.bot import listen_to
from slackbot.bot import respond_to
from mako.lookup import TemplateLookup

from .client.clinet import HClient as client
from .resource.report import Report

templates = TemplateLookup(directories=["plugins\\template\\hiyari"])


@listen_to(matchstr=r'[ひやり|ヒヤリ]+.*一覧+', flags=re.S)
@respond_to(matchstr=r'[ひやり|ヒヤリ]+.*一覧+', flags=re.S)
def get_list_func(message):
    template = templates.get_template("list.txt")
    elms = client.get_list_func()['response']
    message.reply(template.render(elms=elms))


@listen_to(matchstr=r'.*【ヒヤリハット報告】.*(?:報告者).*', flags=re.S)
@respond_to(matchstr=r'.*【ヒヤリハット報告】.*(?:報告者).*', flags=re.S)
def add_report_func(message):
    report: Report = Report(message.body['text'])
    response = client.add_report_func(request=report)
    template = templates.get_template('report.txt')
    response['user_name'] = message.user["profile"]["display_name"]
    message.reply(template.render(**response))


@listen_to(matchstr=r'(?<!【)[ヒヤリ|ひやり].*報告(?!】)(?!書き方)')
@respond_to(matchstr=r'(?<!【)[ヒヤリ|ひやり].*報告(?!】)(?!書き方)')
def report_help_func(message):
    template = templates.get_template('hiyari_report.txt')
    message.reply(template.render(user_name=message.user["profile"]["display_name"]))


@listen_to(r'\d+.*[ひやり|ヒヤリ].*詳細.*')
@respond_to(r'\d+.*[ひやり|ヒヤリ].*詳細.*')
def get_detail_func(message):
    h_id = __get_id(message.body['text'])
    response = client.get_detail_func(h_id)
    template = templates.get_template('detail.txt')
    response['user_name'] = message.user["profile"]["display_name"]
    message.reply(template.render(**response))


@listen_to(r'\d+.*[ひやり|ヒヤリ].*修正.*(?!:ID.*)')
@respond_to(r'\d+.*[ひやり|ヒヤリ].*修正.*(?!:ID.*)')
def get_edit_func(message):
    h_id = __get_id(message.body['text'])
    response = client.get_detail_func(h_id)
    template = templates.get_template('edit.txt')
    message.reply(template.render(**response))


@listen_to(r'.*【ヒヤリハットの修正】.*(?:ID.*)', flags=re.S)
@respond_to(r'.*【ヒヤリハットの修正】.*(?:ID.*)', flags=re.S)
def update_func(message):
    h_id = __get_id(message.body['text'])
    report: Report = Report(message.body['text'])
    response = client.update_detail_func(h_id, request=report)
    template = templates.get_template('edit_result.txt')
    response['user_name'] = message.user["profile"]["display_name"]
    message.reply(template.render(**response))


def __get_id(request: str):
    p = re.compile(r'(\d+)')
    m = p.search(request)
    return m.group(0)
