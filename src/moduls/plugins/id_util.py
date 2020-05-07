# encoding: utf-8

import re


def get_id(request: str):
    p = re.compile(r'(\d+)')
    m = p.search(request)
    return m.group(0)
