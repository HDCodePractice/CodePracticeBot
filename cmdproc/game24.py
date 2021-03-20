import random, string, re, datetime, config
from cmdproc import twconfig
from random import sample
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters, Updater
from telegram import BotCommand, PhotoSize

games = {}
LifetimeStats = twconfig.CONFIG['LifetimeStats']

def help():
    return r"""欢迎来到 Grace 的 24 点游戏! 
    
您的目标是尝试去使用四个数字来算出 24 (四个数字可以在 /gameq 找到)。
每张牌都必须使用一次。
请记住, 您只能使用 加，减，乘，除，和括号 （请不要用不必要的括号）。 
您只能使用三个加减乘除的符号。

祝你们好运！@作者：Noah、Sicheng
--------------------
Welcome to Aunt Grace's 24 point game!
    
Your goal is to try to use four numbers to calculate 24 (the four numbers can be found in /gameq).
Each card must be used once.
Remember, you can only use addition, subtraction, multiplication, division, and parentheses (please don't use unnecessary parentheses).
You can only use three symbols for addition, subtraction, multiplication, and division.

Wish ya'll good luck! @: Noah, Sicheng"""

def correctAnswers(func):
    return func['correct']

def errors(func):
    return func['error']

def times(func):
    return func['AccTime']

def set_games_cards(chatid,cards,uid,fname):
    games[chatid] = {}
    games[chatid]['cards'] = cards
    games[chatid]['time'] = datetime.datetime.now()
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

def check_user(uid,chatid,first_name):
    if not chatid in games:
        games[chatid] = {}
        games[chatid]['users'] = {}
    if not uid in games[chatid]['users']:
        games[chatid]['users'][uid] = {
            'fname':first_name,
                'correct':{
                    'count':0,
                    'answer':[]
                },
                'error':0 
        }

def check_lifetime_stats(uid,first_name):
    if not uid in LifetimeStats:
        LifetimeStats[uid] = {
            'fname':first_name,
            'correct':0,
            'error':0
        }

def sort_leaderboards(chatid,WLB,uids):

    Leaderboard = ""
    Title = ""
    Placement = 1 
    PlayerStatus = []

    if WLB == "QLB" or WLB == "LTLB":
        for uid in uids:
            if WLB == "QLB":
                PlayerStatus.append({
                    'uid': uid,
                    'correct': games[chatid]['users'][uid]['correct']['count'],
                    'error': games[chatid]['users'][uid]['error'],
                    'fname': games[chatid]['users'][uid]['fname']
                    })
            elif WLB == "LTLB":
                PlayerStatus.append({
                    'uid': uid,
                    'correct': LifetimeStats[uid]['correct'],
                    'error': LifetimeStats[uid]['error'],
                    'fname': LifetimeStats[uid]['fname']
                    })

        PlayerStatus.sort(key=errors,reverse=False)
        PlayerStatus.sort(key=correctAnswers,reverse=True)

        title = ["🥇 #1","🥈 #2","🥉 #3"]

        for EachPlayer in PlayerStatus:  
            if Placement > 3:
                Leaderboard += f"「{Placement}𝘁𝗵 𝗽𝗹𝗮𝗰𝗲」 ✨ {EachPlayer['fname']} | ✅ {EachPlayer['correct']} 次正确 ❌ {EachPlayer['error']} 次错误\n"
            else:
                for Num in range(1,4):
                    if Placement == Num:
                        Title = title[Num-1]
                Leaderboard += f"「{Title}」 ✨ {EachPlayer['fname']} | ✅ {EachPlayer['correct']} 次正确 ❌ {EachPlayer['error']} 次错误\n"
            Placement += 1

    elif WLB == "QCAT":
        for uid in uids:
            for answer in games[chatid]['users'][uid]['correct']['answer']:
                AccTime = answer[1] - games[chatid]['time']
                ToSeconds = str(AccTime)[:-7]
                PlayerStatus.append({
                        'AccTime': float(str(AccTime).replace(":","")),
                        'time':ToSeconds,
                        'uid':uid,
                        'answer':answer[0],
                        'fname':games[chatid]['users'][uid]['fname']
                    })
        
        PlayerStatus.sort(key=times,reverse=False)

        title = ["🥇 𝗚𝗼𝗹𝗱","🥈 𝗦𝗶𝗹𝘃𝗲𝗿","🥉 𝗕𝗿𝗼𝗻𝘇𝗲"]

        for EachPlayer in PlayerStatus:  
            if Placement != 1 and Placement != 2 and Placement != 3:
                Leaderboard += f"「{Placement}𝘁𝗵 𝗮𝗻𝘀𝘄𝗲𝗿」{EachPlayer['fname']}  ✔︎  {EachPlayer['answer']} ⏱ ({EachPlayer['time']})\n"
            else:
                for Num in range(1,4):
                    if Placement == Num:
                        Title = title[Num-1]
                Leaderboard += f"「{Title}」{EachPlayer['fname']}  ✔︎  {EachPlayer['answer']} ⏱ ({EachPlayer['time']})\n"
            Placement += 1

    return Leaderboard 
    
