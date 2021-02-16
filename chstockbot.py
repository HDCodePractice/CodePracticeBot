#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
from telegram.ext import Updater
import os
import logging
import getopt
import sys
import mysystemd
from telegram import Update,BotCommand
from telegram.ext import CallbackContext,Dispatcher,CommandHandler

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

def help():
    return "'bot.py -c <configpath>'"

if __name__ == '__main__':
    PATH = os.path.dirname(os.path.expanduser("~/.config/chstockbot/"))

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:",["config="])
    except getopt.GetoptError:
        print(help())
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help())
            sys.exit()
        elif opt in ("-c","--config"):
            PATH = arg

    config.config_file = os.path.join(PATH,"config.json")
    try:
        CONFIG = config.load_config()
    except FileNotFoundError:
        print("config.json not found.Generate a new configuration file in %s" % config.config_file)
        config.set_default()
        sys.exit(2)

    updater = Updater(CONFIG['Token'], use_context=True)
    dispatcher = updater.dispatcher

    me = updater.bot.get_me()
    CONFIG['ID'] = me.id
    CONFIG['Username'] = '@' + me.username
    config.set_default()
    print('Starting... (ID: ' + str(CONFIG['ID']) + ', Username: ' + CONFIG['Username'] + ')')

    from cmdproc import groupcmd
    commands = groupcmd.add_dispatcher(dispatcher)
    updater.bot.set_my_commands(commands)

    updater.start_polling()
    print('Started')
    mysystemd.ready()

    updater.idle()
    print('Stopping...')
    print('Stopped.')