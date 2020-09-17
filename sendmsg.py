#!/usr/bin/env python3

import os
import os
import getopt
import sys
import config

def help():
    return "'sendmsg.py -c <configpath>'"

if __name__ == '__main__':
    PATH = os.path.dirname(os.path.expanduser("~/.config/codepractice/"))

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:w:",["config="])
    except getopt.GetoptError:
        print(help())
        sys.exit(2)

    config.config_file = os.path.join(PATH,"config.json")
    try:
        CONFIG = config.load_config()
    except FileNotFoundError:
        print(f"config.json not found.Generate a new configuration file in {config.config_file}" )
        config.set_default()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-w"):
            # 发送天气预报
            pass
