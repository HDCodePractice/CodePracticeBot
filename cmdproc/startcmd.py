#!/usr/bin/env python3

"""
支持 /start 和 /help
"""

import config
from telegram import Update
from telegram.ext import Dispatcher,CommandHandler,CallbackContext

def help():
    return """
    这是小怪兽们的作品集合，也是大家平时使用的Bot，欢迎大家使用。
    到今天，我竟然只有一个技能，一定是出了什么问题，希望有人能快快给我增加能力！

    /rewards 奖励大转盘 作者:hdcola
    /weather 查询天气 作者:hdcola
    /help 查看帮助 作者:hdcola

    开发者用命令：
    /info 将任意信息的json内容发给你 作者:hdcola

    管理员用命令：
    /admin 管理机器人 作者:hdcola
    """

def start(update : Update, context : CallbackContext):
    update.message.reply_text(help())

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["start","help"], start))
