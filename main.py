import telebot
from telebot import apihelper
    #файл для констант
import data
    #файл, в котором будут собраны функции для работы с базой данных
import bd_def
    #proxy
apihelper.proxy = {'https': data.get_proxy()}
    #инициализация бота
bot = telebot.TeleBot(data.get_token())

    #распознование команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
        #отправка сообщения пользователю
    bot.send_message(message.chat.id, 'Приветствую')
        #получение данных о пользователе
    user_id = message.chat.id
    username = str(message.chat.username)
    firstname = str(message.chat.first_name)
    secondname = str(message.chat.last_name)
        #добавление пользователя в базу данных
    bd_def.add_user(user_id,username,firstname,secondname)

    #распознование текстового сообщения
@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, 'Kekс')
        #вывод сообщения в консоль pycharm
    print(message.chat.username + ' : ' + message.text )
        #отправка сообщения Саше о том, что боту кто-то написал
    bot.send_message(data.sasha_chat_id(),message.chat.username + ' : ' + message.text)

    #это метод, чтобы бот не завершался
bot.polling()