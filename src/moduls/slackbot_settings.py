# coding: utf-8

import os
from mako.lookup import TemplateLookup


# SlackのAPIを利用するためのトークン
API_TOKEN = os.environ["BOT_TOKEN"]

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = TemplateLookup(directories='plugins\\template').get_template('help.txt')

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
