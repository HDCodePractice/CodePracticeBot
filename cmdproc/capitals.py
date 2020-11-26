from telegram import InlineKeyboardButton, InlineKeyboardMarkup,BotCommand
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
import random
import coins

#  ==================================================
#  start
#  /capitals
# 
#  ==================================================
#  help
#  这是 老房东 的 capitals game
#  helpmsg
#  |  easy  |  normal  |   hard   | extreme |
# 
#  ==================================================
#  question
#  这是 老房东 的 capitals game
#  What is the capital of...
#  a.lasdf;aljflasj
#  b.alfj;aljfd;laj
#  c.aflfj;lfjal;fdjla;k
#  d.dszfsfdsfsd'
#  | a | b | c | d | 我也要参加 |
#  
#  ==================================================
#  final
#  这是 老房东 的 capitals game 数据 
#  easy 答对xx次/xx次 | hard答对xx/xx次
#  | easy 再来一题? | 换一个级别 | 我也要参加 |
#  ==================================================
# 
#  show_alert: 如果你也想玩，发 /capitals


# kb1 = [
#     {
#     "text":"callbackdata",
#     "text2":"callbackdata2"
#     },
#     {
#         "text3":"callbackdata3"
#     }
# ]

# def init_markup_new(kb):
#     kb1 = [
#     {
#     "text":"callbackdata",
#     "text2":"callbackdata2"
#     },
#     {
#         "text3":"callbackdata3"
#     }]


