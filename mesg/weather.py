#!/usr/bin/env python3

from pyowm import OWM
import config
from telegram import Bot
from cmdproc import weathercmd

def sendmsg(bot:Bot):
    ws = config.CONFIG['Weather']
    owm = OWM(config.CONFIG['OWM_key'])
    for chat in ws.keys():
        name,lat,lon = ws[chat]
        msg = f"{name}\n{weathercmd.get_weather(owm,lat=lat,lon=lon)}"
        bot.send_message(chat_id=int(chat),text=msg)
