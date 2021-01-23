from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand,InputMediaAudio
import pafy
import os


def youtubemusic(update,context):
    if len(context.args) == 1:
        url = context.args[0]
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4a")
        filepath = f"/tmp/{bestaudio.title}.{bestaudio.extension}"
        music_size = bestaudio.get_filesize()
        if music_size > 1000*1000*10:
            update.message.reply_text("Sorry, but that message is too big. It cannot be bigger than 10MB.")
            return
        bestaudio.download(filepath=filepath)
        img = "https://cloud.addictivetips.com/wp-content/uploads/2019/03/Hiding-IP-Downloading-1-Downloading.jpg"
        msg = update.message.reply_photo(img,caption=f"Downloading your file of {music_size/1000}KB...")
        msg.edit_media(InputMediaAudio(open(filepath,'rb')))
        os.remove(filepath)
    else:
        update.message.reply_text("Sorry, but I need a URL after that.")

def add_ytmusichandler(dp:Dispatcher):
    dp.add_handler(CommandHandler('YTmusic', youtubemusic))

def get_command():
    return [BotCommand('YTmusic','Parker made this command because it was the best')]
