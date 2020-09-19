#!/usr/bin/env python3

"""
使用的是onecall api
返回的数值参见： https://openweathermap.org/api/one-call-api
相关的编码说明参见： https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#onecall
相关的API文档：https://pyowm.readthedocs.io/en/latest/pyowm.weatherapi25.html#module-pyowm.weatherapi25.weather
天气状态的说明参见： https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
天气的emoji参见： https://www.emojidaquan.com/category2-sky-weather
"""

from typing import List
from pyowm import OWM
from pyowm.weatherapi25.weather import Weather
from telegram.ext import Dispatcher,CommandHandler,CallbackContext
from telegram import Update
from datetime import datetime
import pytz

weather_status = {
    801: ["🌤️","few clouds","少云"], 
    802: ["⛅","scattered clouds","零散的云"],
    803: ["🌥️","broken clouds","碎云"],
    804: ["☁️☁️","overcast clouds","阴云"],
    800: ["☀️","clear sky","晴"],
    701: ["🌫️","mist","薄雾"],
    711: ["🌫️","Smoke","烟雾"],
    721: ["🌫️","Haze","阴霾"],
    731: ["🌫️","sand/dust whirls","沙尘飞扬"],
    741: ["🌫️","fog","多雾"],
    751: ["🌫️","sand","沙"],
    761: ["🌫️","dust","土"],
    762: ["🌫️","volcanic ash","火山灰"],
    771: ["🌫️","squalls","狂风"],
    781: ["🌪️","tornado","龙卷风"],
    600: ["❄️","light snow","小雪"],
    601: ["❄️❄️","snow","雪"],
    602: ["❄️❄️❄️","Heavy snow","暴雪"],
    611: ["💧❄️","Sleet","雨夹雪"],
    612: ["💧❄️","Light shower sleet","轻雨夹雪"],
    613: ["💧❄️","Shower sleet","雨夹雪"],
    615: ["💧❄️","Light rain and snow","小雨加雪"],
    616: ["💧❄️","Rain and snow","雨加雪"],
    620: ["🌨️","Light shower snow","轻阵雪"],
    621: ["🌨️🌨️","Shower snow","阵雪"],
    622: ["🌨️🌨️🌨️","Heavy shower snow","大阵雪"],
    500: ["💧","light rain","小雨"],
    501: ["💧💧","moderate rain","中雨"],
    502: ["💧💧💧","heavy intensity rain","大雨"],
    503: ["💧💧💧💧","very heavy rain","暴雨"],
    504: ["💧💧💧💧💧","extreme rain","大暴雨"],
    511: ["🌧️","freezing rain","冻雨"],
    520: ["🌧️","light intensity shower rain","小阵雨"],
    521: ["🌧️","shower rain","阵雨"],
    522: ["🌧️","heavy intensity shower rain","强阵雨"],
    531: ["🌧️","ragged shower rain","阵雨"],
    300: ["🌦️","light intensity drizzle","阳光毛毛雨"],
    301: ["🌧️","drizzle","毛毛雨"],
    302: ["🌧️🌧️","heavy intensity drizzle","强毛毛雨"],
    310: ["🌦️","light intensity drizzle rain","阳光细雨"],
    311: ["🌧️","drizzle rain","细雨"],
    312: ["🌧️🌧️","heavy intensity drizzle rain","强细雨"],
    313: ["🌧️","shower rain and drizzle","蒙蒙细雨"],
    314: ["🌧️","heavy shower rain and drizzle","阵雨和细雨"],
    321: ["🌧️","shower drizzle","阵雨"],
    200: ["🌩️","thunderstorm with light rain","雷阵雨"],
    201: ["🌩️","thunderstorm with rain","雷雨"],
    202: ["🌩️","thunderstorm with heavy rain","雷暴雨"],
    210: ["🌩️","light thunderstorm	","小雷雨"],
    211: ["🌩️","thunderstorm","雷雨"],
    212: ["🌩️🌩️","heavy thunderstorm","大雷雨"],
    221: ["🌩️🌩️🌩️","ragged thunderstorm","恶雷雨"],
    230: ["🌩️","thunderstorm with light drizzle","雷雨夹小雨"],
    231: ["🌩️","thunderstorm with drizzle","雷雨夹毛毛雨"],
    232: ["🌩️","thunderstorm with heavy drizzle","雷阵雨"]
}

