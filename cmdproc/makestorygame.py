import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,BotCommand, Update
from telegram.ext import Dispatcher,CommandHandler,CallbackContext,CallbackQueryHandler
import random
from langdetect import detect


games = {}

def set_game(chatid,uid,fname):
    games[chatid] = {'responsestreak':0,'storysofar':'','last2responses':[],'avotes':0,'bvotes':0}
    games[chatid][uid] = {
            'fname':fname,
            'senctencescontributed':0,
            'voted':True
        }

def set_user(chatid,uid,fname):
    games[chatid][uid] = {
            'fname':fname,
            'senctencescontributed':0,
            'voted':True
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
            startingsentence = ' '
            for i in context.args:
                startingsentence += i
                startingsentence += ' '
            startingsentence = startingsentence[:-1]
            startingsentence += f'. ({fname})\n'
            
            if detect(startingsentence) == 'en':
                set_game(chatid,uid,fname)
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
            else:
                update.message.reply_text('Sorry, but please make sure that:\n\n1. Your sentence is in english\n2. Your sentence is grammatically correct.')

def ms(update,context):
    global lastword
    fname = update.effective_user.first_name
    chatid = update.effective_chat.id

    if len(context.args) == 0:
        update.message.reply_text('Please type a sentence following /ms.')
    else:
        if context.args[0].lower() == lastword.lower():
            sentence = ''
            for i in context.args:
                sentence += i
                sentence += ' '
            sentence += f'.({fname})\n'
            if detect(sentence) == 'en':
                games[chatid]['last2responses'].append(f' {sentence}'[:-1])
                games[chatid]['responsestreak'] += 1
                lastword = ''
                lastword = context.args[-1]                
                update.message.reply_text(f'You have added the sentence "{sentence}" to the story! The story so far:\n\n {games[chatid]["storysofar"]} (Every 2 repsonses, players will vote which sentence they want to add to the story.)\n\nRemember: The first word of the next sentence must be "{lastword}"')
                if games[chatid]['responsestreak'] == 2:
                    votefora = InlineKeyboardButton('Vote for response (a)',callback_data='voteforresponse:a')
                    voteforb = InlineKeyboardButton('Vote for response (b)',callback_data='voteforresponse:b')
                    voteforresponsekb = InlineKeyboardMarkup([[votefora],[voteforb]])
                    update.message.reply_text(f'To prevent spam, Players will now vote which of the last two responses they want to add to the story.\n\nThe two responses:\n\na.{games[chatid]["last2responses"][0]}\n\nb.{games[chatid]["last2responses"][1]}\n\nClick either the "Vote for response (a)" or the "vote for response (b)" to choose which response you want in your story. ',reply_markup=voteforresponsekb)
        else:
            update.message.reply_text(f'Sorry, but the first word in your sentence must be "{lastword}"')

def voteforresponsecallback(update,context):
    query = update.callback_query
    chatid = update.effective_chat.id
    user = update.effective_user
    try:
        if games[chatid][user.id]['voted']== False:
            if query.data =='voteforresponse:a':
                voteindex = 0
                games[chatid]['avotes'] += 1 
                print(str(games[chatid]['avotes']))
            elif query.data == 'voteforresponse:b':
                voteindex = 1
                games[chatid]['bvotes'] += 1 
                print(str(games[chatid]['bvotes']))
        else:
            query.answer('You have already voted.')
    except KeyError:
        set_user(chatid,user.id,user.fname)
    


def add_handler(dp: Dispatcher):
    dp.add_handler(CallbackQueryHandler(voteforresponsecallback,pattern="^voteforresponse:[A-Za-z0-9_]*"))
    dp.add_handler(CommandHandler(["startms"], startms))
    dp.add_handler(CommandHandler(["ms"], ms))
    return get_command()

def get_command():
    return [BotCommand('rewards','Reward Spins // 奖励大转盘')]