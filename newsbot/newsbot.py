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

API_TOKEN='1341244288:AAFYQd42j76LVzPAf11wAgtlTB4Tpu2fqro'

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


@bot.message_handler(commands=['news'])
def send_news(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/news/')
    news = _format_news(res.json()[:5])
    for one_news in news:
        bot.send_message(
            message.chat.id,
            one_news,
            parse_mode='HTML',
        )


def _format_news(raw_data):
    news = list()
    for item in raw_data:
        title = f"<b>{item['title']}</b>"
        abstract = f"{item['abstract']}"
        url = f"<a href='{item['url']}'>Подробнее</a>"
        formatted_news = '\n'.join((title, abstract, url))
        news.append(formatted_news)
    return news





bot.polling()