countries = {
    'easy':{
        "🇫🇷 France // 法国 🇫🇷" : {
            "yes":"Paris // 巴黎",
            "no":["Calais // 加来","Marseilles // 马赛","Versailles // 凡尔赛","Québec // 魁北克"],
            "haha":["thE eIFFel ToWEr obVioUSlY // 当然是诶福尔铁塔啦～","Macron City // 马克龙城","Beaconsfield // 比肯斯菲尔德"]
        },
        "🇨🇦 Canada // 加拿大 🇨🇦" : {
            "yes":"Ottawa // 渥太华",
            "no":["Toronto // 多伦多","Kingston // 金斯敦","Vancouver // 温歌华"],
            "haha":["The North Pole HOHOHO // 北极……好冷啊","Beaconsfield // 比肯斯菲尔德"]
        },
        "🇨🇳 China // 中国 🇨🇳" : {
            "yes": "Beijing // 北京",
            "no":["Shanghai // 上海","Beijiing // 北进","Guangzhou // 广州"],
            "haha" : ["Centre City // 中城","Baconsfield // 培根之地"]
        },
        "🇬🇧 UK // 英国 🇬🇧" : {
            "yes": "London // 伦敦",
            "no":["Windsor // 温莎","Oxford // 牛津","Cambridge // 剑桥","Manchester // 曼切斯特"],
            "haha":["Small Ben? // 小本钟？？？","England's Beaconsfield // 英国的比肯斯菲尔德"]
        },
        "🇧🇷 Brazil // 巴西 🇧🇷" : {
            "yes": "Brasília // 巴西利亚",
            "no": ["São Paulo // 圣保罗","Rio de Janeiro // 里约热内卢","Fortaleza // 福塔莱萨"],
            "haha": ["Amazonia // 亚马逊，公司还是丛林？？？","Where the 2016 Olympics were held? // 2016年奥运举行的哪个地儿？","Beaconsfield // 比肯斯菲尔德"]
        },
        "🇰🇷 South Korea // 韩国 🇰🇷" : {
           "yes": "Seoul // 首尔",
           "no": ["Busan // 釜山", "Gwangzhou // 光州", "Incheon // 仁川"],
           "haha": ["A Place Where Kim-Jong-Un hates? // 金正恩讨厌的地方？","Beaconsfield // 比肯斯菲尔德"]
        },
        "🇷🇺 Russia // 俄罗斯 🇷🇺": {
            "yes": "Moscow // 莫斯科",
            "no": ["St-Petersburg // 圣彼得堡","Arkhangelsk // 阿尔汉格尔斯克","Volgograd // 伏尔加格勒"],
            "haha": ["Vladimirputingrad // 弗拉基米尔普丁格勒","USSR II City // 苏联II 城","Beaconsfield // 比肯斯菲尔德"]
        },
        "🇯🇵 Japan // 日本 🇯🇵": {
            "yes": "Tokyo // 东京",
            "no": ["Osaka // 大阪","Nagasaki // 长崎","Hiroshima // 广岛","Fukushima // 福岛"],
            "haha": ["Toyota City // 丰田城", "Beaconsfield // 比肯斯菲尔德"]
        },
        "🇺🇸 USA // 美国 🇺🇸": {
            "yes": "Washington DC // 华盛顿 DC",
            "no": ["New York // 纽约", "New Youk // 新约","Washington DD // 华盛顿 DD","Philadelphia // 费城"],
            "haha": ["The Place Where There Is A Very Messy Election? // 选举非常混乱的地方？","Beaconsfield // 比肯斯菲尔德"]
        }
    },
    'normal':{
        "🇸🇪 Sweden // 瑞典 🇸🇪" : {
            "yes": "Stockholm // 斯德哥尔摩",
            "no":["Hallashölm // 哈拉索尔姆","Göteborg // 哥德堡","Umeå // 梅阿"],
            "haha":["Malmö // 马尔默","Copenhaguen // 哥本哈根"]
        },
        "🇳🇴 Norway // 挪威 🇳🇴": {
            "yes": "Oslo // 奥斯陆",
            "no":["Helsinki // 赫尔辛基","Bergen // 卑尔根","Trondheim // 特隆赫姆"],
            "haha":["Bodø // 博德","Tromsø // 特罗姆瑟"]
        },
        "🇫🇮 Finland // 芬兰 🇫🇮": {
            "yes": "Helsinki // 赫尔辛基",
            "no": ["Turku // 图尔库","Oslo // 奥斯陆","Joensuu // 约恩苏"],
            "haha": ["Oulu // 奥卢","Tampere // 坦佩雷"]
        },
        "🇦🇺 Australia // 澳大利亚 🇦🇺": {
            "yes": "Canberra // 堪培拉",
            "no": ["Sydney // 悉尼","Melbourne // 墨尔本"],
            "haha": ["Perth // 珀斯","Brisbane // 布里斯班"]
        },
        "🇩🇰 Denmark // 丹麦 🇩🇰": {
            "yes": "Copenhaguen // 哥本哈根",
            "no": ["Stockholm // 斯德哥尔摩","Aarhus // 奥胡斯","Odense // 欧登塞"],
            "haha": ["Aalborg // 奥尔堡","Esbjerg // 埃斯比约"]
        },
        "🇩🇿 Algeria // 阿尔及利亚 🇩🇿" : {
            "yes": "Algiers // 阿尔及尔",
            "no": ["Ouargla // 瓦尔格拉","Constantine // 君士坦丁","Bejaïa // 贝贾亚"],
            "haha": ["Annaba // 安那巴","Oran // 奥兰"]
        }

    },
    'hard':{
        "🇻🇪 Venezuela // 委内瑞拉 🇻🇪" : {
            "yes": "Caracas // 加拉加斯",
            "no":["Maracaibo // 马拉开波","Barquisimeto // 巴基西梅托","Venezuelia // 委内瑞拉城"],
            "haha":["Valencia // 巴伦西亚"]
        },
        "🇨🇴 Colombia // 哥伦比亚 🇨🇴" : {
            "yes": "Bogotá // 波哥大",
            "no":["Barranquilla // 巴兰基亚","Medellín // 麦德林","Cartagena // 卡塔赫纳"],
            "haha":["Cali // 卡利","Montería // 蒙特里亚"]
        },
        "🇺🇦 Ukraine // 乌克兰 🇺🇦": {
            "yes": "Kiev // 基辅",
            "no": ["Odessa // 敖德萨", "Dnipropetrovsk // 第聂伯罗彼得罗夫斯克","Kharkiv // 哈尔科夫"],
            "haha": ["Chernobyl // 切尔诺贝利","Zaporizhia // 扎波罗热"]
        },
        "🇱🇻 Latvia // 拉脱维亚 🇱🇻": {
            "yes": "Riga // 里加",
            "no": ["Daugavpils // 陶格夫匹尔斯","Liepāja // 利耶帕亚"],
            "haha": ["Ventspils // 文茨皮尔斯","Rēzekne // 雷泽克内"]
        },
        "🇬🇪 Georgia // 格鲁吉亚 🇬🇪": {
            "yes": "Tbilisi // 第比利斯",
            "no" : ["Kutaisi // 库塔伊西","Batumi // 巴统"],
            "haha" : ["Borjomi // 博尔若米","Rustavi // 鲁斯塔维"] 
        }

    },
    'extreme':{
        "🇵🇬 Papua New Guinea // 巴布亚新几内亚 🇵🇬" : {
            "yes": "Port Moresby // 莫尔兹比港",
            "no":["Daru // 达鲁","Lae // 莱城"],
            "haha":["Jayapura // 查亚普拉"]
        },
        "🇸🇮 Slovenia 🇸🇮" : {
            "yes": "Ljubljana // 卢布尔雅那",
            "no":["Bratislava // 布拉迪斯拉发","Koper // 科珀","Maribor // 马里博尔"],
            "haha":["Velenje // 维伦耶","Koper // 科珀"]
        },
        "🇲🇰 North Macedonia // 马其顿 🇲🇰": {
            "yes": "Skopje // 斯科普里",
            "no": ["Podgorica // 波德戈里察","Bitola // 比托拉"],
            "haha": ["Ohrid // 奥赫里德","Prilep // 普里列普"]
        },
        "🇲🇪 Montenegro // 黑山 🇲🇪": {
            "yes": "Podgorica // 波德戈里察",
            "no": ["Skopje // 斯科普里","Nikšić // 尼克希奇"],
            "haha": ["Berane // 贝拉内","Kotor // 科托尔"]
        },
        "🇱🇹 Lithuania // 立陶宛 🇱🇹": {
            "yes": "Vilnius // 维尔纽斯",
            "no": ["Kaunas // 考纳斯","Šiauliai // 希奥利艾","Klaipėda // 克莱佩达"],
            "haha": ["Panevėžys // 帕内韦日斯","Palanga // 帕兰加"]
        }
    }
}

