#!/usr/bin/env python3

import json
import os

loads = json.loads
load = json.load
dumps = json.dumps
dump = json.dump

config_file = ""
run_path = os.path.split(os.path.realpath(__file__))[0]

CONFIG = {}

def load_config():
    global CONFIG
    with open(config_file, 'r') as configfile:
        CONFIG = load( configfile )
    return CONFIG

def save_config():
    file_dir = os.path.split(config_file)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    with open(config_file, 'w') as configfile:
        dump(CONFIG, configfile, indent=4,ensure_ascii=False)

def get_json():
    return dumps(CONFIG,indent=4,ensure_ascii=False)

def set_default():
    # (filepath,filename) = os.path.split(config_file)
    # folder = os.path.exists(filepath)
    # if not folder:
    #     os.makedirs(filepath)
    load_config
    CONFIG.setdefault("Token","")       #BotToken
    CONFIG.setdefault("Admin",[])       #管理员id
    CONFIG.setdefault("Admin_path","")  #Admin Shell Path
    CONFIG.setdefault("OWM_key","")     #OpenWeatherMap key
    CONFIG.setdefault("Weather",{0:["name",0,0]}) # Weather记录的是 chatid:[lat=45.41,lon=-73.88]
    save_config()