def detective_system(answer,cards):
    Cheat = False
    Numbers = list(dict.fromkeys(re.findall(r'\d+', answer)))

    modsAnswer = answer.replace("+","_").replace("-","_").replace("*","_").replace("/","_")
    numberCount = modsAnswer.split("_")

    modbAnswer = answer.replace("(","_").replace(")","_")
    bracketCount = modbAnswer.split("_")

    if not len(numberCount) == 4:
        Cheat = True
    for number in Numbers:
        if not int(number) in cards:
            Cheat = True
    for every in range(1,10):
        if f"({every})" in answer:
            Cheat = True
    if ("(((" in answer or ")))" in answer) or ("((" in answer and "))" in answer) or len(bracketCount) >= 6:
        Cheat = True
    try:
        if answer.endswith(')') and answer.startswith('('):
            if eval(answer.lstrip('(').rstrip(')')) == eval(answer):
                Cheat = True
    except SyntaxError:
        pass
    return Cheat

def start(update,context): 
    uid = str(update.effective_user.id)
    fname = str(update.effective_user.first_name)
    chatid = update.effective_chat.id
    cards = random.choices(range(1,10),k=4) 
    set_games_cards(chatid,cards,uid,fname)
    while answer(chatid)[0] == "":
        cards = random.choices(range(1,10),k=4) 
        set_games_cards(chatid,cards,uid,fname)
    update.effective_message.reply_text(f" {help()} \n\n四个数字分别是：") 
    context.bot.send_message(chatid, text=f"{cards[0]}, {cards[1]}, {cards[2]}, {cards[3]}")

    if random.choice(range(1,4)) == 2:
        context.bot.send_photo(chatid, photo=open(f'{config.run_path}/imgs/re.png', 'rb'), caption= "⚠️ 温馨提示：请把 Telegram 自动表情给关掉！Reminder: Please turn off Telegram's automatic emoji replacement!")

    


def question(update,context):
    first_name = update.effective_user.first_name
    uid = str(update.effective_user.id)
    chatid = update.effective_chat.id

    try:
        check_user(uid,chatid,first_name)
        update.effective_message.reply_text(f"""当前卡牌/Current cards：{games[chatid]['cards']}
-------------------
目前的正确答案/Current right answers：
                                            
{sort_leaderboards(chatid,"QCAT",games[chatid]['users'])}
-------------------
个人排行榜/GameQ leaderboard：

{sort_leaderboards(chatid,"QLB",games[chatid]['users'])}

-------------------
如想看您的终身统计，请使用 /gamel@CodePracticeBot /If you want to see your lifetime stats, please use /gamel@CodePracticeBot
""")
    except KeyError:
        update.effective_message.reply_text("目前没有被开启的游戏。/gamestart24 来开启一个游戏。There are currently no games opened. /gamestart24 to start a game.")

def end(update,context):
    chatid = update.effective_chat.id
    try:
        update.message.reply_text(f"游戏结束。/gamestart24 来开启一个游戏。\n\n所有的正确答案：\n\n{answer(chatid)[0]}")
        for i in range(1,7):
            if not answer(chatid)[i] == "":
                context.bot.send_message(chatid,text=answer(chatid)[i])
        del games[chatid]
    except KeyError:
        update.effective_message.reply_text("目前没有被开启的游戏。/gamestart24 来开启一个游戏。")
        
def rules(update,context):
    update.message.reply_text(help())

def List_Lifetime_Stats(update,context):
    update.message.reply_text(sort_leaderboards(update.effective_chat.id,"LTLB",LifetimeStats))

