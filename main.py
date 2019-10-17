
import telebot
from telebot import apihelper
import data
import bd_def  # файл, в котором будут собраны функции для работы с базой данных

apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота

name = ''
@bot.message_handler(commands=['start'])  # распознование команды /start
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую')  # отправка сообщения пользователю
    user_id = message.chat.id  # получение данных о пользователе
    username = str(message.chat.username)
    firstname = str(message.chat.first_name)
    secondname = str(message.chat.last_name)
    bd_def.add_user(user_id, username, firstname, secondname)  # добавление пользователя в базу данных
    bot.send_message(message.from_user.id, 'Как тебя зовут?')  # отправка сообщения пользователю
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


def get_name(message):  # вывод сообщения
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Хорошо, я запомню, что тебя зовут ' + name)
    print(message.chat.first_name + ' : ' + message.text)  # вывод сообщения в консоль pycharm
    bot.send_message(data.sasha_chat_id(), message.chat.first_name + ' : ' + message.text)  # сбщ, что боту написали


bot.polling()
