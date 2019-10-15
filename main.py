import telebot
from telebot import apihelper
import data
import bd_def
#apihelper.proxy = {'https': data.get_proxy()}


bot = telebot.TeleBot(data.get_token())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую')
    user_id = message.chat.id
    username = str(message.chat.username)
    firstname = str(message.chat.first_name)
    secondname = str(message.chat.last_name)
    #добавление пользователя в базу данных
    bd_def.add_user(user_id,username,firstname,secondname)


@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Kekс')
    print(message.chat.username + ' : ' + message.text )
    bot.send_message(data.sasha_chat_id(),message.chat.username + ' : ' + message.text)

bot.polling()