#!/usr/bin/env python3

"""
为每个群设置一个自己的金币体系

数据结构：

coins={
    chatid:{
        userid:{
            name:firstname,
            coins:int
        }
    }
}
"""


from random import randint

coins={}

def checkcoins(chatid,userid,username):
    # 检查chatid和userid是否存在
    if chatid in coins:
        if not((userid in coins[chatid])):
            coins[chatid][userid]={'name':username,"coins":0}
        else:
            coins[chatid][userid]['name']=username
    else:
        coins[chatid]={}
        coins[chatid][userid]={'name':username,"coins":0}

def pre_check(func):
    def check_coins(*args):
        checkcoins(*args)
        return func(*args)
    return check_coins

@pre_check
def checkin(chatid,userid,username):
    """
    打卡签到，返回签到增加的coins数量
    """
    checkin_coins = randint(20000,30000)
    coins[chatid][userid]['coins'] += checkin_coins
    return checkin_coins