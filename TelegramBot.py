import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as b
from secret import API

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,f"Здравствуйте {message.from_user.first_name}! Вас приветствует интернет-магазин. Для того, чтобы ознакомиться с нашими товарами, нажмите /menu. Для того, чтобы получить информацию о нашем магазине,"
                             f" нажмите /help.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Это чат-бот магазина Mark Formelle. Наш чат-бот покажет вам ассортимент продукции в выбранной категории. Для перехода к товарам нажмите /menu.')

@bot.message_handler(commands=['menu'])
def menu(message):
    my_buttons = types.InlineKeyboardMarkup(row_width=2)
    button_socks = types.InlineKeyboardButton(text='Носки', callback_data='socks')
    button_tights = types.InlineKeyboardButton(text='Колготки', callback_data='tights')
    my_buttons.add(button_socks, button_tights)
    bot.send_message(message.chat.id, 'Выберите категорию товаров:', reply_markup=my_buttons)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'tights':

            URL_tights = 'https://markformelle.by/catalog/zhenshchinam/noski-i-kolgotki/kolgotki-zhenskie/'
            r = requests.get(URL_tights)
            soup = b(r.text, 'html.parser')
            tigts_title = soup.select('div.catalog-name')
            tigts_price = soup.select('div.catalog-cost')
            for i in tigts_title:
                title = i.get_text()
                for j in tigts_price:
                    price = j.get_text()
                    bot.send_message(call.message.chat.id, title + price)

        elif call.data == 'socks':
            URL_socks = 'https://markformelle.by/catalog/zhenshchinam/noski-i-kolgotki/noski-zhen/poliamidnye-zhenskie/'
            r = requests.get(URL_socks)
            soup = b(r.text, 'html.parser')
            socks_title = soup.select('div.catalog-name')
            socks_price = soup.select('div.catalog-cost')
            for i in socks_title:
                title_socks = i.get_text()
                for j in socks_price:
                    price_socks = j.get_text()
                    bot.send_message(call.message.chat.id, title_socks + price_socks)

bot.polling(none_stop=True)
