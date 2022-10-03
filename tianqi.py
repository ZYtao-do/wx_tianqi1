'''
天气：{{weather.DATA}} 温度：{{temperature.DATA}} 湿度：{{humidity.DATA}} 风度：{{wind.DATA}} 空气质量：{{airquality.DATA}} 距离她的生日还有 {{brithday_left.DATA}}天 {{eng.DATA}} {{chinese.DATA}} {{words.DATA}}
'''
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['airQuality'], weather['weather'], math.floor(weather['temp']), weather['humidity'], weather['wind']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_jsyyh():
  url = "http://open.iciba.com/dsapi/"
  word = requests.get(url)
  content = word.json()["content"]
  note = word.json()["note"]
  return content, note
  

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
airquality, wea, temperature, humidity, wind = get_weather()
eng, chinese = get_jsyyh()
data = {"airquality":{"value":airquality}, "weather":{"value":wea}, "temperature":{"value":temperature}, "humidity":{"value":humidity}, "wind":{"value":wind}, "birthday_left":{"value":get_birthday()},"eng":{"value":eng, "color":get_random_color()}, "chinese":{"value":chinese}, "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)