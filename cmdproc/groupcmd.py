import config
from telegram import Update,BotCommand
from telegram.ext import CallbackContext,Dispatcher,CommandHandler

wellcom_msg = ""

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

def delete_reply_msg(context : CallbackContext):
    msgs=context.job.context
    for msg in msgs:
        context.bot.delete_message(msg.chat.id,msg.message_id)

def start_cmd(update : Update, context : CallbackContext):
    delete_time = 10
    msg = update.effective_message.reply_text(wellcom_msg,disable_web_page_preview=True)
    context.job_queue.run_once(delete_reply_msg,delete_time,context=[msg,update.effective_message],name=f"delete_msg_{msg.message_id}")

def add_dispatcher(dp: Dispatcher):
    get_start_msg()
    dp.add_handler(CommandHandler(["start","help"], start_cmd))
    # dp.add_handler(CommandHandler(["top"], top_cmd))
    # return [BotCommand('help','获得进群帮助'),BotCommand('top','得到群精华')]
    return [BotCommand('help','获得进群帮助')]