from telegram.ext import Dispatcher,CommandHandler,MessageHandler,Filters
from telegram import BotCommand,Update
import random
import re
from datetime import datetime

games = {}

def myFunc(e):
    return e['correct']

def check(solution):
    try:
        if eval(solution) == 24:
            return True
        return False
    except ZeroDivisionError:
        return False

def get_numbers():
    numbers = []
    for a in range(0,4):
        for b in range(0,4):
            for c in range(0,4):
                for d in range(0,4):
                    if a == b or b == c or c == d or a == c or a == d or b == d:
                        pass
                    else:
                        numbers.append([a,b,c,d])
    return numbers

def add_solution(solution,solutions):
    if check(solution) == True:
        if not solution in solutions:
            solutions.append(solution)

def get_answers(cards):
    operations = ['+','-','*','/']
    if len(cards) != 4:
        return []
    solutions = []
    for i in operations:
        for j in operations:
            for k in operations:
                for indexlist in get_numbers():
                    solution = f'(({cards[indexlist[0]]} {i} {cards[indexlist[1]]}) {j} {cards[indexlist[2]]}) {k} {cards[indexlist[3]]}'
                    add_solution(solution,solutions)
                    solution = f'{cards[indexlist[0]]} {i} (({cards[indexlist[1]]} {j} {cards[indexlist[2]]}) {k} {cards[indexlist[3]]})'
                    add_solution(solution,solutions)
                    solution = f'({cards[indexlist[0]]} {i} ({cards[indexlist[1]]} {j} {cards[indexlist[2]]})) {k} {cards[indexlist[3]]}'
                    add_solution(solution,solutions)
                    solution = f'{cards[indexlist[0]]} {i} ({cards[indexlist[1]]} {j} ({cards[indexlist[2]]} {k} {cards[indexlist[3]]}))'
                    add_solution(solution,solutions)
                    solution = f'({cards[indexlist[0]]} {i} {cards[indexlist[1]]}) {j} ({cards[indexlist[2]]} {k} {cards[indexlist[3]]})'
                    add_solution(solution,solutions)
    return solutions

def set_games_cards(chatid,cards):
    games[chatid] = {'answers':[],'users':{},'time':datetime.now()}
    games[chatid]['cards'] = cards

def add_player(user,chatid):
    uid = user.id
    if not chatid in games:
        games[chatid] = {'answers':[],'users':{}}
    if not uid in games[chatid]['users']:
        games[chatid]['users'][uid] = {'correct':0,'incorrect':0,'fname':user.first_name}

def add_answer(chatid,answer,user,timeused):
    if not chatid in games:
        games[chatid] = {'answers':[],'users':{}}
    if not 'answers' in games[chatid]:
        games[chatid]['answers'] = []
    games[chatid]['answers'].append([answer,user,timeused])

def remove_games_cards(chatid):
    games[chatid] = {}

def start(update,context):
    chatid = update.effective_chat.id
    cards = [1,2,3,4,5,6,7,8,9,10]
    putcards = random.choices(cards,k=4)
    update.message.reply_text(f'{putcards[0]},{putcards[1]},{putcards[2]},{putcards[3]}')
    set_games_cards(chatid,putcards)

def rules(update,context):
    update.message.reply_text('''Welcome to 24! Your goal is to figure out how to make 24 with these numbers ( /q@sicheng24bot ).
Remember, you can only use the basic operations. They are to be typed like this: +, -, *, /. Parentheses are allowed.
Good Luck! Or is it luck?''')

def question(update,context):
    chatid = update.effective_chat.id
    msg = ""
    lead = ""
    dict1 = []
    if not chatid in games:
        update.effective_message.reply_text("There is no game currently. Use /start24@sicheng24bot to start a game.")
        return
    if games[chatid]['users'] == {}:
        update.effective_message.reply_text(f"Current cards: {games[chatid]['cards']}. There are no answers currently.")
        return
    for uid in games[chatid]['users']:
        dict1.append({'correct':float(f"{games[chatid]['users'][uid]['correct']}.{100000-games[chatid]['users'][uid]['incorrect']}"),'fname':games[chatid]['users'][uid]['fname'],'uid':uid})
    dict1.sort(key=myFunc,reverse=True)
    count = 0
    countTrans = ['','🥇','🥈','🥉']
    for persondict in dict1:
        count += 1
        if count >= 4:
            countEmoji = ''
        else:
            countEmoji = countTrans[count]
        lead += f"\n{countEmoji} {count}. {persondict['fname']}: ✅ {games[chatid]['users'][persondict['uid']]['correct']} times correct ❌ {games[chatid]['users'][persondict['uid']]['incorrect']} times incorrect"
    anscount = 1
    if games[chatid]['answers'] == []:
        msg = "\nThere are currently no right answers."
    else:
        ansTrans = ['','st answer','nd answer','rd answer']
        for answer in games[chatid]['answers']:
            if anscount >= 4:
                anstxt = 'th answer'
                ansemoji = ''
            else:
                anstxt = ansTrans[anscount]
                ansemoji = countTrans[anscount]
            msg += f"\n☑️ {answer[1].first_name}: {ansemoji}{anscount}{anstxt}: {answer[0]} ⏱ {answer[2]}"
            anscount += 1
    update.effective_message.reply_text(f"""Current cards: {games[chatid]['cards']}
--------------------
Current (right) answers{msg}
--------------------
Leaderboard:{lead}
""")

