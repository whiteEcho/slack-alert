# coding: utf-8

import os

from slackbot.bot import default_reply

from .error_handler import error_handler


@default_reply()
@error_handler
def default_func(message):
    """
    デフォルトの返答をする。

    Parameters
    ----------
    message : Message
       Slackから送られてきたMessageObject

    Returns
    -------
    None
    """

    with open(os.path.join('plugins', 'template', 'help.txt'), encoding='utf-8') as f:
        message.reply(f.read())
