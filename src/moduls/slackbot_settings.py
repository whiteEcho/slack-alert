# coding: utf-8

import os

# SlackのAPIを利用するためのトークン
API_TOKEN = os.environ["BOT_TOKEN"]

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "I don't understand you."

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']