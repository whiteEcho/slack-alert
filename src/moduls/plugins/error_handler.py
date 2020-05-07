# coding: utf-8

import logging
import os

from mako.lookup import TemplateLookup
from requests.exceptions import RequestException

templates = TemplateLookup(directories=[os.path.join('plugins', 'template')])
template = templates.get_template('error.txt')

formatter = '%(levelname)s : %(asctime)s : %(message)s'
date_fmt = '%Y-%m-%d %H:%M:%S'
logging.getLogger('Error handler')
logging.basicConfig(format=formatter, datefmt=date_fmt)


class Error:
    code = '---'
    message = '---'
    fmt = '%s'

    def __init__(self, **kwargs):
        if 'response' in kwargs:
            response = kwargs['response']
            if response is not None:
                response = response.json()
                self.code = response['code']
                self.message = response['message']
                self.fmt = self.message + ' %s'
            else:
                pass
        elif 'code' in kwargs and 'message' in kwargs:
            self.code = kwargs['code']
            self.message = kwargs['message']
            self.fmt = self.message + '%s'
        else:
            pass


def __message_render(error: Error):
    return template.render(
        code=error.code,
        message=error.message,
    )


def error_handler(func):
    def wrapper(message):
        try:
            return func(message)
        except RequestException as e:
            response = e.response
            error = Error(response=response)
            logging.warning(error.fmt, e, exc_info=True)
            message.reply(__message_render(error))
        except Exception as e:
            error = Error(code='999', message='Internal Server Error.')
            logging.error(error.fmt, e, exc_info=True)
            message.reply(__message_render(error))

    return wrapper
