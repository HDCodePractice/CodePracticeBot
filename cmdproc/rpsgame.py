#!/usr/bin/env python3

"""
支持 /startkill
"""

import config
from telegram import Update,User,InlineKeyboardMarkup,InlineKeyboardButton,Chat
from telegram.ext import Dispatcher,CommandHandler,CallbackContext

# GameMember 每个群只有一个游戏{chatid{}}
gm = {}

def help(user):
    return f"""
由 {user} 发起了一局石头剪刀布的游戏，点击按钮加入游戏。
A game of rock-paper-scissors was started by {user}, click the button to join the game.

群玩规则：如果石头剪刀布都出现就不算,等出到只有某两种了输的那方退出，剩下也是同样的方式直到最后一人。
Rules of group play: If rock-paper-scissors appears, it doesn't count, and the loser quits when there are only two kinds of players left."""

def start_markup(chatid):
    url = f"https://t.me/{config.CONFIG['Username']}?start=joinrps_{chatid}"
    button = InlineKeyboardButton("加入游戏 join gmae",url=url)
    return InlineKeyboardMarkup([[button]])

def startrps(update : Update, context : CallbackContext):
    user : User = update.effective_user
    chat : Chat = update.effective_chat
    update.message.reply_text(text=help(user.first_name),quote=False,reply_markup=start_markup(chat.id))

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["startrps"], startrps))

def start(update : Update, context : CallbackContext):
    # cmds: ['joinrps_-1001366387264']
    cmds = context.args
    chat : Chat = update.effective_chat
    if len(cmds) > 0:
        cmd,chatid = cmds[0].split("_")
        return f"你成功加入了在群组 [{chat.title}[http://t.me/{chat.username}]] 中的游戏"
    