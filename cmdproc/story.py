from telegram.ext import Dispatcher,CommandHandler,MessageHandler,Filters
from telegram import BotCommand,Update
import random
import re
from datetime import datetime

story = []

def get_last_letter(text):
    chinesechars = []
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            chinesechars.append(char)
    return chinesechars[-1]

def chinese(msg):
    for char in msg:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False

def get_formatted_story(storylist):
    sendmsg = ''
    for partlist in storylist:
        sendmsg += f'\n{partlist[0]} ✍️ 作者：{partlist[1].first_name}'
    return sendmsg
        

def make_story(update,context):
    msglist = context.args
    user = update.effective_user
    msg = ''
    text = ''
    for partlist in story:
        text += partlist[0]
    if text == '':
        lastletter = '任何中文字'
    else:
        lastletter = get_last_letter(text)
    if len(story) > 0:
        sendmsg = get_formatted_story(story)
    else:
        sendmsg = '故事还没开始。'
    if len(msglist) == 0:
        update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/write [您的句子]')
        return
    for word in msglist:
        msg += word
    if text != '':
        if msg[0] != lastletter:
            update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n⚠🤦 您没用正确字开头！请用‘{lastletter}’开始下一个句子！！！请用此格式：/write [您的句子]')
            return
    if chinese(msg):
        story.append([msg,user])
        sendmsg = get_formatted_story(story)
        for partlist in story:
            text += partlist[0]
        lastletter = get_last_letter(text)
        update.message.reply_text(f"目前的故事:\n{sendmsg}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/write [您的句子]")
    else:
        update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n⚠️ 您没用中文！请用‘{lastletter}’开始下一个句子。请用此格式：/write [您的句子]')

def end_story(update,context):
    global story
    text = ''
    for partlist in story:
        text += partlist[0]
    update.message.reply_text(f'故事:\n\n{text}\n\n故事结束')
    story = []

def get_command():
    return []

def add_handler(dp):
    dp.add_handler(CommandHandler('write',make_story))
    dp.add_handler(CommandHandler('end_story',end_story))