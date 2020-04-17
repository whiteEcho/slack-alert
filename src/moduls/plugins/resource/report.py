# coding: utf-8

import json
import re


class Report:
    reporter = None
    date_of_occurred = None
    date_of_discovered = None
    summary = None
    detail = None

    def __init__(self, request: str):
        reporter, occurred, discovered, summary, detail = self.__convert(request)
        self.reporter = reporter
        self.date_of_occurred = self.__date(occurred)
        self.date_of_discovered = self.__date(discovered)
        self.summary = summary
        self.detail = detail

    @staticmethod
    def __convert(request):
        p = re.compile(
            r'''報告者.\s*(\S*)\s+
            発生日.\s*(\S*)\s+
            発覚日.\s*(\S*)\s+
            概要（300文字以内で簡潔に）.\s*(\S*)\s+
            詳細（1000文字以内で詳細に）.\s*([\S\n]*)(?:\s|`)*$''',
            re.X)
        m = p.search(request)
        return m.group(1, 2, 3, 4, 5)

    @staticmethod
    def __date(date_str):
        p = re.compile(r'(\d{4})[-\/年](\d{1,2})[-\/月](\d{1,2})日?')
        m = p.match(date_str)
        return '{}-{}-{}'.format(m.group(1), m.group(2), m.group(3)) if m else None


class ReportSerializer(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Report):
            return self.__to_dict(o)

        return super(ReportSerializer, self).default(o)

    @staticmethod
    def __to_dict(report: Report):
        return {
            'reporter': report.reporter,
            'date_of_occurred': report.date_of_occurred,
            'date_of_discovered': report.date_of_discovered,
            'summary': report.summary,
            'detail': report.detail
        }
