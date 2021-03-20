from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def getkb(KeyboardDict):
    # KeyboardDict: [ {'text':'callback_data','text':'callback_data'},{'text':'callback_data','text':'callback_data'},{'text':'callback_data','text':'callback_data'...}.... ]
    k = []
    for line in KeyboardDict:
        j = []
        for button in line:
            #line : {'小': 'small', '大': 'big'}
            #button : 小
            j.append(InlineKeyboardButton(button,callback_data=line[button]))
        k.append(j)
    return InlineKeyboardMarkup(k)
