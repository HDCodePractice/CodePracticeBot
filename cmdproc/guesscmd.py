#!/usr/bin/env python3

"""
在群里猜数字
"""

import random
from telegram import Update,User
from telegram.ext import Dispatcher,CommandHandler,CallbackContext

n = random.randint(1,99)
m = {}

def help()->str:
    msg =  """
猜一个0-100之间的数字。You guessed a number from 0 - 100.
/gess 查看现在的状态和获取帮助。Check your current status and get help.
/gess number 输入number猜数字，看谁用的次数最少。Enter number and see who uses it the least often.

"""
    for key in m.keys():
        msg += f"{m[key][0]} : {m[key][1]} \n"
    msg += "\nAuthorised By Noah <3\n作者：Noah"
    return msg


def guessing(update : Update, context : CallbackContext):
    global n,m
    msg = ""
    user : User = update.effective_user

    if len(context.args) == 0:
        update.message.reply_text(help())
        return
    count = 0

    if user.id in m.keys():
        count = m[user.id][1]
    
    count +=1
    m[user.id] = [user.first_name,count]

    a = int(context.args[0])
    if a == n :
        count -=1
        m[user.id] = [user.first_name,count]
        msg += f"猜对了！{user.first_name}用了{count}开始新的一轮猜测！\nAyyy You guessed it! Start a new round of guess!\n\n"
        for key in m.keys():
            msg += f"{m[key][0]} : {m[key][1]} \n"
        m = {}
        n = random.randint(1,99)
    elif a > n :
        msg += f"猜大了！{user.first_name}用了{count}次！快重猜！It's big! Guess again!"
    elif a < n :
        msg += f"猜小了！{user.first_name}用了{count}次！重猜！It's small! Guess again!"
    elif a != int :
        msg += "ur bad thats not a number"
    msg += "\nAuthorised By Noah <3\n作者：Noah"
    update.message.reply_text(msg)

def add_dispatcher(dp:Dispatcher):
    guess_handler = CommandHandler('guess',guessing)
    dp.add_handler(guess_handler)