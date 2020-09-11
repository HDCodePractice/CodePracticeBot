#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
支持 /rewards 命令
"""


import config
from telegram import Update
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
import random

def help():
    return """
    这是小怪兽们的作品集合，也是大家平时使用的Bot，欢迎大家使用。
    到今天，我竟然只有一个技能，一定是出了什么问题，希望有人能快快给我增加能力！

    /help 查看帮助 作者:hdcola
    """

def rewards(update : Update, context : CallbackContext):
    rewards = [
        "爽了！直接加90XP。\nIt's cool! Directly to 90XP.",
        "你太幸运啦！不用加XP！\nYou're so lucky! No need to add XP!",
        "普普通通，只有40XP。\nOrdinary, only 40 XP.",
        "让神来决定你的命运吧！\nLet God decide your fate!"
    ]
    msg = random.choice(rewards)
    if msg == rewards[3]:
        xp = random.randrange(40,120)
        msg = "%s\n\n亲爱的%s,天神奖励你%sXP，离下一级你还有多远？"%(
            msg,
            update.effective_user.first_name,
            xp
        )
        msg = "%s\nDear %s, the gods have rewarded you with %sXP, how far are you from the next level?"%(
            msg,
            update.effective_user.first_name,
            xp
        )
    update.message.reply_text(msg)

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["rewards"], rewards))