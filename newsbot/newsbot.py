import telebot
import requests
import json

# TODO: Настроить фильтрацию в джангорест
# TODO: Добавить модели для юзеров ТГ и их настроек
# TODO: Написать обработку команд (см. ниже)
# TODO: Разобраться с красивой версткой сообщений (включая диплники)

# /news_by_source - получить новости
## /NYT
### /last_hour
### /daily
### /top

# "/topic Superbowl Winner Loser" (returns list of titles, each title is a /command)

# "/news_by_title News title" (returns all we know about the record)

# "/news_by_date 2021-01-02"

API_TOKEN='1579083588:AAEzkj36aB9q1sZZ7C0BvCykeQawpJahqOA'

BASE_URL = 'http://127.0.0.1:8000/api'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    _ = requests.get(f'{BASE_URL}/start/', params=message.json['from'])
    bot.send_message(f'Hello, {message.json["from"].get("username", "User")}')

@bot.message_handler(commands=['source'])
def send_welcome(message):
    panel = telebot.types.ReplyKeyboardMarkup(row_width=1)
    button_nyt = telebot.types.KeyboardButton('NYTimes')
    button_ap = telebot.types.KeyboardButton('AP')
    panel.add(button_nyt, button_ap)
    bot.send_message(message.chat.id, "Choose source:", reply_markup=panel)

@bot.message_handler(commands=['topic'])
def send_nytimes_settings(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/tags/')
    bot.send_message(message.chat.id, json.dumps(res.json()[:5]))


def _format_news(raw_data):
    pass

bot.polling()
