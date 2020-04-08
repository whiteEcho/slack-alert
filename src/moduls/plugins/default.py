# coding: utf-8

from mako.lookup import TemplateLookup
from slackbot.bot import default_reply

templates = TemplateLookup(directories=["plugins\\template"])


@default_reply()
def default_func(message):
    user_name = message.user["profile"]["display_name"]
    message.reply(default_response(user_name))


def default_response(user_name):
    my_template = templates.get_template("help.txt")

    return my_template.render(user_name=user_name)
