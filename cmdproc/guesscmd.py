#!/usr/bin/env python3

"""
在群里猜大小
"""

from random import randint
from telegram import Update,User,InlineKeyboardButton,InlineKeyboardMarkup,BotCommand
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
        "step":"start"              /start开局/play玩/""结束
    }
}
"""
guessResult = {}

start_buttons = [
    {
        "guess_start:add":"➕加入游戏",
        "guess_start:start":"▶️开始游戏"
        # "guess_start:score":"ℹ️查看成绩"
    }
]

play_buttons = [
    {
        "guess_play:x":"🔽小",
        "guess_play:d":"🔼大"
    },
    {
        "guess_play:do":"🧮结算"
    }
]

def gen_end_result(chatid)->str:
    # 得出一局的结果，如： 1+3+3=7
    global guessResult

    msg = "结算结果/Settlement results:"
    sum = 0
    for i in range(3):
        n = randint(1,6)
        sum += n
        if i == 2:
            msg += f"{n}="
        else:
            msg += f"{n}+"
    msg += f"{sum}\n"

    if len(guessResult[chatid]['histore']) >= 30:
        guessResult[chatid]['histore'] = guessResult[chatid]['histore'][0:29]
    if sum <= 10:
        guessResult[chatid]['histore'] += 'x'
        sum ='x'
    else:
        guessResult[chatid]['histore'] += 'd'
        sum = 'd'
    return msg

def check_chatid(chatid):
    # 如果这个chatid之前没有记录过数据
    if not (chatid in guessResult):
        guessResult[chatid] = {"histore":"","score":{},"state":{},"step":"start"}
        return False
    else:
        return True

def start_play_list(chatid)->str:
    # 开始参与时的玩家列表
    global guessResult
    
    msg = "\n玩家列表:"
    for key in guessResult[chatid]['state'].keys():
        msg += f"\n{guessResult[chatid]['state'][key][0]}"
    msg += f"\n\n30局走势:{guessResult[chatid]['histore']}"
    return msg

def play_play_list(chatid)->str:
    # 游戏进行中的玩家列表
    global guessResult

    msg = "\n玩家列表:"
    for key in guessResult[chatid]['state'].keys():
        if guessResult[chatid]['state'][key][1] == "d":
            msg += f"\n{guessResult[chatid]['state'][key][0]}:🔼大"
        elif guessResult[chatid]['state'][key][1] == "x":
            msg += f"\n{guessResult[chatid]['state'][key][0]}:🔽小"
        else:
            msg += f"\n{guessResult[chatid]['state'][key][0]}:🔴未完成"
    msg += f"\n\n30局走势:{guessResult[chatid]['histore']}"
    return msg

def end_play_list(chatid)->str:
    # 这是结算时的玩家列表
    msg = "\n玩家列表:"
    for key in guessResult[chatid]['state'].keys():
        if guessResult[chatid]['state'][key][1] == guessResult[chatid]['histore'][-1]:
            msg += f"\n{guessResult[chatid]['state'][key][0]}:胜利 😊"
        elif guessResult[chatid]['state'][key][1] == "":
            msg += f"\n{guessResult[chatid]['state'][key][0]}:未参与"
        else:
            msg += f"\n{guessResult[chatid]['state'][key][0]}:失败 😱"
    msg += f"\n\n30局走势:{guessResult[chatid]['histore']}"
    return msg

def help(chatid)->str:
    # print(guessResult)
    msg =  """
猜大小
三个1到6的数字之和，10及以下点小，11及以上点大。
The sum of three numbers from 1 to 6, if you think the sum is 10 and below , you click 🔽
If you think the sum is 11 and above , you click 🔼.
"""
    if guessResult[chatid]['step']=="start":
        msg += start_play_list(chatid)
    elif guessResult[chatid]['step']=="play":
        msg += play_play_list(chatid)
    elif guessResult[chatid]['step']=="end":
        msg += gen_end_result(chatid)
        msg += end_play_list(chatid)
    msg += "\n\nContributor:hdcola,Sicheng,Noah"
    return msg


def guess_start(update : Update, context : CallbackContext):
    # 处理/guess命令，这时处在游戏开始阶段
    global guessResult
    chatid = update.effective_chat.id
    check_chatid(chatid)
    # 新开局时，把所有的状态都清除
    guessResult[chatid]['state']={}
    guessResult[chatid]["step"] = "start"
    
    update.message.reply_text(help(chatid),reply_markup=init_replay_markup(start_buttons))

def guess_start_callback(update : Update, context : CallbackContext):
    global guessResult
    query = update.callback_query
    user : User = update.effective_user
    chatid = update.effective_chat.id
    check_chatid(chatid)
    if query.data == "guess_start:add":
        # 处理按下 guess_start:add 按钮
        if user.id in guessResult[chatid]['state']:
            query.answer("你已经加入游戏了！You're in the game!",show_alert=True)
            return
        else:
            guessResult[chatid]['state'][user.id]=[user.first_name,""]
            query.edit_message_text(text=help(chatid),reply_markup=init_replay_markup(start_buttons))
            query.answer("加入游戏成功！You joined the game successfully!")
    elif query.data == "guess_start:start":
        # 处理按下 guess_start:start 按钮
        guessResult[chatid]['step']="play"
        query.edit_message_text(text=help(chatid),reply_markup=init_replay_markup(play_buttons))
        query.answer("开局啦")

def guess_play_callback(update : Update, context : CallbackContext):
    global guessResult
    query = update.callback_query
    user : User = update.effective_user
    chatid = update.effective_chat.id
    check_chatid(chatid)
    if query.data == "guess_play:x":
        if guessResult[chatid]['state'][user.id]==[user.first_name,"x"]:
            query.answer("你已经选择了小")
            return
        else:
            guessResult[chatid]['state'][user.id]=[user.first_name,"x"]
            query.answer("你选择了小")
    elif query.data == "guess_play:d":
        if guessResult[chatid]['state'][user.id]==[user.first_name,"d"]:
            query.answer("你已经选择了大")
            return
        else:
            guessResult[chatid]['state'][user.id]=[user.first_name,"d"]
            query.answer("你选择了大")
    elif query.data == "guess_play:do":
        query.answer("结算结果")
        guessResult[chatid]['step']="end"
        query.edit_message_text(text=help(chatid))
        return
    query.edit_message_text(text=help(chatid),reply_markup=init_replay_markup(play_buttons))

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
    dp.add_handler(CallbackQueryHandler(guess_play_callback,pattern="^guess_play:[A-Za-z0-9_]*"))
    dp.add_handler(guess_handler)
    return get_command()

def get_command():
    return [BotCommand('guess','猜大小')]