def answer(chatid):
    cards = [
        games[chatid]['cards'][0],
        games[chatid]['cards'][1],
        games[chatid]['cards'][2],
        games[chatid]['cards'][3]
        ]
    cards.sort()

    AllPossibleCombs = []

    correctAnswers = ""
    correctAnswers2 = ""
    correctAnswers3 = ""
    correctAnswers4 = ""
    correctAnswers5 = ""
    correctAnswers6 = ""
    correctAnswers7 = ""
    correctAnswers8 = ""

    count = 1

    for n1 in cards:
        for n2 in cards:
            for n3 in cards:
                for n4 in cards:
                    comb = [n1,n2,n3,n4]
                    comb.sort()
                    if comb == cards and not f"{n1} f {n2} s {n3} t {n4}" in AllPossibleCombs:
                        AllPossibleCombs.extend([
                            f"{n1} f {n2} s {n3} t {n4}",
                            f"({n1} f {n2}) s {n3} t {n4}", f"{n1} f ({n2} s {n3}) t {n4}", f"{n1} f {n2} s ({n3} t {n4})",
                            f"(({n1} f {n2}) s {n3}) t {n4}", f"({n1} f ({n2} s {n3})) t {n4}", f"{n1} f (({n2} s {n3}) t {n4})", f"{n1} f ({n2} s ({n3} t {n4}))",
                            f"({n1} f {n2}) s ({n3} t {n4})",
                            f"({n1} f {n2} s {n3}) t {n4}", f"{n1} f ({n2} s {n3} t {n4})"
                            ]) 
    symbols = ["+","-","*","/"]
    for each in AllPossibleCombs:
        for s1 in symbols:
            for s2 in symbols:
                for s3 in symbols:
                    e = each.replace("f",s1).replace("s",s2).replace("t",s3)
                    try:
                        answer = eval(e)
                        if answer == 24:
                            if count < 81:
                                correctAnswers += f"{count} ✔︎ {e} = 24\n"
                            elif count < 161:
                                correctAnswers2 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 241:
                                correctAnswers3 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 321:
                                correctAnswers4 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 401:
                                correctAnswers5 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 481:
                                correctAnswers6 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 561:
                                correctAnswers7 += f"{count} ✔︎ {e} = 24\n"
                            elif count < 641:
                                correctAnswers8 += f"{count} ✔︎ {e} = 24\n"
                            count += 1
                    except ZeroDivisionError:
                        pass
    return [
        correctAnswers,
        correctAnswers2,
        correctAnswers3,
        correctAnswers4,
        correctAnswers5,
        correctAnswers6,
        correctAnswers7,
        correctAnswers8
        ]


def proc_text(update,context):
    first_name = update.effective_user.first_name
    chatid = update.effective_chat.id
    uid = str(update.effective_user.id)    
    msg = ""
    answer = update.message.text.replace(".","").replace("（","(").replace("）",")").replace(" ","").replace("x","*").replace("[","(").replace("]",")").replace("×","*").replace("÷","/")
    if answer[0].isdigit() or answer[0] == "(":
        try: 
            cards = games[chatid]['cards']
            check_user(uid,chatid,first_name)
            check_lifetime_stats(uid,first_name)
            if not answer in games[chatid]['totalanswers']:
                try:
                    if detective_system(answer,cards) == False:
                        if int(eval(answer)) == 24:
                            msg = f"🎉 {first_name} 答对啦！{first_name} got it right!" 
                            games[chatid]['users'][uid]['correct']['count'] += 1
                            LifetimeStats[uid]['correct'] += 1
                            games[chatid]['users'][uid]['correct']['answer'].append([answer,datetime.datetime.now()])
                            games[chatid]['totalanswers'].append(answer)
                        else:  
                            msg = f"❌🤦 {first_name} 答错啦！{first_name} got it COMPLETELY WRONG!"
                            games[chatid]['users'][uid]['error'] += 1
                            LifetimeStats[uid]['error'] += 1
                    else:
                        games[chatid]['users'][uid]['error'] += 1
                        LifetimeStats[uid]['error'] += 1
                        msg = f"❌🤦 请使用我给你的那几个数字，只用三个加减乘除的符号，并且不要使用不必要的括号！需有查看更多规则，请查看 /gamerules。Please use the numbers I gave you, use only three symbols for addition, subtraction, multiplication, and division, and don't use unnecessary parentheses! For more rules, please check /gamerules."                                                                                                                    
                except:
                    msg = f"❌🤦 {first_name} 答错啦！您的目标是尝试去使用 {games[chatid]['cards']} 来算出 24.\n请记住, 您只能使用 +, -, *, / 和 ()。{first_name} got it wrong! Your goal is to try to use {games[chatid]['cards']} to calculate 24.\nRemember, you can only use +, -, *, / and ()."
                    games[chatid]['users'][uid]['error'] += 1
                    LifetimeStats[uid]['error'] += 1
            else:
                msg = f"{first_name}, 某某人已经说出来您的答案啦！{first_name}, someone has already said your answer!"
        except KeyError:
            msg = "目前没有被开启的游戏。/gamestart24 来开启一个游戏。There are currently no games opened. /gamestart24 to start a game."
        update.effective_message.reply_text(msg)
    twconfig.save_config()

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('gamestart24', start))
    dp.add_handler(CommandHandler('gameq', question))
    dp.add_handler(CommandHandler('gameend24', end))
    dp.add_handler(CommandHandler('gamerules', rules))
    dp.add_handler(CommandHandler('gamel',List_Lifetime_Stats))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command) & Filters.chat_type.groups,proc_text))
    return [
        BotCommand('gamestart24','开始一个24点游戏'),
        BotCommand('gameq','查询当前进行中的24点游戏'),
        BotCommand('gameend24','结束当前进行的游戏'),
        BotCommand('gamerules','查询24点的游戏规则'),
        BotCommand('gamel','查询总排行榜')
        ]
