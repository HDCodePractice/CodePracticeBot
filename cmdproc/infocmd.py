#!/usr/bin/env python3

from telegram.ext import Dispatcher,CommandHandler,CallbackContext
from telegram import BotCommand,Update
from json import dumps

msg_type = {
        "video":["file_id","file_unique_id","width","height","duration"],
        "photo":["file_id","file_unique_id","width","height","file_size"],
        "audio":["file_id","file_unique_id","mime_type","file_size"],
        "animation":["file_id","file_unique_id","width","height","duration"],
        "sticker":["file_id","file_unique_id","width","height","is_animated"],
        "video_note":["file_id","file_unique_id","length","duration"],
        "voice":["file_id","file_unique_id","duration","mime_type","file_size"]
    }

def getobjinfo (msgtype,msgobj):
    if msgtype == "photo":
        msg = f"PhotoSize("
    else:
        msg = f"{msgtype.capitalize()}("
    for i in msg_type[msgtype]:
        msg += str(f'{i}="{msgobj.__dict__[i]}",')
    return f"{msg[:-1]})\n"

def getmsgtype(update,context):
    if update.message.reply_to_message:
        if update.message.reply_to_message.video:
            video = update.message.reply_to_message.video
            update.message.reply_video(video,caption=f'{getobjinfo("video",video)}\nMade By Parker')
        elif update.message.reply_to_message.photo:
            msg = ''
            photo = update.message.reply_to_message.photo
            lastindex = -1
            for i in photo:
                lastindex += 1
                msg += f"\nPhoto {lastindex+1}:\n{getobjinfo('photo',i)}\n"
                
            msg += '\nMade By Parker'
            update.message.reply_photo(photo[lastindex],caption=msg)
        elif update.message.reply_to_message.audio:
            audio = update.message.reply_to_message.audio
            update.message.reply_audio(audio,caption=f'{getobjinfo("audio",audio)}\nMade By Parker')
        elif update.message.reply_to_message.animation:
            animation = update.message.reply_to_message.animation
            update.message.reply_animation(animation,caption=f'{getobjinfo("animation",animation)}\nMade By Parker')
        elif update.message.reply_to_message.sticker:
            sticker = update.message.reply_to_message.sticker
            update.message.reply_text(f'{getobjinfo("sticker",sticker)}\nMade By Parker')
        elif update.message.reply_to_message.video_note:
            video_note = update.message.reply_to_message.sticker
            update.message.reply_video_note(video_note,caption=f'{getobjinfo("video_note",video_note)}\nMade By Parker')
        elif update.message.reply_to_message.voice:
            voice = update.message.reply_to_message.voice
            update.message.reply_voice(voice,caption=f'{getobjinfo("voice",voice)}\nMade By Parker')
        else:
            info(update,context)
    else:
        info(update,context)

def info(update : Update, context : CallbackContext):
    u = str(update)
    u = dumps(eval(u),indent=2)
    update.message.reply_text(text=u)
    # context.bot.send_message(update.effective_user.id,text=u)

def add_dispatcher(dp:Dispatcher):
    dp.add_handler(CommandHandler('ainfo', getmsgtype))
    dp.add_handler(CommandHandler("info", info))
    return [BotCommand('ainfo','Get the msg type （Made by parker lol)'),BotCommand('info','查看消息的信息数据')]
