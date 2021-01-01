import random
from datetime import datetime,timedelta
from telegram.ext import Dispatcher,CommandHandler
from telegram import BotCommand

# {
#   uid : {
#       'name': first_name,
#       'coins': 123,
#       'dailytime' : time
#       'hp' : 56
#       'items' : ["herring","trout","shark","boar","fox","deer","skunk","basilisk"]
#       }
# }

coins = config.CONFIG["coins"]

def save():
    config.CONFIG["coins"] = coins
    config.save_config()

def check_user(user):
    uid = str(user.id)
    first_name = user.first_name
    if not uid in coins.keys():
        coins[uid] = {'name':first_name,'coins':0,'dailytime':datetime.now().strftime("%Y/%m/%d %H:%M:%S"),'hourlytime':datetime.now().strftime("%Y/%m/%d %H:%M:%S"),'hp':100,'items':[]}
        save()

def check_hp(user):
    check_user(user)
    uid = str(user.id)
    if coins[uid]['hp'] == 0:
        coins[uid]['coins'] = 0
        coins[uid]['hp'] = 100
        save()

def show_user(user):
    uid = str(user.id)
    check_user(user)
    #  老房东(10):200
    return f"{coins[uid]['name']}, you have {coins[uid]['coins']} GP and {coins[uid]['hp']} HP\n{coins[uid]['name']}, 你有 {coins[uid]['coins']} GP 和 {coins[uid]['hp']} HP"

def add_coins(user,c):
    check_user(user)
    uid = str(user.id)
    coins[uid]['coins'] += c
    save()

def add_hp(user,c):
    check_user(user)
    uid = str(user.id)
    if c == -100:
        coins[uid]['hp'] = 0
        check_hp(user)
    else:
        coins[uid]['hp'] += c
        check_hp(user)
    save()

def hourly(update,context):
    user = update.effective_user
    check_user(user)
    uid = str(user.id)
    hourlytime = datetime.strptime(coins[uid]['hourlytime'],"%Y/%m/%d %H:%M:%S")
    if datetime.now() > hourlytime:
        c = random.randint(50,200)
        coins[uid]['coins'] += c
        hourlytime = datetime.now() + timedelta(hours=1)
        update.message.reply_text("Here are your hourly coins, %s\n%s coins were placed in your wallet."%(user.first_name,c))
    else:
        update.message.reply_text("Slow it down, cmon!!! I'm not made of money dude, one hour hasn't passed yet!")
    coins[uid]['hourlytime'] = hourlytime.strftime("%Y/%m/%d %H:%M:%S")
    save()

def daily(update,context):
    user = update.effective_user
    check_user(user)
    uid = str(user.id)
    dailytime = datetime.strptime(coins[uid]['dailytime'],"%Y/%m/%d %H:%M:%S")
    if datetime.now() > dailytime:
        c = random.randint(500,2000)
        coins[uid]['coins'] += c
        dailytime = datetime.now() + timedelta(hours=24)
        update.message.reply_text("Here are your daily coins, %s\n%s coins were placed in your wallet."%(user.first_name,c))
    else:
        update.message.reply_text("Slow it down, cmon!!! I'm not made of money dude, one day hasn't passed yet!")
    coins[uid]['dailytime'] = dailytime.strftime("%Y/%m/%d %H:%M:%S")    
    save()

def shop(update, context):
    user = update.effective_user
    check_user(user)
    markets = ["Walmart","Costco","Super C","Central Supermarket+"]
    if len(context.args) == 0:
        update.message.reply_animation('https://media1.giphy.com/media/fAhOtxIzrTxyE/200.gif',caption="""Here are some stuff you can buy at %s.
FOOD:
--------------------------------------
Buy apples! 🍎:
Description: An apple a day keeps the doctors away! When you eat one, gain 10HP!
500GP per 🍎
/shop apple
--------------------------------------
Buy brocolis! 🥦:
Description: Eat your vegetables, it's actually good for you, you can gain 20HP!
900GP per 🥦
/shop brocoli
--------------------------------------
Buy ramen! 🍜:
Description: Good hot ramen is great for your health! You can gain 35HP per bowl!
1500GP per 🍜
/shop ramen
--------------------------------------
Buy Super Interesting Magic Potions! 🍾:
Description: Several Snap has developed a new potion that actually doesn't kill you! Instead, it makes you gain 50HP!
2000GP per 🍾
/shop simp
"""%(random.choice(markets)))
    elif context.args[0] == "apple":
        update.message.reply_text("%s"%buy_stuff(user,"apple",500))
    elif context.args[0] == "brocoli":
        update.message.reply_text("%s"%buy_stuff(user,"brocoli",900))
    elif context.args[0] == "ramen":
        update.message.reply_text("%s"%buy_stuff(user,"ramen",1500))
    elif context.args[0] == "simp":
        update.message.reply_text("%s"%buy_stuff(user,"simp",2000))
    else:
        update.message.reply_text("Bruh this item doesn't even exist")

