import random, string, re
from random import sample
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters, Updater
from telegram import BotCommand

#Fix bug where users are added to lead twice: 

games = {}

def help():
    return r"""Welcome to Parker's game of 24! 
    
Your goal is to try to use four numbers to figure out 24

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

def set_games_data(chatid,cards,uid,fname):
    games[chatid] = {}
    games[chatid]['cards'] = cards
    games[chatid]['users'] = {}
    games[chatid]['users'][uid] = {
            'fname':fname,
            'correct':{
                'count':0,
                'answer':[]
            },
            'error':0,
            'inlead':False
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
    set_games_data(chatid,cards,uid,fname)


def question(update,context):
    chatid = update.effective_chat.id
    correctAnswers = ""
    try:
        for uid in games[chatid]['users']:
            if not 'lead' in games[chatid]:
                lead = []
            for answer in games[chatid]['users'][uid]['correct']['answer']:
                if not games[chatid]['users'][uid]['inlead'] == True:
                    correctAnswers += f"{games[chatid]['users'][uid]['fname']}: {answer}\n"
                    lead.append({"name":games[chatid]['users'][uid]['fname'], "count":games[chatid]['users'][uid]['correct']['count']})
                    games[chatid]['users'][uid]['inlead'] = True
                    print(lead)
                    games[chatid]['lead'] = lead
            
            list_of_peoples_scores = []
            for i in games[chatid]['users']:
                list_of_peoples_scores.append(games[chatid]['users'][i]['correct']['count'])
            list_of_peoples_scores.sort(reverse=True)


        update.effective_message.reply_text(f"""Current Cards：{games[chatid]['cards']}
--------------------
Current correct answers:

{correctAnswers}
--------------------
Individual rankings:

{games[chatid]['lead']}
{list_of_peoples_scores}
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
