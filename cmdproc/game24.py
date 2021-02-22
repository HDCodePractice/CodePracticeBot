import random, string, re
from random import sample
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters, Updater
from telegram import BotCommand

games = {}

def help():
    return r"""欢迎来到 Noah 的 24 点游戏! 
    
您的目标是尝试去使用四个数字来算出 24.
请记住, 您只能使用 +, -, *, / 和 ()。 

祝你们好运!"""

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
    print(games)

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
    update.effective_message.reply_text(f" {help()} 四个数字分别是：") 

    context.bot.send_message(chatid, text=f"{cards[0]}, {cards[1]}, {cards[2]}, {cards[3]}")
    set_games_cards(chatid,cards,uid,fname)


def question(update,context):
    chatid = update.effective_chat.id
    correctAnswers = ""
    lead = ""
    try:
        for uid in games[chatid]['users']:
            for answer in games[chatid]['users'][uid]['correct']['answer']:
                correctAnswers += f"✔︎ {games[chatid]['users'][uid]['fname']}: {answer}\n"
            lead += f"✨ {games[chatid]['users'][uid]['fname']}: ✅ {games[chatid]['users'][uid]['correct']['count']} 次正确 ❌ {games[chatid]['users'][uid]['error']} 次错误\n"
        update.effective_message.reply_text(f"""当前卡牌：{games[chatid]['cards']}
--------------------
目前的正确答案：

{correctAnswers}
--------------------
个人排行榜：

{lead}
""")
    except KeyError:
        update.effective_message.reply_text("目前没有被开启的游戏。/gamestart24@Noah24GameBot 来开启一个游戏。")

def end(update,context):
    update.effective_message.reply_text("游戏结束。/gamestart24@Noah24GameBot 来开启一个游戏。")
    del games[update.effective_chat.id]

def rules(update,context):
    update.message.reply_text(help())
    
def proc_text(update,context):
    first_name = update.effective_user.first_name
    chatid = update.effective_chat.id
    uid = str(update.effective_user.id)    
    msg = ""
    answer = update.message.text.replace(".","")
    try: 
        cards = games[chatid]['cards']
        check_user(uid,chatid,first_name)
        if not answer.replace(" ","") in games[chatid]['totalanswers']:
            try:
                if detective_system(answer,cards) == False:
                    if int(eval(answer)) == 24:
                        msg = f"{first_name} 答对啦！" 
                        games[chatid]['users'][uid]['correct']['count'] += 1
                        games[chatid]['users'][uid]['correct']['answer'].append(answer.replace(" ",""))
                        games[chatid]['totalanswers'].append(answer.replace(" ",""))
                        print(games[chatid]['totalanswers'])  
                    else:  
                        msg = f"{first_name} 答错啦！"
                        games[chatid]['users'][uid]['error'] += 1
                else:
                    games[chatid]['users'][uid]['error'] += 1
                    msg = f"请使用我给你的那几个数字！需有查看更多规则，请查看 /gamerules@Noahs24GameBot."                                                                                                                    
            except:
                msg = f"{first_name} 答错啦！您的目标是尝试去使用 {games[chatid]['cards']} 来算出 24.\n请记住, 您只能使用 +, -, *, / 和 (). "
                games[chatid]['users'][uid]['error'] += 1
        else:
            msg = f"{first_name}, 某某人已经说出来您的答案啦！"
    except KeyError:
        msg = "目前没有被开启的游戏。/gamestart24@Noah24GameBot 来开启一个游戏。"
    
    update.effective_message.reply_text(msg)

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('gamestart24', start))
    dp.add_handler(CommandHandler('gameq', question))
    dp.add_handler(CommandHandler('gameend24', end))
    dp.add_handler(CommandHandler('gamerules', rules))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command) & Filters.chat_type.supergroup,proc_text))
    return [
        BotCommand('gamestart24','开始一个24点游戏'),
        BotCommand('gameq','查询当前进行中的24点游戏'),
        BotCommand('gameend24','结束当前进行的游戏'),
        BotCommand('gamerules','查询24点的游戏规则')
        ]