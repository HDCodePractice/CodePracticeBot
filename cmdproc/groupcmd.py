import config
from telegram import Update,BotCommand
from telegram.ext import CallbackContext,Dispatcher,CommandHandler

wellcom_msg = ""
stock_msg = ""

def set_start_msg():
    config.CONFIG['start'] = wellcom_msg
    config.save_config()

def get_start_msg():
    global wellcom_msg
    if 'start' in config.CONFIG:
        wellcom_msg = config.CONFIG['start']
    else:
        wellcom_msg = """
欢迎来自clubhouse的朋友
点击后面的链接加入我们的股票开心聊群：
https://t.me/joinchat/IzsBA-YckmcYdpyX

点击后面的链接加入我们的旅行团友群：
https://t.me/joinchat/H7BPD0eLWqvSTPKB

点击后面的链接加入我们的狼人杀现场：
https://t.me/joinchat/H3E3Y_WL4MABeF9s
"""
    global stock_msg
    if 'stock_start' in config.CONFIG:
        stock_msg = config.CONFIG['stock_start']
    else:
        stock_msg = """
我们的旅行团友群：
https://t.me/joinchat/H7BPD0eLWqvSTPKB

我们的狼人杀现场：
https://t.me/joinchat/H3E3Y_WL4MABeF9s

交易提醒加入机器人
https://t.me/TradeAlertAssistantBot

本群精华收集频道-听毛票女神和女皇的
https://t.me/joinchat/TfWBdbo2jPd-rsRH

ARK交易跟踪频道
https://t.me/ark_fyi_bot
https://t.me/ARK_Trading_Desk

两个财经快讯频道
https://t.me/cnwallstreet
https://t.me/fnnew

一本书读懂K线图，图形技术入门书
https://t.me/c/1307935093/97

麦克米伦谈期权，读完之后再考虑操作期权
https://t.me/c/1307935093/95

期权、期货及其他衍生产品，读完之后再考虑操作期货
https://t.me/c/1307935093/96
"""

def delete_reply_msg(context : CallbackContext):
    msgs=context.job.context
    for msg in msgs:
        context.bot.delete_message(msg.chat.id,msg.message_id)

def start_cmd(update : Update, context : CallbackContext):
    delete_time = 30
    # stock group
    if update.effective_chat.id == -1001346239262: 
        msg = update.effective_message.reply_text(stock_msg,disable_web_page_preview=True)
    else:
        msg = update.effective_message.reply_text(wellcom_msg,disable_web_page_preview=True)
    context.job_queue.run_once(delete_reply_msg,delete_time,context=[msg,update.effective_message],name=f"delete_msg_{msg.message_id}")

def add_dispatcher(dp: Dispatcher):
    get_start_msg()
    dp.add_handler(CommandHandler(["start","help"], start_cmd))
    return [BotCommand('help','获得神秘代码')]