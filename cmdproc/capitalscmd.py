from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
import random

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

def init_markup(update,choice):
    mk = []
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
            mk.append({yes:"cap:yes"})
        else:
            mk.append({no[0]:"cap:no"})
            no.remove(no[0])
    mk.append({haha:"cap:no"})
    buttons = []
    uid = update.effective_user.id
    for line in mk:
        button = []
        for key in line.keys():
            button.append(InlineKeyboardButton(key, callback_data="%s-%s"%(line[key],uid)))
        buttons.append(button)
    return InlineKeyboardMarkup(buttons)


def capitals(update,context):
    country = {}
    command = update.effective_message.text
    if command == "/capitals_easy":
        country = countries['easy']
    elif command == "/capitals_normal":
        country = countries['normal']
    elif command == "/capitals_hard":
        country = countries['hard']
    elif command == "/capitals_extreme":
        country = countries['extreme']
    elif command == "/capitals_random":
        rkey = random.choice([*countries.keys()])
        country = countries[rkey]
    else:
        update.effective_message.reply_text(help())
        return
    c = random.choice([*country.keys()])
    update.effective_message.reply_text("""What is the capital of %s?
-------------------------------------------------------------------------
Warning: These buttons may not completely appear on mobile devices, but @TheRandomDudeHimself is trying to find a solution quickly!
Pro tip: if the button text does not completely appear, it's because it's not the right answer!
警告：这些按钮可能不会完全显示在移动设备上，但是 @TheRandomDudeHimself 正在试图快速找到解决方案！
专家提示：如果按钮文本没有完全显示，那是因为这不是正确的答案！
-------------------------------------------------------------------------
Please choose one // 请选一个:"""%c,reply_markup=init_markup(update,country[c]))
    

def help():
    return """A general knowledge game! The bot will randomly generate a country and a number of answer choices, depending on your chosen difficulty level. The choices are as shown:
-------------------------------------------------------------------------
- /capitals_easy : You are supposed to be cultivated enough to know these countries's capitals.
-------------------------------------------------------------------------
- /capitals_normal : Quite easy questions for those who have at least observed correctly a map.
-------------------------------------------------------------------------
- /capitals_hard : Quite hard countries, but most of which you have heard of, but probably not the capitals...
Rewards: 50GP per correct answer, lose 10GP per wrong answer.
-------------------------------------------------------------------------
- /capitals_extreme : Countries you have never heard of! Big cash to win, though!
-------------------------------------------------------------------------
- /capitals_random : A random level! The same parameters as the chosen level, but the rewards gain a 10GP bonus (for right answers, smh) for being brave!
-------------------------------------------------------------------------
Creator/作者: Sichengthebest"""

def capitalsCallback(update,context):
    query = update.callback_query
    callback, curruid = update.callback_query.data.split('-')
    uid = update.effective_user.id
    if str(uid) != curruid:
        query.answer("你是谁？你在哪儿？你想做啥？这是别人的，大笨蛋！",show_alert=True)
        return
    if callback == 'cap:yes':
        query.edit_message_text("Good job, @%s, you have got the right answer!\nCreator/作者: Sichengthebest"%(update.effective_user.username))
    else:
        query.edit_message_text("WRONG!!! @%s, you are so trash at this.\nCreator/作者: Sichengthebest"%(update.effective_user.username))

def add_handler(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(capitalsCallback,pattern="^cap:[A-Za-z0-9_-]*"))
    dispatcher.add_handler(CommandHandler('capitals_easy', capitals))
    dispatcher.add_handler(CommandHandler('capitals_normal', capitals))
    dispatcher.add_handler(CommandHandler('capitals_hard', capitals))
    dispatcher.add_handler(CommandHandler('capitals_extreme', capitals))
    dispatcher.add_handler(CommandHandler('capitals_random', capitals))
    dispatcher.add_handler(CommandHandler('capitals', capitals))