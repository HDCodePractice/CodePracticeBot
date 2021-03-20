import config
from telegram import Update,BotCommand
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
import random

games = {}

def set_game(chatid,uid,fname):
    games[chatid] = {'responsestreak':0}
    games[chatid]['storysofar'] = ''
    games[chatid][uid] = {
            'fname':fname,
            'senctencescontributed':0
        }


def startms(update,context):
    global lastword
    fname = update.effective_user.first_name
    uid = str(update.effective_user.id)
    chatid = update.effective_chat.id

    if len(context.args) == 0:
        update.message.reply_text("""
        Welcome to Parker's Story game!

        How to play:
        - 1 Person will the start the game by typing a "/startms (word/sentence)"
        - The next person will continue by typing "/ms (sentence)", but the first word of the sentence must be the last word of the last sentence.
        Type /startms followed by any sentence to begin a new game.

        Note: This is the english version. You can play the chinese version with @TheRandomDudeHimself's @SichengsGodBot.
        """)
    else:
        try:
            game = games[chatid]
            print(game)
            update.message.reply_text('Sorry, but there is already a game going on in this group. Please try again later.')
        except KeyError:
            set_game(chatid,uid,fname)
            
            startingsentence = ' '
            for i in context.args:
                startingsentence += i
                startingsentence += ' '
            startingsentence = startingsentence[:-1]
            startingsentence += f'. ({fname})\n'

            lastword = ''
            lastword = context.args[-1]
            games[chatid]['storysofar'] = startingsentence
            update.message.reply_text(f"""
            A game has begun!

            To play, type /ms followed by any sentence.

            Note: This is the english version. You can play the chinese version with @TheRandomDudeHimself's @BotGod.

            The current story:

            {games[chatid]['storysofar']}
            
            The next message must begin with the word "{lastword}" """)

def ms(update,context):
    global lastword
    fname = update.effective_user.first_name
    uid = str(update.effective_user.id)
    chatid = update.effective_chat.id

    if len(context.args) == 0:
        update.message.reply_text('Please type a sentence following /ms.')
    else:
        if context.args[0].lower() == lastword.lower():
            if games[chatid]['responsestreak'] < 2:
                sentence = ''
                for i in context.args:
                    sentence += i
                    sentence += ' '
                sentence += f'.({fname})\n'
                games[chatid]['storysofar'] += f' {sentence}'
                lastword = ''
                lastword = context.args[-1]                
                update.message.reply_text(f'You have added the sentence "{sentence}" to the story! The story so far:\n\n {games[chatid]["storysofar"]}\n\nRemember: The first word of the next sentence must be "{lastword}"')
        else:
            update.message.reply_text(f'Sorry, but the first word in your sentence must be "{lastword}"')
    # except KeyError:
    #     update.message.reply_text('Sorry, but there is no game going on in this group chat. Type /startms to start one!')


def add_handler(dp: Dispatcher):
    dp.add_handler(CommandHandler(["startms"], startms))
    dp.add_handler(CommandHandler(["ms"], ms))
    return get_command()

def get_command():
    return [BotCommand('rewards','Reward Spins // 奖励大转盘')]