#!/usr/bin/env python3

"""
支持admin命令
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用说明

import admincmd

admincmd.add_dispatcher(dispatcher)

然后自己来改下cmds，设置命令名和按钮名。这样就支持  /admin 和所有的按钮回调了。注意，cmds的callback名一定要admin:开头。
"""

from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,Dispatcher,CallbackQueryHandler,CallbackContext
import config
from json import dumps
import os

cmds = [
    {
        "admin:config":"配置",
        "admin:update":"更新",
        "admin:restart":"重启",
        "admin:status":"状态"
    },{
        "admin:help":"帮助"
    }
]

def admin_cmd_callback(update : Update, context : CallbackContext):
    query = update.callback_query
    if query.from_user.id in config.CONFIG['Admin'] :
        msg=""
        if query.data == "admin:config":
            config.set_default()
            cfg = config.CONFIG.copy()
            cfg['Token'] = "***"
            cfg['OWM_key'] = "***"
            query.answer("获取配置")
            msg = dumps(cfg,indent=4,ensure_ascii=False)
        elif query.data == "admin:status":
            shell=config.CONFIG['Admin_path'] + '/status.sh > /tmp/status.txt'
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/status.txt").read()
            query.answer("获取状态")
        elif query.data == "admin:restart":
            shell=config.CONFIG['Admin_path'] + '/restart.sh > /tmp/restart.txt'
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/restart.txt").read()
            query.answer("重启服务")
        elif query.data == "admin:update":
            shell=config.CONFIG['Admin_path'] + '/update.sh > /tmp/gitpull.txt'
            os.system(shell)
            msg = "反回信息:\n" + open("/tmp/gitpull.txt").read()
            query.answer("更新代码")
        elif query.data == "admin:help":
            msg = help()
        if msg != query.message.text :
            query.edit_message_text(text=msg,reply_markup=init_replay_markup())
    else:
        query.answer("兄弟，这个按钮你不能按哟",show_alert=True)

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
可以点按按钮的必须是在配置文件里Admin的uid
/setw chatid,name,经度纬度 ... 设置天气预报发送配置，支持多组
/getw 显示现在的天气预报配置
配置： 查看配置文件的内容
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
    dp.add_handler(CommandHandler(["admin"], admin_cmd))
    dp.add_handler(CallbackQueryHandler(admin_cmd_callback,pattern="^admin:[A-Za-z0-9_]*"))
    return []
    