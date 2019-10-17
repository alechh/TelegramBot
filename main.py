
import telebot
from telebot import apihelper
from telebot import types
import data
import bd_def  # файл, в котором будут собраны функции для работы с базой данных

#apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота

def report(message, event): # отчет в pycharm об инициализации пользователя
    if event == 'name':
        print(message.chat.first_name + ' просит называть себя : ' + message.text)  # вывод сообщения в консоль pycharm
    elif event == 'category':
        print(message.chat.first_name + ' выбрал категорию : ' + message.text)


@bot.message_handler(commands=['start'])  # распознование команды /start
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую')  # отправка сообщения пользователю
    bot.send_message(message.from_user.id, 'Как Вас зовут?')  # отправка сообщения пользователю
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name

def get_name(message):  # получение имени
    name = str(message.text)
    user_id = message.chat.id  # получение данных о пользователе
    username = str(message.chat.username)
    firstname = str(message.chat.first_name)
    secondname = str(message.chat.last_name)
    bot.send_message(message.from_user.id, 'Хорошо, я запомню, что тебя зовут ' + name)
    bot.send_message(message.from_user.id, 'Теперь по команде /category Вы можете установить свою категорию')
    report(message,'name')
    bd_def.add_user(user_id, username, firstname, secondname, name, 'None')  # добавление пользователя в базу данных


@bot.message_handler(commands=['category'])  # распознование команды /category
def start_category(message): # получение категории пользователя
    bot.send_message(message.from_user.id, 'К какой категории вы относитесь?')  # отправка сообщения пользователю
    markup = types.ReplyKeyboardMarkup(row_width=2) #клавиатура
    c1 = types.KeyboardButton('Студент')
    c2 = types.KeyboardButton('Школьник')
    c3 = types.KeyboardButton('Работающий')
    c4 = types.KeyboardButton('Бездельник')
    markup.add(c1,c2,c3,c4)
    bot.send_message(message.from_user.id, "Выбирите категорию:", reply_markup=markup)
    bot.register_next_step_handler(message, get_category)

def get_category(message):
    user_id = message.chat.id
    category = message.text
    bd_def.set_category(user_id,category)
    if (message.text == 'Студент' or message.text == 'Школьник' or message.text == 'Работающий' or message.text == 'Бездельник'):
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(user_id,"Замечательно", reply_markup=markup)
        report(message,'category')
    else:
        bot.send_message(user_id,"Неверная категория, попробуйте снова")
        bot.register_next_step_handler(message, get_category)



bot.polling()
