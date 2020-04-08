# coding: utf-8

from slackbot.bot import listen_to
from slackbot.bot import respond_to


@listen_to(".*:hiyari:.*")
def mention_func(message):
    message.reply(message_func(message.user["profile"]["display_name"]))


@respond_to(".*:hiyari:.*")
def mention_func(message):
    message.reply(message_func(message.user["profile"]["display_name"]))


def message_func(user_name):
    # TODO: ちゃんとメッセージ作る
    # TODO: 登録するのもやる
    return "ヒヤリハットですね！！"
