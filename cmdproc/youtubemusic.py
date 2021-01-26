from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand,InputMediaAudio,PhotoSize
import pafy
import os
import config


def youtubemusic(update,context):
    if len(context.args) == 1:
        url = context.args[0]
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4a")
        filepath = f"/tmp/{bestaudio.title}.{bestaudio.extension}"
        music_size = bestaudio.get_filesize()
        if music_size > 1000*1000*10:
            update.message.reply_text("对不起，这个音乐超过了10MB！Sorry, this music is more than 10MB.")
            return
        img = f"{config.run_path}/imgs/downloading.jpg"
        msg = update.message.reply_photo(open(img,'rb'),caption=f"正在下载你的音乐/Downloading your music of {music_size/1000}KB...")
        bestaudio.download(filepath=filepath,quiet=True)
        msg.edit_media(InputMediaAudio(open(filepath,'rb')),timeout=60)
        os.remove(filepath)
    else:
        update.message.reply_text("对不起，需要给我一个像样儿的网址/Sorry, but I need a URL after that.比如:\n/ytm ")

def add_dispatcher(dp:Dispatcher):
    dp.add_handler(CommandHandler('ytm', youtubemusic))
    return [BotCommand('ytm','下载油管音乐/Download Youtube Music（Made by Parker)')]