import pytz
from icalevents.icalevents import events
from datetime import datetime, timedelta, date, time
from telegram.ext import JobQueue, CommandHandler, Updater
from telegram import bot
import config


cals = config.CONFIG['cal']

def save():
    config.CONFIG['cal'] = cals
    config.save_config()    

def get_cal(context):
    job = context.job
    t = date.today()
    tmr = t + timedelta(days=1)
    es = events(url=cals[str(job.context)]['url'],start=tmr,end=tmr,fix_apple=True)
    msg = "Tomorrow's events:"
    if len(es) == 0:
        msg = 'You have no events tomorrow.'
    for thing in es:
        description = str(thing.description)
        if description == 'None':
            description = 'No description'
        msg += f'''
----------------------------
{thing.summary}: {description}
    Starts: {datetime.strftime(thing.start,"%Y/%m/%d %H:%M:%S")}
    Ends: {datetime.strftime(thing.end,"%Y/%m/%d %H:%M:%S")}'''
    context.bot.send_message(job.context,msg)

def show_cal(update,context):
    msg = 'Here are your calendars:'
    for chatid in cals:
        msg += f'''
~~~~~~~~~~~~~~~~~~~~~~~~
📆 {chatid}:
    Calendar URL: {cals[chatid]['url']}
    Time: {cals[chatid]['time'][0]}:{cals[chatid]['time'][1]}
    Timezone: {cals[chatid]['time'][2]}'''
    update.message.reply_text(msg)

def show_job(update,context):
    msg = 'Here is a list of jobs:'
    for job in context.job_queue.jobs():
        msg += f'\n{job.name}: {datetime.strftime(job.next_t,"%H:%M")}'
    update.message.reply_text(msg)

def set_cal(update,context):
    uid = update.effective_user.id
    if not uid in config.CONFIG['admin']:
        update.message.reply_text('Sorry, you\'re not an admin.')
        return
    if len(context.args) == 0:
        update.message.reply_text('Here\'s the format you need to respect to subscribe to your calendar notifications:\n\n/get_cal@SichengGodBot {Your Apple Calendar URL} {The time you want the notification sent, for example, 17:00} {Your time zone, for example, US/Eastern}\n\nFor a list of time zones please check https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568#file-pytz-time-zones-py')
        return
    if len(context.args) > 3:
        update.message.reply_text('Too many arguments! Please follow this format: /set_cal@CodePracticeBot {Your Apple Calendar URL} {The time you want the notification sent, for example, 17:00} {Your time zone, for example, US/Eastern}')
        return
    url = context.args[0]
    time = context.args[1]
    timezone = context.args[2]
    chatid = update.effective_chat.id
    if not timezone in pytz.all_timezones:
        update.message.reply_text('Sorry, that is not a valid time zone. Please check this website for more info: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568#file-pytz-time-zones-py')
        return
    cals[str(chatid)] = {}
    cals[str(chatid)]['url'] = url
    strhours,strminutes = time.split(':')
    hours = int(strhours)
    minutes = int(strminutes)
    if hours > 23 or hours < 0:
        update.message.reply_text('BIG DUMMY A DAY HAS 24 HOURS WTH and BTW 12AM is 0:00')
        return
    if minutes >= 60 or minutes < 0:
        update.message.reply_text('BIG DUMMY AN HOUR HAS 60 MINUTES WTH')
        return
    cals[str(chatid)]['time'] = [hours,minutes,timezone]
    update.message.reply_text(f'Success! You will receive notifications every day at {time}.')
    run_daily(context.job_queue)

def run_daily(job_queue):
    for chatid in cals:
        calstuff = cals[chatid]
        for job in job_queue.jobs():
            if job.name == chatid:
                job.schedule_removal()
        job_queue.run_daily(get_cal,time(calstuff['time'][0],calstuff['time'][1],0,0,pytz.timezone(calstuff['time'][2])),context=chatid,name=chatid)

def add_handler(dp):
    dp.add_handler(CommandHandler('set_cal',set_cal))
    dp.add_handler(CommandHandler('show_cal',show_cal))
    dp.add_handler(CommandHandler('show_jobs',show_job))