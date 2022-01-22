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
        "COOL! +1XP!\n爽！+1XP！", 
        "Good! +2XP!\n很好！+2XP！", 
        "POG! +3XP!\n很好！+2XP！", 
        "Sad... Nothing happens.\n好伤心...什么都没发生。", 
    ]
    update.message.reply_text("%s\nCreator/作者: Sichengthebest, Parker"%(randomPenalty))

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["rewards"], rewards))
    return get_command()

def get_command():
    return [BotCommand('rewards','Reward Spins // 奖励大转盘')]
