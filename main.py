import telebot
from telebot import apihelper
import data
#proxy
apihelper.proxy = {'https': 'https://188.217.245.105:8118'}

bot = telebot.TeleBot('966505306:AAHFTinGFcnYjZ7abFCZG9wAO47OkkAqkhI')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ну здарова')

@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Kek')
    print(message.chat.username + ' : ' + message.text )
    bot.send_message(data.my_chat_id(),message.chat.username + ' : ' + message.text)

bot.polling()