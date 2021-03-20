import json
import os
import config

def load_config():
    with open(config_file, 'r') as configfile:
        CONFIG = json.load(configfile)
    return CONFIG

def save_config():
    with open(config_file, 'w') as configfile:
        json.dump(CONFIG, configfile, indent=4,ensure_ascii=False)

RUN_PATH = os.getcwd()

config_file = f'{config.run_path}/ms.json'
CONFIG = load_config()
if not "game" in CONFIG:
    CONFIG["game"] = {}