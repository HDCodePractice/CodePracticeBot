#!/usr/bin/env python3

"""
在群里猜数字
"""

import random
from telegram import Update,User
from telegram.ext import Dispatcher,CommandHandler,CallbackContext

# 存储每个chat有不同的随机数{chatid:number}
n = {}
# 每个chat里每个人猜测的次数{chatid:{userid:[first_name,count]}}
m = {}
# 每个chat里猜中者的次数{chatid:{userid:[first_name,count]}}
t = {}

def gettop(chatid)->str:
    msg = ""
    if len(m[chatid]) > 0 :
        for key in m[chatid].keys():
            msg += f"{m[chatid][key][0]} 本轮猜了 {m[chatid][key][1]} 次\n"
    msg += "\n"
    if len(t[chatid]) > 0:
        for key in t[chatid].keys():
            msg += f"{t[chatid][key][0]} 过去猜中 {t[chatid][key][1]} 次\n"
    return msg

def help(chatid)->str:
    msg =  """
猜一个0-100之间的数字。You guessed a number from 0 - 100.
/guess 查看现在的状态和获取帮助。Check your current status and get help.
/guess *your number here* 输入数字，看谁用的次数最少。Enter number and see who uses it the least often.
Creator: hdcola, Sichengthebest
作者：hdcola, Sichengthebest
"""

    msg += gettop(chatid) + "\nAuthorised By Noah <3\n作者：Noah"
    return msg


def guessing(update : Update, context : CallbackContext):
    global n,m
    msg = ""
    user : User = update.effective_user
    chatid = update.effective_chat.id
    
    # 如果这个chat没有出现过，就增加它
    if not (chatid in m) :
        m[chatid]={}
    if not (chatid in n):
        n[chatid]=random.randint(1,99)
    if not (chatid in t):
        t[chatid]={}

    if len(context.args) == 0:
        update.message.reply_text(help(chatid))
        return
    count = 0

    b = context.args[0]
    if not b.isdigit():
        tcount += 1
        msg = "糟糕，那不是一个数字！ur bad thats not a number!"
        update.message.reply_text(msg)
        return
    
    if user.id in m[chatid].keys():
        count = m[chatid][user.id][1]
    count +=1
    m[chatid][user.id] = [user.first_name,count]

    a = int(b)
    if a == n[chatid] :
        m[chatid][user.id] = [user.first_name,count]
        msg += f"猜对了！{user.first_name}用了{count}次！又开始新的一轮猜测！\nAyyy You guessed it! Start a new round of guess!\n\n"
        for key in m[chatid].keys():
            msg += f"{m[chatid][key][0]} : {m[chatid][key][1]} \n"
        m[chatid] = {}
        tcount = 0
        if user.id in t[chatid].keys():
            tcount = t[chatid][user.id][1]
        tcount += 1
        t[chatid][user.id]=[user.first_name,tcount]
        n[chatid] = random.randint(1,99)
    elif a > n[chatid] :
        msg += f"{user.first_name}猜大了！快重猜！It's big! Guess again!"
    elif a < n[chatid] :
        msg += f"{user.first_name}猜小了！快重猜！It's small! Guess again!"
    msg += "\n\n" + gettop(chatid)
    msg += "\nAuthorised By Noah <3\n作者：Noah"
    update.message.reply_text(msg)

def add_dispatcher(dp:Dispatcher):
    guess_handler = CommandHandler('guess',guessing)
    dp.add_handler(guess_handler)
