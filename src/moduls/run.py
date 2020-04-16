# coding: utf-8

from slackbot.bot import Bot
from datetime import datetime


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('[{}] start slackbot'.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))

    main()
