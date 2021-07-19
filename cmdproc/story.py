from telegram.ext import Dispatcher,CommandHandler,MessageHandler,Filters, CallbackQueryHandler
from telegram import BotCommand,Update,InlineKeyboardButton, InlineKeyboardMarkup
import random
import re
from datetime import datetime

story = []

incomingstory = []

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

def get_choices(storylist):
    sendmsg = ''
    count = 0
    for partlist in storylist:
        count += 1
        sendmsg += f"\n\n{count}: {partlist['msg']} ✍️ 作者：{partlist['user'].first_name} 🗳 票数：{len(partlist['votes'])}"
    return sendmsg  

def get_buttons(incomingstory):
    kblist = []
    count = 0
    choicecount = -1
    for _i in incomingstory:
        choicecount += 1
        if choicecount % 5 == 0:
            kblist.append([])
        count += 1
        kblist[int(count/6)].append(InlineKeyboardButton(f'{count}',callback_data=f'getstory:{count-1}'))
    kb = InlineKeyboardMarkup(kblist)      
    return kb

def get_vote_max_nb(incomingstory):
    uids = []
    for partlist in incomingstory:
        if not partlist['user'].id in uids:
            uids.append(partlist['user'].id)
    return len(uids)

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
        sendmsg = '\n故事还没开始。'
    if len(msglist) == 0:
        update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s')
        return
    for word in msglist:
        msg += word
    if text != '':
        if msg[0] != lastletter:
            update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n⚠🤦 您没用正确字开头！请用‘{lastletter}’开始下一个句子！！！请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s')
            return
    if chinese(msg):
        incomingstory.append({'msg':msg,'user':user,'votes':[]})
        for partlist in story:
            text += partlist[0]
        if text != '':
            lastletter = get_last_letter(text)
            sendmsg = get_formatted_story(story)
        else:
            sendmsg = '\n故事还没开始。'
        sendchoices = get_choices(incomingstory)
        kb = get_buttons(incomingstory)
        update.message.reply_text(f"目前的故事:\n{sendmsg}\n\n目前的选项:{sendchoices}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s",reply_markup=kb)
    else:
        update.message.reply_text(f'目前的故事:\n{sendmsg}\n\n⚠️ 您没用中文！请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s')

def story_vote_callback(update,context):
    global incomingstory
    query = update.callback_query
    _,index = query.data.split(':')
    index = int(index)
    user = update.effective_user
    uid = user.id
    votes_required = get_vote_max_nb(incomingstory)
    text = ''
    for partlist in story:
        text += partlist[0]
    count = 0
    for partlist in incomingstory:
        if uid in partlist['votes']:
            incomingstory[index]['votes'].append(uid)
            incomingstory[count]['votes'].remove(uid)
            for partlist in story:
                text += partlist[0]
            if text != '':
                lastletter = get_last_letter(text)
                sendmsg = get_formatted_story(story)
            else:
                sendmsg = '\n故事还没开始。'
                lastletter = '任何中文字'
            sendchoices = get_choices(incomingstory)
            kb = get_buttons(incomingstory)
            if len(incomingstory[index]['votes']) >= votes_required:
                story.append([incomingstory[index]['msg'],incomingstory[index]['user']])
                text = ''
                for partlist in story:
                    text += partlist[0]
                lastletter = get_last_letter(text)
                query.edit_message_text(f"{index+1}号句子，‘{incomingstory[index]['msg']}’，被加入故事，因为这是第一个获得{votes_required}票的片段。\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s")
                incomingstory = []
            else:
                query.edit_message_text(f"目前的故事:\n{sendmsg}\n\n目前的选项:{sendchoices}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s\n\n{user.first_name}已成功的为{index+1}号句子投票。\n\n{user.first_name}给{count+1}号句子投的票已被重置。",reply_markup=kb)
            return
        count += 1
    incomingstory[index]['votes'].append(uid)
    for partlist in story:
        text += partlist[0]
    if text != '':
        lastletter = get_last_letter(text)
        sendmsg = get_formatted_story(story)
    else:
        lastletter = '任何中文字'
        sendmsg = '\n故事还没开始。'
    sendchoices = get_choices(incomingstory)
    kb = get_buttons(incomingstory)
    if len(incomingstory[index]['votes']) >= votes_required:
        story.append([incomingstory[index]['msg'],incomingstory[index]['user']])
        text = ''
        for partlist in story:
            text += partlist[0]
        lastletter = get_last_letter(text)
        query.edit_message_text(f"{index+1}号句子，‘{incomingstory[index]['msg']}’，被加入故事，因为这是第一个获得{votes_required}票的片段。\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s")
        incomingstory = []
    else:
        query.edit_message_text(f"目前的故事:\n{sendmsg}\n\n目前的选项:{sendchoices}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想查看故事，请使用 /view_s\n\n{user.first_name}已成功的为{index+1}号句子投票。",reply_markup=kb)

def end_story(update,context):
    global story
    update.message.reply_text(f'故事:\n{get_formatted_story(story)}\n\n故事结束')
    story = []

def view_story(update,context):
    text = ''
    for partlist in story:
        text += partlist[0]
    if text != '':
        lastletter = get_last_letter(text)
    else:
        lastletter = '任何中文字'
    update.message.reply_text(f'故事:\n{get_formatted_story(story)}\n\n请用‘{lastletter}’开始下一个句子。请用此格式：/cms [您的句子]\n\n如果想结束故事，请使用 /end_s')

def get_command():
    return [BotCommand('cms','写故事')]

def add_handler(dp):
    dp.add_handler(CommandHandler('cms',make_story))
    dp.add_handler(CommandHandler('end_s',end_story))
    dp.add_handler(CommandHandler('view_s',view_story))
    dp.add_handler(CallbackQueryHandler(story_vote_callback,pattern="^getstory:[A-Za-z0-9_]*"))