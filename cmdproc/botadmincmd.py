#!/usr/bin/env python3

"""
支持adminbot命令
"""

from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,Dispatcher,CallbackQueryHandler,CallbackContext
import config
from json import dumps
import os

cmds = [
    {
        "adminbot:scupdate":"思成更新",
        "adminbot:scstart":"启动",
        "adminbot:scstop":"停止",
        "adminbot:scstatus":"状态"
    },{
        "adminbot:noahupdate":"Noah更新",
        "adminbot:noahrestart":"重启",
        "adminbot:noahstatus":"状态"
    },{
        "adminbot:help":"帮助"
    }
]

# sicheng的shell目录
sichengShell = "/home/pi/sicheng/MyFirstBot/shell"

def admin_cmd_callback(update : Update, context : CallbackContext):
    query = update.callback_query
    if query.from_user.id in config.CONFIG['Admin'] :
        msg=""
        if query.data == "adminbot:help":
            msg = help()
        elif query.data == "adminbot:scstart":
            shell = f"{sichengShell}/start.sh > /tmp/status.txt"
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/status.txt").read()
        elif query.data == "adminbot:scstop":
            shell = f"{sichengShell}/stop.sh > /tmp/status.txt"
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/status.txt").read()
        elif query.data == "adminbot:scupdate":
            shell = f"{sichengShell}/update.sh > /tmp/status.txt"
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/status.txt").read()
        elif query.data == "adminbot:scstatus":
            shell = f"{sichengShell}/status.sh > /tmp/status.txt"
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/status.txt").read()
        if msg != query.message.text :
            query.edit_message_text(text=msg,reply_markup=init_replay_markup())
    else:
        query.answer("兄弟，这个按钮只能管理员操作哟",show_alert=True)

def init_buttons():
    buttons = []
    for cmd in cmds:
        button = []
        for key in cmd:
            button.append(InlineKeyboardButton(cmd[key], callback_data=key ) )
        buttons.append(button)
    return buttons

def init_replay_markup():
    return InlineKeyboardMarkup(init_buttons())

def help():
    msg = """
通过这里可以管理小怪兽们的bot
更新： 从GitHub上更新Bot的代码
重启： 重启Bot，应用新的代码或配置
状态： 查看服务运行的状态
作者：hdcola
"""
    return msg

def admin_cmd(update : Update, context : CallbackContext):
    if update.message.from_user.id in config.CONFIG['Admin'] :
        msg = help()
        update.message.reply_text(msg,reply_markup=init_replay_markup())

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["botadmin"], admin_cmd))
    dp.add_handler(CallbackQueryHandler(admin_cmd_callback,pattern="^adminbot:[A-Za-z0-9_]*"))
    return []
    