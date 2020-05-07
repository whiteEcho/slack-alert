# coding: utf-8

import os

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
default_reply = None
with open(os.path.join('plugins', 'template', 'help.txt'), encoding='utf-8') as f:
    default_reply = f.read()
DEFAULT_REPLY = default_reply

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