local_timezone = 0

def get_local_time(t):
    return datetime.fromtimestamp(t).astimezone(local_timezone).strftime("%H:%M:%S")

def get_local_time_hour(t):
    return datetime.fromtimestamp(t).astimezone(local_timezone).strftime("%H")

def get_local_time_weekday(t):
    return datetime.fromtimestamp(t).astimezone(local_timezone).strftime("%A")

def forecast_daily_str(wts:List[Weather]) -> str:
    wstr = ""
    for wt in wts[1:]:
        wstr += (
            f"{get_local_time_weekday(wt.ref_time)}\n{weather_status[wt.weather_code][0]} {wt.temperature('celsius')['min']}-{wt.temperature('celsius')['max']}°C 💨{wt.wind()['speed']}m/s\n"
        )
    return wstr

def forecast_hourly_str(wts:List[Weather]) -> str:
    wstr = ""
    for wt in wts[1:13]:
        wstr += "%s %s %s°C 💨%sm/s\n"%(
            get_local_time_hour(wt.ref_time),
            weather_status[wt.weather_code][0],
            wt.temperature('celsius')['temp'],
            wt.wind()['speed']
        )
    return wstr

def current_str(wt:Weather):
    wstr = "%s%s(%s)"%(weather_status[wt.weather_code][0],weather_status[wt.weather_code][2],weather_status[wt.weather_code][1])

    wstr += "\n温度(temp)%s°C\n体感温度(feels like)%s°C\n湿度(humidity)%s%%"%(wt.temperature('celsius')['temp'],wt.temperature('celsius')['feels_like'],wt.humidity)
    wstr += "\n能见度(visibility)%skm 💨%sm/s"%(wt.visibility_distance / 1000,wt.wind()['speed'])
    wstr += "\n🌅%s 🌇%s"%(
        get_local_time(wt.sunrise_time()),
        get_local_time(wt.sunset_time())
        )
    return wstr

def get_weather(owm,lat,lon):
    global local_timezone
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=45.41, lon=-73.88)
    local_timezone = pytz.timezone(one_call.timezone)
    rstr = current_str(one_call.current)
    rstr += (
        f"\n\n{forecast_hourly_str(one_call.forecast_hourly)}"
        f"\n{forecast_daily_str(one_call.forecast_daily)}"
    )
    return rstr

def weather(update : Update, context : CallbackContext):
    import config
    owm = OWM(config.CONFIG['OWM_key'])
    update.message.reply_text(get_weather(owm,lat=45.41,lon=-73.88))
    

def setw_cmd(update : Update, context : CallbackContext):
    import config
    if update.message.from_user.id in config.CONFIG['Admin'] :
        ws = {}
        for t in context.args:
            chat,name,lat,lon = t.split(",")
            ws[chat]=[name,float(lat),float(lon)]
        if len(ws)  > 0 :
            config.CONFIG['Weather']=ws
            config.save_config()
            update.message.reply_text(f"更新完成:{ws}")
        else:
            update.message.reply_text(f"内容为空")
           

def getw_cmd(update : Update, context : CallbackContext):
    import config
    ws = config.CONFIG['Weather']
    msg = ""
    for chat in ws.keys():
        name,lat,lon = ws[chat]
        msg +=f"{chat},{name},{lat},{lon} "
    update.message.reply_text(msg)

def add_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler(["weather"], weather))
    dp.add_handler(CommandHandler(["setw"], setw_cmd))
    dp.add_handler(CommandHandler(["getw"], getw_cmd))


if __name__ == '__main__':
    owmkey = open("owmkey").read()
    owm = OWM(owmkey)
    print(get_weather(owm,lat=45.41,lon=-73.88))