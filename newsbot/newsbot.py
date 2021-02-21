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
    bot.send_message(message.chat.id, f'Hello, {message.json["from"].get("username", "User")}')


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

# в этом варианте мы вытягиваем руками нужные поля, но они дублируются превьюшкой
@bot.message_handler(commands=['top1'])
def send_nytimes_news(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/news/')
    for item in _format_news(res.json()[:1]):
        bot.send_message(message.chat.id, item, parse_mode='MarkdownV2', disable_web_page_preview=False)

# этот вариант дает в превьюшках то, что мы пытаемся вытянуть руками
@bot.message_handler(commands=['top2'])
def send_nytimes_news(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/news/')
    for item in res.json()[:2]:
        bot.send_message(message.chat.id, _clear_MarkdownV2(item['url']), parse_mode='MarkdownV2')

# в этом варианте мы вытягиваем руками и запрещаем превьюшки, чтобы не дублировать
@bot.message_handler(commands=['top3'])
def send_nytimes_news(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/news/')
    for item in _format_news(res.json()[:3]):
        bot.send_message(message.chat.id, item, parse_mode='MarkdownV2', disable_web_page_preview=True)

# в этом варианте отправляем 15 ссылок одним сообщением
@bot.message_handler(commands=['top4'])
def send_nytimes_news(message):
    res = requests.get('http://h4newsapi.pythonanywhere.com/news/')
    result = ''
    for item in _format_news(res.json()[:4]):
        result = f"{result}\r\n\r\n{item}"
    bot.send_message(message.chat.id, result, parse_mode='MarkdownV2', disable_web_page_preview=True)

def _format_news(raw_data):
    return [_format_single_entry(news) for news in raw_data]


def _clear_MarkdownV2(entry):
    # _*[]()~>#+-=|{}.!
    for char in '_*[]()~>#+-=|{}.!':
        entry = entry.replace(char, f'\{char}')
    return entry


def _format_single_entry(dict):
    return f"*{_clear_MarkdownV2(dict['title'])}*\r\n" \
           f"{_clear_MarkdownV2(dict['abstract'])}\r\n" \
           f"[Подробнее]({_clear_MarkdownV2(dict['url'])})"


bot.polling()
