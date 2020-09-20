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

    /weather - 查询天气 
    /rewards - 奖励大转盘 作者:Sichengthebest
    /penalties - 处罚大转盘 作者:Sichengthebest
    /help - 查看帮助

    开发者用命令：
    /info 将任意信息的json内容发给你

    管理员用命令：
    /admin 管理机器人
    """

def help_city():
    return """
    这是小怪兽们为City群所完成的作品集合，也是大家平时使用的Bot，欢迎大家使用。

    /weather - 查询天气 
    /rewards - 奖励大转盘 作者:Sichengthebest
    /penalties - 处罚大转盘 作者:Sichengthebest
    /help - 查看帮助
    """

def start(update : Update, context : CallbackContext):
    update.message.reply_text(help())

def start_city(update : Update, context : CallbackContext):
    update.message.reply_text(help_city())

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["start","help"], start))

def add_dispather_city(dp: Dispatcher):
    dp.add_handler(CommandHandler(["start","help"], start_city))