def init_q(choice,country,level,uid):
    buttons = []
    callbacks = []
    yesIndex = random.randint(0,2)
    no1 = random.choice(choice['no'])
    no2 = random.choice(choice['no'])
    while no1 == no2 :
        no2 = random.choice(choice['no'])
    no = [no1,no2]
    haha = random.choice(choice['haha'])
    yes = choice['yes']
    for i in range(3):
        if i == yesIndex:
            buttons.append(yes)
            # 我选a)fdgfdg
            callbacks.append("cap:-%s-%s-%s-%s"%(uid,yesIndex,i,level))
        else:
            buttons.append(no[0])
            callbacks.append("cap:-%s-%s-%s-%s"%(uid,yesIndex,i,level))
            no.remove(no[0])
    buttons.append(haha)
    callbacks.append("cap:-%s-%s-%s-%s"%(uid,yesIndex,3,level))
    #  "cap:-uid-1-2    cap:-uid-正确的答案-当前答案"
    #  "cap:-uid-1-1"
    msg = """What is the capital of %s?
A) %s
B) %s
C) %s
D) %s
------------------------
Please choose one:"""%(country,buttons[0],buttons[1],buttons[2],buttons[3])
    markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("A)",callback_data=callbacks[0]),
        InlineKeyboardButton("B)",callback_data=callbacks[1]),
        InlineKeyboardButton("C)",callback_data=callbacks[2]),
        InlineKeyboardButton("D)",callback_data=callbacks[3])
        ]])
    return msg,markup

