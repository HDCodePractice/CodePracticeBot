#!/usr/bin/env python3

"""
在群里猜数字
"""

import random
from telegram.ext import Dispatcher,CommandHandler

n = random.randint(1,99)

def guessing(update, context):
    global n
    msg8 = ""
    gn = "猜一个0-100之间的数字。\nYou guessed a number from 0 - 100.\n\n "
    b = context.args[0]
    a = int(b)
    msg8 += gn
    if a == n :
        msg8 += "你猜对了！开始新的一轮猜测！\nAyyy You guessed it! Start a new round of guess!"
        n = random.randint(1,99)
    elif a > n :
        msg8 += "大了！重猜！It's big! Guess again!"
    elif a < n :
        msg8 += "小了！重猜！It's small! Guess again!"
    elif a != int :
        msg8 += "ur bad thats not a number"
    msg8 += "\n\nAuthorised By Noah <3\n作者：Noah"
    update.message.reply_text(msg8)

def add_dispatcher(dp:Dispatcher):
    guess_handler = CommandHandler('guess',guessing)
    dp.add_handler(guess_handler)