def end(update,context):
    chatid = update.effective_chat.id
    solutions = get_answers(games[chatid]['cards'])
    msg = f'There are {len(solutions)} answers to this question.'
    index = 0
    update.message.reply_text('The game is now ended. Use /start24@sicheng24bot to start a new game.')
    for answer in solutions:
        index += 1
        msg += f'\n{index}. {answer}'
    update.message.reply_text(msg)
    remove_games_cards(chatid)

def answer(update,context):
    chatid = update.effective_chat.id
    user = update.effective_user
    uid = user.id
    add_player(user,chatid)
    if not chatid in games:
        update.message.reply_text('There is no game currently. Use /start24@sicheng24bot to start a game.')
        return
    if not 'cards' in games[chatid]:
        update.message.reply_text('There is no game currently. Use /start24@sicheng24bot to start a game.')
        return
    cards = games[chatid]['cards']
    valid = True
    msg = update.message.text.replace(".","").replace(" ","").replace('x','*')
    numbers = []
    signs = []
    if msg[0].isdigit() or msg[0]== "(":
        for thing in msg:
            if thing != '*' and thing != '+' and thing != '-' and thing != '/' and thing != '(' and thing != ')':
                if not thing.isnumeric():
                    valid = False
        for character in msg:
            if character.isdigit():
                numbers.append(character)
        index = 1
        for number in numbers:
            try:
                if numbers[index-1] == '1' and numbers[index] == '0':
                    numbers[index-1] = '10'
                    numbers.remove(numbers[index])
                index += 1
            except IndexError:
                pass
        for character in msg:
            if character == '*' or character == '+' or character == '/' or character == '-':
                signs.append(character)
        if len(signs) > 3 or len(signs) < 3:
            update.message.reply_text("You must use the basic operations (+,-,*,/) 3 times only!")
            return
        for number in numbers:
            if not int(number) in cards:
                valid = False
        if valid == False:
            games[chatid]['users'][uid]['incorrect'] += 1
            update.message.reply_text(f"You must use the basic operations (+,-,*,/) and the numbers from the list I gave you! (/q@sicheng24bot) For more information, please check the rules of the game here: /rules@sicheng24bot\n{update.effective_user.first_name}, you now have {games[chatid]['users'][uid]['correct']} correct answers and {games[chatid]['users'][uid]['incorrect']} incorrect answers.")
            return
        if len(numbers) != 4:
            games[chatid]['users'][uid]['incorrect'] += 1
            update.message.reply_text(f"You must use the numbers from the list I gave you, and only once! (/q@sicheng24bot) For more information, please check the rules of the game here: /rules@sicheng24bot\n{update.effective_user.first_name}, you now have {games[chatid]['users'][uid]['correct']} correct answers and {games[chatid]['users'][uid]['incorrect']} incorrect answers.")
            return
        if eval(msg) == 24:
            for answerlist in games[chatid]['answers']:
                if msg in answerlist:
                    update.message.reply_text('Someone already said that answer!')
                    return
            timenow = datetime.now()
            timedifference = timenow-games[chatid]['time']
            timeused = f'{int(timedifference.total_seconds()/60/24)}:{int(timedifference.total_seconds()/60)}:{int(timedifference.total_seconds()%60)}'
            games[chatid]['users'][uid]['correct'] += 1
            update.message.reply_text(f"🎉 You did it! {update.effective_user.first_name}, you now have {games[chatid]['users'][uid]['correct']} correct answers and {games[chatid]['users'][uid]['incorrect']} incorrect answers.")
            add_answer(chatid,msg,user,timeused)
        else:
            games[chatid]['users'][uid]['incorrect'] += 1
            update.message.reply_text(f"🤦🐛 You are a big bug! {update.effective_user.first_name}, you now have {games[chatid]['users'][uid]['correct']} correct answers and {games[chatid]['users'][uid]['incorrect']} incorrect answers.")

def get_command():
    return [
        BotCommand('start24','开始一个24点游戏'),
        BotCommand('q','查询当前进行中的24点游戏'),
        BotCommand('end24','结束当前进行的游戏'),
        BotCommand('rules','规矩~')
    ]

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('start24', start))
    dp.add_handler(CommandHandler('q', question))
    dp.add_handler(CommandHandler('end24', end))
    dp.add_handler(CommandHandler('rules', rules))
    dp.add_handler(MessageHandler(Filters.chat_type.supergroup & Filters.text, answer))