def eat(update, context):
    user = update.effective_user
    check_user(user)
    if len(context.args) == 0:
        update.message.reply_animation('https://i.gifer.com/RjWn.gif',caption="""Enjoy your meal! What are you eating tho?
/eat apple for a nice juicy red apple.
/eat brocoli for some ugly green miniature trees.
/eat ramen to enjoy some delicious noodles in soup.
/eat simp to drink Several Snap's new potion.""")
    elif context.args[0] == "apple":
        update.message.reply_text("%s"%eat_stuff(user,"apple",10))
    elif context.args[0] == "brocoli":
        update.message.reply_text("%s"%eat_stuff(user,"brocoli",20))
    elif context.args[0] == "ramen":
        update.message.reply_text("%s"%eat_stuff(user,"ramen",35))
    elif context.args[0] == "simp":
        update.message.reply_text("%s"%eat_stuff(user,"simp",50))
        
def eat_stuff(user,aliment,c):
    uid = str(user.id)
    hpmax = coins[uid]['hp'] - c
    if aliment == "apple" or aliment == "brocoli" or aliment == "ramen" or aliment == "simp":
        for item in coins[uid]['items']:
            if item == aliment:
                if coins[uid]['hp'] < hpmax:
                    coins[uid]['items'].remove(item)
                    coins[uid]['hp'] += c
                elif coins[uid]['hp'] >= hpmax and coins[uid]['hp'] < 100:
                    coins[uid]['items'].remove(item)
                    coins[uid]['hp'] = 100
                elif coins[uid]['hp'] >= 100:
                    return "Bruh your HP is maxed out, try losing some."
                save()
                return "You ate/drank a/an/some %s! Gain %sHP."%(aliment,c)
            else:
                return "You do not own this item lol"
    else:
        return "Bruh this item doesn't even exist"

def show_items(update,context):
    user = update.effective_user
    check_user(user)
    uid = user.id
    update.message.reply_text("%s"%coins[uid]['items'])

def buy_stuff(user,object,c):
    uid = str(user.id)
    if coins[uid]['coins'] < c:
        return "No disrespect but... LMFAO ur so poor u need %s more GP "%(c-coins[uid]['coins'])
    coins[uid]['items'].append(object)
    coins[uid]['coins'] -= c
    save()
    return "Success! You have bought a/an/some %s! You still have %s GP."%(object,coins[uid]['coins'])

