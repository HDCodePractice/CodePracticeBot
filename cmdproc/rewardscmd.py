#!/usr/bin/env python3

"""
支持 /rewards 命令
"""

import config
from telegram import Update,BotCommand
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
import random

def rewards(update : Update, context : CallbackContext):
    rewards = [
        "COOL! +90XP!\n爽！+90XP！", 
        "Good! +40XP!\n很好！+40XP！", 
        "Sad... Nothing happens.\n好伤心...什么都没发生。", 
        "Let BOTGOD decide your fate!\n让BOTGOD决定您的命运吧！"
    ]
    randomPenalty = random.choice(rewards)
    randomInt = random.randint(50,150)
    if randomPenalty == rewards[3]:
        update.message.reply_text("%s\nDear %s, BOTGOD has decided give you %sXP, keep up the good work!\n亲爱的%s，BOTGOD已决定奖励您%s XP。继续加油！\nCreator/作者: Sichengthebest"%(
            randomPenalty,
            update.message.from_user.first_name,
            randomInt,
            update.message.from_user.first_name,
            randomInt))
    else:
        update.message.reply_text("%s\nCreator/作者: Sichengthebest"%(randomPenalty))

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["rewards"], rewards))
    return get_command()

def get_command():
    return [BotCommand('rewards','领取奖励')]