#!/usr/bin/env python3

import config
from telegram import Update,BotCommand
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
from json import dumps,loads


def info(update : Update, context : CallbackContext):
    u = str(update)
    u = dumps(eval(u),indent=2)
    context.bot.send_message(update.effective_user.id,text=u)

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["info"], info))
    return [BotCommand('info','查看消息的信息数据')]