def get_kb(update):
    uid = update.effective_user.id
    easy_button = InlineKeyboardButton('Easy // 简单模式',callback_data='caplvl:easy-%s'%uid)
    normal_button = InlineKeyboardButton('Normal // 普通模式',callback_data='caplvl:normal-%s'%uid)
    hard_button = InlineKeyboardButton('Hard // 困难模式',callback_data='caplvl:hard-%s'%uid)
    extreme_button = InlineKeyboardButton('Extreme // 地牢模式',callback_data='caplvl:extreme-%s'%uid)
    random_button = InlineKeyboardButton('Random // 随机模式',callback_data='caplvl:random-%s'%uid)
    restart_button = InlineKeyboardButton('Play again? // 再来一遍？',callback_data='capres:restart-%s'%uid)
    lvlskb = InlineKeyboardMarkup([[easy_button],[normal_button],[hard_button],[extreme_button],[random_button]])
    restartkb = InlineKeyboardMarkup([[restart_button]])
    return [lvlskb,restartkb]

def capitals_old(update,context):
    update.message.reply_text("""这是%s的游戏，如果你不叫%s，请不要乱点，请点 /capitals
-------------------------------
A general knowledge game! The bot will randomly generate a country and a number of answer choices, depending on your chosen difficulty level. The choices are as shown:
-------------------------------
- Easy : You are supposed to be cultivated enough to know these countries's capitals.
Rewards: 10GP per correct answer, lose 50GP per wrong answer.
-------------------------------
- Normal : Quite easy questions for those who have at least observed correctly a map.
Rewards: 25GP per correct answer, lose 20GP per wrong answer.
-------------------------------
- Hard : Quite hard countries, but most of which you have heard of, but probably not the capitals...
Rewards: 50GP per correct answer, lose 10GP per wrong answer.
-------------------------------
- Extreme : Countries you have never heard of! Big cash to win, though!
Rewards: 125GP per correct answer, lose 5GP per wrong answer.
-------------------------------
- Random : A random level! The same parameters as the chosen level, but the rewards gain a 10GP bonus (for right answers, smh) for being brave!
-------------------------------
Creator/作者: Sichengthebest"""%(update.effective_user.first_name,update.effective_user.first_name),reply_markup=get_kb(update)[0])

def capitalsCallback(update,context):
    user = update.effective_user
    query = update.callback_query
# What is the capital of 🇯🇵 Japan // 日本 🇯🇵?
# A) Fukushima // 福岛
# B) Tokyo // 东京
# C) Osaka // 大阪
# D) Toyota City // 丰田城
# ------------------------
# Please choose one:
    msg = query.message.text
    lines = msg.split("\n")
    # "cap:-uid-正确-当前"
    _ , curruid,ranswer,youranswer,level = update.callback_query.data.split('-')
    uid = update.effective_user.id
    if str(uid) != curruid:
        query.answer("你是谁？你在哪儿？你想做啥？这是别人的，大笨蛋！",show_alert=True)
        return
    lines.remove(lines[8])
    lines[int(ranswer)+3] += " ✅"
    if youranswer != ranswer:
        lines[int(youranswer)+3] += " ❌"
    send_msg = ""
    for line in lines:
        send_msg += line
        send_msg += "\n"
    if youranswer == ranswer:
        send_msg += "你答对了！🎉🎉🎉"
        if level == "easy":
            coins.add_coins(user,10)
            send_msg += "\n真厉害！你赢了10GP！🎊🎊🎊"
        elif level == "normal":
            coins.add_coins(user,25)
            send_msg += "\n真厉害！你赢了25GP！🎊🎊🎊"
        elif level == "hard":
            coins.add_coins(user,50)
            send_msg += "\n真厉害！你赢了50GP！🎊🎊🎊"
        else:
            coins.add_coins(user,125)
            send_msg += "\n真厉害！你赢了125GP！🎊🎊🎊"
    else:
        send_msg += "你答错了！😭😭😭"
        if level == "easy":
            coins.add_coins(user,-50)
            send_msg += "\n你输惨了！丢了50GP！"
        elif level == "normal":
            coins.add_coins(user,-20)
            send_msg += "\n你输惨了！丢了20GP！"
        elif level == "hard":
            coins.add_coins(user,-10)
            send_msg += "\n你输惨了！丢了10GP！"
        else:
            coins.add_coins(user,-5)
            send_msg += "\n你输惨了！丢了5GP！"
    query.edit_message_text("%s"%send_msg,reply_markup=get_kb(update)[1])