def convert(update,context):
    user = update.effective_user
    uid = user.id
    if len(context.args) == 0:
        update.message.reply_animation('https://thumbs.gfycat.com/AliveWelloffAtlanticspadefish-max-1mb.gif',caption="""What are you about to convert?
/convert gptofc {amount of GP} : Convert 5 GP into 1 fishcoin!
/convert gptobc {amount of GP} : Convert 5 GP into 1 beastcoin!
/convert fctobc {amount of fishcoins} : Convert 1 fishcoin into 1 beastcoin!
/convert bctofc {amount of beastcoins} : Convert 1 beastcoin into 1 fishcoin!
/convert fctogp {amount of fishcoins} : Convert 1 fishcoin into 5 GP!
/convert bctogp {amount of beastcoins} : Convert 1 beastcoin into 5 GP!""")
    elif context.args[0] == "gptofc":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > coins[str(uid)]['coins']:
                update.message.reply_text("Ur too poor u can't convert that many GP")
            elif int(context.args[1]) <= 0 or int(context.args[1]) % 5 != 0:
                update.message.reply_text("You need to enter a valid amount that can be divisible by 5!")
            else:
                add_coins(user,-(int(context.args[1])))
                fish.fishgame[str(uid)]['fcoins'] += int(int(context.args[1]) / 5)
                update.message.reply_text("Success! You now have %s GP and %s fishcoins!"%(coins[str(uid)]['coins'],fish.fishgame[str(uid)]['fcoins']))
        else:
            update.message.reply_text("You need to enter a valid amount!")
    elif context.args[0] == "gptobc":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > coins[str(uid)]['coins']:
                update.message.reply_text("Ur too poor u can't convert that many GP")
            elif int(context.args[1]) <= 0 or int(context.args[1]) % 5 != 0:
                update.message.reply_text("You need to enter a valid amount that can be divisible by 5!")
            else:
                add_coins(user,-(int(context.args[1])))
                hunt.huntgame[str(uid)]['bcoins'] += int(int(context.args[1]) / 5)
                update.message.reply_text("Success! You now have %s GP and %s beastcoins!"%(coins[str(uid)]['coins'],hunt.huntgame[str(uid)]['bcoins']))
    elif context.args[0] == "fctobc":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > fish.fishgame[str(uid)]['fcoins']:
                update.message.reply_text("Ur too poor u can't convert that many fishcoins")
            elif int(context.args[1]) <= 0:
                update.message.reply_text("You need to enter a valid amount")
            else:
                fish.fishgame[str(uid)]['fcoins'] -= int(context.args[1])
                hunt.huntgame[str(uid)]['bcoins'] += int(context.args[1])
                update.message.reply_text("Success! You now have %s fishcoins and %s beastcoins!"%(fish.fishgame[str(uid)]['fcoins'],hunt.huntgame[str(uid)]['bcoins']))
        else:
            update.message.reply_text("You need to enter a valid amount!")
    elif context.args[0] == "bctofc":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > hunt.huntgame[str(uid)]['bcoins']:
                update.message.reply_text("Ur too poor u can't convert that many beastcoins")
            elif int(context.args[1]) <= 0:
                update.message.reply_text("You need to enter a valid amount")
            else:
                fish.fishgame[str(uid)]['fcoins'] += int(context.args[1])
                hunt.huntgame[str(uid)]['bcoins'] -= int(context.args[1])
                update.message.reply_text("Success! You now have %s fishcoins and %s beastcoins!"%(fish.fishgame[str(uid)]['fcoins'],hunt.huntgame[str(uid)]['bcoins']))
        else:
            update.message.reply_text("You need to enter a valid amount!")
    elif context.args[0] == "fctogp":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > fish.fishgame[str(uid)]['fcoins']:
                update.message.reply_text("Ur too poor u can't convert that many fishcoins")
            elif int(context.args[1]) <= 0:
                update.message.reply_text("You need to enter a valid amount")
            else:
                add_coins(user,int(int(context.args[1]) * 5))
                fish.fishgame[str(uid)]['fcoins'] -= int(context.args[1])
                update.message.reply_text("Success! You now have %s GP and %s fishcoins!"%(coins[str(uid)]['coins'],fish.fishgame[str(uid)]['fcoins']))
        else:
            update.message.reply_text("You need to enter a valid amount!")
    elif context.args[0] == "bctogp":
        if len(context.args) == 1:
            update.message.reply_text("You need to enter a valid amount!")
        elif context.args[1].isdigit():
            if int(context.args[1]) > hunt.huntgame[str(uid)]['bcoins']:
                update.message.reply_text("Ur too poor u can't convert that many fishcoins")
            elif int(context.args[1]) <= 0:
                update.message.reply_text("You need to enter a valid amount")
            else:
                add_coins(user,int(int(context.args[1]) * 5))
                hunt.huntgame[str(uid)]['bcoins'] -= int(context.args[1])
                update.message.reply_text("Success! You now have %s GP and %s beastcoins!"%(coins[str(uid)]['coins'],hunt.huntgame[str(uid)]['bcoins']))
        else:
            update.message.reply_text("You need to enter a valid amount!")

def get_coins(update, context):
    user = update.effective_user
    check_user(user)
    update.message.reply_animation('https://media4.giphy.com/media/3Z1basZxa2mGOSPBzR/200_d.gif',caption=f"{show_user(user)}")

def get_command():
    return [
        BotCommand('bal','Check the amount of money you have. // 检查您有多少GP。'),
        BotCommand('daily','Get daily GP! // 每日打卡！'),
        BotCommand('hourly','Get hourly GP! // 每小时打卡！'),
        BotCommand('shop',' Buy nice useful stuff! // 购买有用的东西！'),
        BotCommand('eat','Eat to gain HP // 吃东西来增加HP'),
        BotCommand('inv','[BETA] Check the items you have in your inventory. // [测试] 检查库存中的物品。'),
        BotCommand('convert','Convert one currency into another! // 将一种货币转换为另一种货币！')]

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('bal', get_coins))
    dp.add_handler(CommandHandler('daily', daily))
    dp.add_handler(CommandHandler('hourly', hourly))
    dp.add_handler(CommandHandler('shop', shop))
    dp.add_handler(CommandHandler('eat', eat))
    dp.add_handler(CommandHandler('inv', show_items))
    dp.add_handler(CommandHandler('convert', convert))
