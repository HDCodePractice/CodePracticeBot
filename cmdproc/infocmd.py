from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand
from json import dumps

def getobjinfo (msgtype,msgobj):
    msg = ""
    for i in msg_type[msgtype]:
        msg += str(f'{i} = {msgobj.__dict__[i]}\n')
    return msg

def getmsgtype(update,context):
    global msg_type
    msg_type = {
        "video":["file_id","file_unique_id","width","height","duration"],
        "photo":["file_id","file_unique_id","width","height","file_size"],
        "audio":["file_id","file_unique_id","mime_type","file_size"],
        "animation":["file_id","file_unique_id","width","height","duration"],
        "sticker":["file_id","file_unique_id","width","height","is_animated"],
        "video_note":["file_id","file_unique_id","length","duration"],
        "voice":["file_id","file_unique_id","duration","mime_type","file_size"]
    }
    if update.message.reply_to_message:
        if update.message.reply_to_message.video:
            video = update.message.reply_to_message.video
            update.message.reply_video(video,caption=f'{getobjinfo("video",video)}\n\nMade By Parker')
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
            update.message.reply_audio(audio,caption=f'{getobjinfo("audio",audio)}\n\nMade By Parker')
        elif update.message.reply_to_message.animation:
            animation = update.message.reply_to_message.animation
            update.message.reply_animation(animation,caption=f'{getobjinfo("animation",animation)}\n\nMade By Parker')
        elif update.message.reply_to_message.sticker:
            sticker = update.message.reply_to_message.sticker
            update.message.reply_sticker(sticker,caption=f'{getobjinfo("sticker",sticker)}\n\nMade By Parker')
        elif update.message.reply_to_message.video_note:
            video_note = update.message.reply_to_message.sticker
            update.message.reply_video_note(video_note,caption=f'{getobjinfo("video_note",video_note)}\n\nMade By Parker')
        elif update.message.reply_to_message.voice:
            voice = update.message.reply_to_message.voice
            update.message.reply_voice(voice,caption=f'{getobjinfo("voice",voice)}\n\nMade By Parker')
    else:
        msg = 'Helloooooo?! This command gives you the info for the MESSAGE YOU REPLIED TO! You didn\'t even reply to anything!'


def add_getmsgtypehandler(dp:Dispatcher):
    dp.add_handler(CommandHandler('getmsgtype', getmsgtype))

def get_command():
    return [BotCommand('getmsgtype','Get the msg type （Made by parker lol)')]
