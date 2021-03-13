import config
from telegram import Update,BotCommand
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
import random, re, itertools

def solve(num1,num2,num3,num4):
    operations = ['+','-','*','/']
    all_possible_combinations = []          
    for i in operations:
        for j in operations:
            for k in operations:
                all_possible_combinations.append((f"{num1}{i}{num2}{j}{num3}{k}{num4}"))
                all_possible_combinations.append((f"({num1}{i}{num2}){j}{num3}{k}{num4}"))
                all_possible_combinations.append((f"({num1}{i}{num2}{j}{num3}){k}{num4}"))
                all_possible_combinations.append((f"{num1}{i}({num2}{j}{num3}){k}{num4}"))
                all_possible_combinations.append((f"{num1}{i}({num2}{j}{num3}{k}{num4})"))
                all_possible_combinations.append((f"{num1}{i}{num2}{j}({num3}{k}{num4})"))

    arrayofanswers = []
    for i in all_possible_combinations:
        try:
            if int(eval(i)) == 24:
                arrayofanswers.append(i)
        except ZeroDivisionError:
            pass
    return(arrayofanswers)

"""
支持 /rewards 命令
"""

def solve24(update,context):
    if len(context.args) == 4:
        allints = True
        for i in context.args:
            if type(i) == int:
                allints = False
        if allints == True:
            update.message.reply_text(f'All possible solutions for a game of 24 using the numbers {context.args[0]},{context.args[1]},{context.args[2]}, and {context.args[3]}:\n\n{solve(context.args[0],context.args[1],context.args[2],context.args[3])}')
        else: 
            update.message.reply_text('Sorry, but all four characters must be numbers from 1 - 10.')
    else:
        update.message.reply_text('Sorry, but please use this format: \n\n/solve24 (number 1) (number 2) (number 3) (number 4)(e.g"/solve24 5 6 9 2")')

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["solve24"], solve24))

def add_handler(dp:Dispatcher):
    dp.add_handler(CommandHandler('solve24', solve24))
    return [BotCommand('solve24','Cheat in a game of 24 XD // Made by @ParkerChen')]