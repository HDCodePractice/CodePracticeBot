import random
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from telegram import BotCommand, InlineKeyboardMarkup,InlineKeyboardButton
import util

games = {}

def rules():
    return r""" 欢迎来到 Noah 的故事接龙游戏！

您可以开启一个游戏使用命令 /smnew 。
游戏开始之后，任意一个玩家可以编故事的第一句话。

第一句话说完之后，别的玩家可以来接龙使用 /smw [要说的东西]。

如果您想接龙，您句子的第一个字必须和上一个人说的句子的最后一个*中文汉字*一样。
比如：

    我是 Noah
    是 Noah 呀

您接龙的句子里并且还需要包括至少一个中文汉字。

别的玩家接龙完了之后，写上一句话的人可以选择他/她最喜欢的接龙使用命令 /smchoose。

如果想看目前的故事，可以使用命令 /sminfo。
如果想查看规则, 可以使用命令 /smrules。
如果想结束游戏, 可以使用命令 /smend。
    """

def detective_system(strs):
    last = ""
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            last = _char
    return last

def set_up(chatid):
    games[chatid] = {}
    games[chatid]['story'] = ""
    games[chatid]['trans'] = ""
    games[chatid]['current'] = ""
    games[chatid]['count'] = 1
    games[chatid]['nextanswer'] = []
    games[chatid]['keyboard'] = [{}]

def new(update,context):
    chatid = update.effective_chat.id
    set_up(chatid)
    update.effective_message.reply_text(f"游戏开始！\n\n{rules()}")

def start(update,context):
    chatid = update.effective_chat.id
    first_name = update.effective_user.first_name
    uid = str(update.effective_user.id)
    reply = ""
    if not len(context.args) == 0:
        for each in context.args:
            reply += each + " "
    else:
        update.effective_message.reply_text("请按照格式：/smw [要说的东西]")
        return
    try:
        if not detective_system(reply) == "":
            if reply[0] == games[chatid]['trans']:
                games[chatid]['nextanswer'].append(f"{uid}:{first_name}:{reply}:{games[chatid]['count']}")
                games[chatid]['count'] += 1
                update.effective_message.reply_text("接龙成功！")
            elif games[chatid]['trans'] == "":
                games[chatid]['current'] = uid
                games[chatid]['story'] += f"{reply} ➡ ({first_name})\n"
                games[chatid]['trans'] = detective_system(reply)
                update.effective_message.reply_text(f"{games[chatid]['story']}\n\n下一个人请使用 '{games[chatid]['trans']}' 开头的句子来造句。")
            else:
                update.effective_message.reply_text(f"{first_name} 请使用 '{games[chatid]['trans']}' 开头的句子来造句!")
        else:
            update.effective_message.reply_text(f"{first_name}, 请输入一个中文的句子！")
    except KeyError:
        update.effective_message.reply_text(f"目前没有被开启的游戏。请使用指令 /smnew 来开启一个新的游戏。")

def vac(update,context):
    msg = ""
    chatid = update.effective_chat.id
    uid = str(update.effective_user.id)
    try:   
        games[chatid]['keyboard'] = [{}]  
        for every in games[chatid]['nextanswer']:
            info = every.split(":")
            if not len(games[chatid]['keyboard'][-1]) == 4:
                games[chatid]['keyboard'][-1][info[3]] = f"story:{info[3]}:{uid}"
            else:
                games[chatid]['keyboard'].append({})
                games[chatid]['keyboard'][-1][info[3]] = f"story:{info[3]}:{uid}"
            kb = util.getkb(games[chatid]['keyboard'])
            info = every.split(":")
            msg += f"{info[3]}: {info[2]} ➡ ({info[1]})\n"
        update.effective_message.reply_text(msg,reply_markup=kb)
    except KeyError:
        update.effective_message.reply_text(f"目前没有被开启的游戏。请使用指令 /smnew 来开启一个新的游戏。")

def info(update,context):
    chatid = update.effective_chat.id
    try:
        if not games[chatid]['trans'] == "":
            update.effective_message.reply_text(f"{games[chatid]['story']}\n\n下一个人请使用 '{games[chatid]['trans']}' 开头的句子来造句。")
        else:
            update.effective_message.reply_text("请说第一句话！")
    except KeyError:
        update.effective_message.reply_text(f"目前没有被开启的游戏。请使用指令 /makestory 来开启一个新的游戏。")

def end(update,context):
    chatid = update.effective_chat.id
    try:
        update.effective_message.reply_text(f"游戏结束。这是你们所编的故事：\n\n{games[chatid]['story']}")
        del games[chatid]
    except KeyError:
        update.effective_message.reply_text(f"目前没有被开启的游戏。请使用指令 /makestory 来开启一个新的游戏。")

def callback(update,context):
    choice = 0
    chatid = update.effective_chat.id
    query = update.callback_query
    cmd = query.data.split(":")
    if games[chatid]['current'] == str(update.effective_user.id):
        query.answer("成功！")
        for line in games[chatid]['keyboard']:
            for button in line:
                if cmd[1] == button:
                    choice = button
        for every in games[chatid]['nextanswer']:
            info = every.split(":")
            if info[3] == choice:
                update.effective_message.reply_text(f"👌 {info[1]} 会是接龙的人，他/她可以做下一个选择。(认为最棒的答案)")
                games[chatid]['current'] = info[0]
                games[chatid]['story'] += f"{info[2]} ➡ ({info[1]})\n"
                games[chatid]['trans'] = detective_system(info[2])
                games[chatid]['nextanswer'] = []
                games[chatid]['count'] = 1
                games[chatid]['keyboard'] = [{}]
                update.effective_message.reply_text(f"{games[chatid]['story']}\n\n下一个人请使用 '{games[chatid]['trans']}' 开头的句子来造句。")
    else:
        query.answer("您不是选择的人！")

def gamerules(update,context):
    update.effective_message.reply_text(rules())

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('smw', start))
    dp.add_handler(CommandHandler('smend', end))
    dp.add_handler(CommandHandler('sminfo', info))
    dp.add_handler(CommandHandler('smchoose', vac))
    dp.add_handler(CommandHandler('smnew', new))
    dp.add_handler(CommandHandler('smrules', gamerules))
    dp.add_handler(CallbackQueryHandler(callback,pattern="^story:[A-Za-z0-9_:]*"))
    return [
        BotCommand('smnew','开始一个故事接龙的游戏'),
        BotCommand('sminfo','查询一个故事接龙的游戏的信息'),
        BotCommand('smchoose','选择下一个接龙的人'),
        BotCommand('smw','继续接龙'),
        BotCommand('smend','结束一个故事接龙的游戏'),
        BotCommand('smrules','查询一个故事接龙的游戏的规则')
        ]