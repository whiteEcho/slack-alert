# coding: utf-8

from mako.lookup import TemplateLookup
from slackbot.bot import default_reply

templates = TemplateLookup(directories=["plugins\\template"])


@default_reply()
def default_func(message):
    message.reply(templates.get_template("help.txt").render())
