#!/usr/bin/env python3

from telegram.ext import Updater
import mysystemd
import os
import getopt
import sys
import config

def help():
    return "'bot.py -c <configpath>'"

if __name__ == '__main__':
    PATH = os.path.dirname(os.path.expanduser("~/.config/codepractice/"))

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
        print(f"config.json not found.Generate a new configuration file in {config.config_file}" )
        config.set_default()
        sys.exit(2)

    updater = Updater(CONFIG['Token'], use_context=True)
    dispatcher = updater.dispatcher

    me = updater.bot.get_me()
    CONFIG['ID'] = me.id
    CONFIG['Username'] = '@' + me.username
    config.set_default()
    print(f"Starting... ID: {str(CONFIG['ID'])} , Username: {CONFIG['Username']}")

    # 在这里加入功能
    from cmdproc import startcmd,rewardscmd,admincmd,weathercmd,infocmd,penaltiescmd,guesscmd,capitals
    commands = startcmd.add_dispatcher(dispatcher)
    commands = admincmd.add_dispatcher(dispatcher)
    commands = rewardscmd.add_dispatcher(dispatcher)
    commands += weathercmd.add_dispatcher(dispatcher)
    commands += penaltiescmd.add_dispatcher(dispatcher)    
    commands += guesscmd.add_dispatcher(dispatcher)
    commands += infocmd.add_dispatcher(dispatcher)
    commands += capitals.add_handler(dispatcher)
    
    print(commands)
    updater.bot.set_my_commands(commands)


    updater.start_polling()
    print('Started...')
    mysystemd.ready()

    updater.idle()
    print('Stopping...')
    print('Stopped.')