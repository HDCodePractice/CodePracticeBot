import random, string, re
from random import sample
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters, Updater
from telegram import BotCommand

games = {}

def help():
    return r"""Welcome to Noah's Aunt Grace's game of 24! 
    
Your goal is to try to use four numbers to figure out 24.
Remember, you can only use +, -, *, / and (). 

Good luck!"""

def detective_system(answer,cards):
    Cheat = False
    Numbers = list(dict.fromkeys(re.findall(r'\d+', answer)))
    modsAnswer = answer.replace("+","_").replace("-","_").replace("*","_").replace("/","_")
    a = modsAnswer.split("_")
    if not len(a) == 4:
        Cheat = True
    for number in Numbers:
        if not int(number) in cards:
            Cheat = True
    return Cheat

def set_games_cards(chatid,cards,uid,fname):
    games[chatid] = {}
    games[chatid]['cards'] = cards
    games[chatid]['users'] = {}
    games[chatid]['users'][uid] = {
            'fname':fname,
            'correct':{
                'count':0,
                'answer':[]
            },
            'error':0
        }
    games[chatid]['totalanswers'] = []
    # print(games)

def check_user(uid,chatid,first_name):
    if not uid in games[chatid]['users']:
        games[chatid]['users'][uid] = {
            'fname':first_name,
            'correct':{
                'count':0,
                'answer':[]
            },
            'error':0
        }

def start(update,context): 
    uid = str(update.effective_user.id)
    fname = str(update.effective_user.first_name)
    chatid = update.effective_chat.id
    cards = random.sample([1,2,3,4,5,6,7,8,9,10],4) 
    update.effective_message.reply_text(f" {help()} The four numbers are：") 

    context.bot.send_message(chatid, text=f"{cards[0]}, {cards[1]}, {cards[2]}, {cards[3]}")
    set_games_cards(chatid,cards,uid,fname)


def question(update,context):
    chatid = update.effective_chat.id
    correctAnswers = ""
    lead = ""
    numofanswers = 0
    try:
        for uid in games[chatid]['users']:
            for answer in games[chatid]['users'][uid]['correct']['answer']:
                correctAnswers += f"Answer #{numofanswers+1} {games[chatid]['users'][uid]['fname']}: {answer}\n"
                numofanswers += 1
            lead += f"✨ {games[chatid]['users'][uid]['fname']}: ✅ {games[chatid]['users'][uid]['correct']['count']} times correct ❌ {games[chatid]['users'][uid]['error']} times incorrect\n"
        update.effective_message.reply_text(f"""Current Cards：{games[chatid]['cards']}
--------------------
Current correct answer.

{correctAnswers}
--------------------
个人排行榜：

{lead}
""")
    except KeyError:
        update.effective_message.reply_text("No games are currently opened. /gamestart24 to open a game。")

def end(update,context):
    update.effective_message.reply_text("Game over. /gamestart24 to open a game.")
    del games[update.effective_chat.id]

def rules(update,context):
    update.message.reply_text(help())
    
def proc_text(update,context):
    first_name = update.effective_user.first_name
    chatid = update.effective_chat.id
    uid = str(update.effective_user.id)    
    msg = ""
    answer = update.message.text.replace(".","").replace(" ","")
    if answer[0].isdigit() or answer[0]=="(":
        try: 
            cards = games[chatid]['cards']
            check_user(uid,chatid,first_name)
            if not answer in games[chatid]['totalanswers']:
                try:
                    if detective_system(answer,cards) == False:
                        if int(eval(answer)) == 24:
                            msg = f"{first_name} You got it!！" 
                            games[chatid]['users'][uid]['correct']['count'] += 1
                            games[chatid]['users'][uid]['correct']['answer'].append(answer.replace(" ",""))
                            games[chatid]['totalanswers'].append(answer.replace(" ",""))
                            # print(games[chatid]['totalanswers'])  
                        else:  
                            msg = f"{first_name} Wrong answer!"
                            games[chatid]['users'][uid]['error'] += 1
                    else:
                        games[chatid]['users'][uid]['error'] += 1
                        msg = f"Please use the numbers I gave you! To see more rules, please check /gamerules ."                                                                                                                    
                except:
                    msg = f"{first_name} Wrong answer! Your goal is to try to use {games[chatid]['cards']} to figure out 24.\n Remember, you can only use +, -, *, / and (). "
                    games[chatid]['users'][uid]['error'] += 1
            else:
                msg = f"{first_name}, Someone has said your answer!"
        except KeyError:
            msg = "There are no games currently open. /gamestart24 to open a game."
        update.effective_message.reply_text(msg)

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('gamestart24', start))
    dp.add_handler(CommandHandler('gameq', question))
    dp.add_handler(CommandHandler('gameend24', end))
    dp.add_handler(CommandHandler('gamerules', rules))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command),proc_text))
    return [
        BotCommand('gamestart24','Start a 24-point game'),
        BotCommand('gameq','Query the currently in progress 24-point game'),
        BotCommand('gameend24','end the current game in progress'),
        BotCommand('gamerules','Query the rules of a 24-point game')
        ]
