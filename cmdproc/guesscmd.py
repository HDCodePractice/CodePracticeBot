#!/usr/bin/env python3

"""
在群里猜大小
"""

import random
from telegram import Update,User,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Dispatcher,CommandHandler,CallbackContext,CallbackQueryHandler


"""
存储游戏的所有数据
{
    "chatid":{
        "histore":"dxdxdx"，        历史
        "score":{                   每个人的成绩
            uid:[first_name,12]
        },
        "state":{                   游戏状态
            uid:[first_name,"d or x"]
        },
        "step":"start"
    }
}
"""
guessResult = {}


start_buttons = [
    {
        "guess_start:start":"▶️开始游戏",
        "guess_start:score":"ℹ️查看成绩"
    }
]

def start_play_list(chatid)->str:
    # 开始参与时的玩家列表
    global guessResult
    # 如果这个chatid之前没有记录过数据
    if not (chatid in guessResult):
        guessResult[chatid] = {"histore":"","score":{},"state":{},"step":"start"}
    
    msg = "\n玩家列表:"
    for key in guessResult[chatid]['state'].keys():
        msg += f"\n{guessResult[chatid]['state'][key][0]}"
    return msg

def help(chatid)->str:
    msg =  """
猜大小 Noah&hdcola
三个1到7的数字之和，10及以下是小，11及以上是大。
The sum of three numbers from 1 to 7, 10 and below is small and 11 and above is large.
"""
    msg += start_play_list(chatid)
    return msg

def guess_start(update : Update, context : CallbackContext):
    # 处理/guess命令，这时处在游戏开始阶段
    global guessResult
    user : User = update.effective_user
    chatid = update.effective_chat.id
    update.message.reply_text(help(chatid),reply_markup=init_replay_markup(start_buttons))

def guess_start_callback(update : Update, context : CallbackContext):
    global guessResult
    query = update.callback_query
    user : User = update.effective_user
    chatid = update.effective_chat.id
    if query.data == "guess_start:start":
        if user.id in guessResult[chatid]['state']:
            query.answer("你已经加入游戏了！You're in the game!",show_alert=True)
            return
        else:
            guessResult[chatid]['state'][user.id]=[user.first_name,""]
            query.edit_message_text(text=help(chatid),reply_markup=init_replay_markup(start_buttons))

def init_buttons(cmds):
    buttons = []
    for cmd in cmds:
        button = []
        for key in cmd:
            button.append(InlineKeyboardButton(cmd[key], callback_data=key ) )
        buttons.append(button)
    return buttons

def init_replay_markup(cmds):
    return InlineKeyboardMarkup(init_buttons(cmds))

def add_dispatcher(dp:Dispatcher):
    guess_handler = CommandHandler('guess',guess_start)
    # 将所有guess_start开头的按钮处理交由guess_start_callback来进行
    dp.add_handler(CallbackQueryHandler(guess_start_callback,pattern="^guess_start:[A-Za-z0-9_]*"))
    dp.add_handler(guess_handler)
