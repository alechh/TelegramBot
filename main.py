import telebot
from telebot import apihelper
import data
#proxy
apihelper.proxy = {'https': data.get_proxy()}


bot = telebot.TeleBot(data.get_token())

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ну здарова')

@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Kek')
    print(message.chat.username + ' : ' + message.text )
    bot.send_message(data.my_chat_id(),message.chat.username + ' : ' + message.text)

bot.polling()