def restartCallback(update,context):
    query = update.callback_query
    uid = update.effective_user.id
    _ , curruid = update.callback_query.data.split('-')
    if str(uid) != curruid:
        query.answer("你是谁？你在哪儿？你想做啥？这是别人的，大笨蛋！",show_alert=True)
        return
    query.edit_message_text("""这是%s的游戏，如果你不叫%s，请不要乱点，请点 /capitals
-------------------------------
Which level?
- Easy : You are supposed to be cultivated enough to know these countries's capitals.
Rewards: 10GP per correct answer, lose 50GP per wrong answer.
-------------------------------
- Normal : Quite easy questions for those who have at least observed correctly a map.
Rewards: 25GP per correct answer, lose 20GP per wrong answer.
-------------------------------
- Hard : Quite hard countries, but most of which you have heard of, but probably not the capitals...
Rewards: 50GP per correct answer, lose 10GP per wrong answer.
-------------------------------
- Extreme : Countries you have never heard of! Big cash to win, though!
Rewards: 125GP per correct answer, lose 5GP per wrong answer.
-------------------------------
- Random : A random level, the same parameters as the chosen level!
-------------------------------
Creator/作者: Sichengthebest"""%(update.effective_user.first_name,update.effective_user.first_name),reply_markup=get_kb(update)[0])

def get_level(update,context):
    uid = update.effective_user.id
    query = update.callback_query
    data,curruid = update.callback_query.data.split('-')
    if str(uid) != curruid:
        query.answer("你是谁？你在哪儿？你想做啥？这是别人的，大笨蛋！",show_alert=True)
        return
    country = {}
    command = data
    level = command.split(":")[1]
    if command == "caplvl:easy":
        country = countries['easy']
    elif command == "caplvl:normal":
        country = countries['normal']
    elif command == "caplvl:hard":
        country = countries['hard']
    elif command == "caplvl:extreme":
        country = countries['extreme']
    elif command == "caplvl:random":
        rkey = random.choice([*countries.keys()])
        country = countries[rkey]
        level = rkey
    c = random.choice([*country.keys()])
    msg,markup = init_q(country[c],c,level,update.effective_user.id)
    query.edit_message_text("这是%s的游戏，如果你不叫%s，请不要乱点，请点 /capitals\n-------------------------------\n%s"%(update.effective_user.first_name,update.effective_user.first_name,msg),reply_markup=markup)

def get_command():
    return [BotCommand('capitals','How good are you at capitals? // 你了解所有首都吗？')]

def add_handler(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(capitalsCallback,pattern="^cap:[A-Za-z0-9_-]*"))
    dispatcher.add_handler(CallbackQueryHandler(restartCallback,pattern="^capres:[A-Za-z0-9_-]*"))
    dispatcher.add_handler(CallbackQueryHandler(get_level,pattern="^caplvl:[A-Za-z0-9_-]*"))
    dispatcher.add_handler(CommandHandler('capitals', capitals_old))
