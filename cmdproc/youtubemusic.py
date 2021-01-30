from telegram.ext import Dispatcher,CommandHandler,CallbackQueryHandler
from telegram import BotCommand, InputMediaAudio
import pafy
import os

def youtubemusic(update,context):
    if len(context.args) == 1:
        url = context.args[0]
        video = pafy.new(url)
        update.message.reply_text(str(video) )
    else:
        update.message.reply_text("Put a link! for example: /pd_yt_music@dankpbot https://www.youtube.com/watch?v=r_a4Zg3PyA0")

def musicOnly(update,context):
    if len(context.args) == 1:
        url = str(context.args[0])
        if 'www.youtube.com' in url:
            chatid = update.effective_chat.id
            video = pafy.new(url)
            v = str(video).split('\n')
            title = v[0].split(':')[1]
            author = v[1].split(':')[1]
            bestaudio = video.getbestaudio(preftype="m4a")
            music_size = bestaudio.get_filesize()
            audiofile = f'/tmp/{bestaudio.title}.{bestaudio.extension}'
            a = audiofile.split('"')
            a2 = ''
            audio = ''
            for i in a:
                a2 += f'{i}'
            a3 = a2.split(" ")
            for j in a3:
                audio += f'{j}'
            if music_size < 1000*1000*10:
                img = "https://i.pcmag.com/imagery/articles/04oP7J3OIykTchX4vhU57vn-28..1569485834.jpg"
                bestaudio.download(audio)
                msg = update.message.reply_photo(img,f"downloading... Your audio's size is {music_size/100}KB\n\n🎵 Music: {title} by 🎶 {author}")
                msg.edit_media(InputMediaAudio(open(audio,'rb')))
                msg == context.bot.send_message(chatid,f"{str(video)}")
                os.remove(audio)
            else: 
                update.message.reply_text("Sorry this file is too big")
        else:
            update.message.reply_text("YT VID!")
    else:
        update.message.reply_text("Put a link! for example: /pdgetmusic@dankpbot https://www.youtube.com/watch?v=r_a4Zg3PyA0")

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('getMusicInfo', youtubemusic))
    dp.add_handler(CommandHandler('ytm', musicOnly))
