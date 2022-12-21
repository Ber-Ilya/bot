import time

import telebot
from telebot import types
import re
import asyncio


TOKEN = '5864216251:AAF-uP6r15oBpkRe3pzorX-jtqlGWeypHuo'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','помощь',])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}! Чем могу помочь?")



#@bot.message_handler(content_types=['text'])

#def get_text(message):
 #   text = "Я могу тебя проконсультировать по согласованию перепланировки! Что тебя интересует? "
  #  text2= "Согласование - длительный процесс"
    #if message.text == "Привет" or message == "Здравствуйте" or message == "Здарова":
   #     bot.send_message(message.chat.id, text, parse_mode='html')
    #elif message.text == 'Меня интересует':
    #    bot.send_message(message.chat.id, text2, parse_mode='html')
    #else:
     #   bot.send_message(message.chat.id, "Я не понял, можешь задать вопрос по другому?", parse_mode='html')
@bot.message_handler(commands = ['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()
    #site = types.InlineKeyboardButton('Наш сайт', url="https://replan.one")
    markup.add(types.InlineKeyboardButton('Наш сайт', url="https://replan.one"))
    bot.send_message(message.chat.id, "Перейти на сайт", reply_markup=markup)


@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup()
    site = types.InlineKeyboardButton('Наш сайт', url="https://replan.one")
    contacts = types.KeyboardButton("Наши контакты")
    service = types.KeyboardButton("Наши услуги")
    price = types.KeyboardButton("Наши цены")
    menu = types.KeyboardButton("Меню")
    return_ = types.KeyboardButton('Назад')


    markup.add(site, contacts, service, price, menu, return_)
    bot.send_message(message.chat.id, 'Выберите неоходимый пункт меню', reply_markup=markup)

asyncio.run(bot.polling())

