
import telebot
from telebot import apihelper
import keyboards
import data
import bd_def  # файл, в котором будут собраны функции для работы с базой данных

#apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота

def report(message, event): # отчет в pycharm об инициализации пользователя
    if event == 'name':
        print(message.chat.first_name + ' просит называть себя : ' + message.text)  # вывод сообщения в консоль pycharm
    elif event == 'category':
        print(message.chat.first_name + ' выбрал категорию : ' + message.text)
    elif event == 'priority':
        print(message.chat.first_name + ' выбрал приоритет : '+ message.text)
    elif event =='time of priority':
        print(message.chat.first_name + ' выбрал время для приоритета : '+message.text)
    elif event =="success of priority":
        print(message.chat.first_name + ' завершил выбирать приоритеты')


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


@bot.message_handler(commands=['del_key'])
def delete_keyboard(message):
    bot.send_message(message.chat.id, "Клавиатура удалена ", reply_markup=keyboards.delete_keyboard())

@bot.message_handler(commands=['category'])  # распознование команды /category
def start_category(message): # получение категории пользователя
    bot.send_message(message.from_user.id, 'К какой категории вы относитесь?')  # отправка сообщения пользователю
    bot.send_message(message.from_user.id, "Выбирите категорию:", reply_markup=keyboards.category_key())
    bot.register_next_step_handler(message, get_category)

def get_category(message):
    category = message.text
    if (message.text == 'Студент' or message.text == 'Школьник' or message.text == 'Работающий' or message.text == 'Бездельник'):
        bot.send_message(message.chat.id,"Замечательно, теперь по команде /priority Вы можете выбрать приоритеты", reply_markup=keyboards.delete_keyboard())
        bd_def.set_category(message.chat.id, category)
        report(message,'category')
    else:
        bot.send_message(message.chat.id,"Неверная категория, попробуйте снова")
        bot.register_next_step_handler(message, get_category)


@bot.message_handler(commands=['priority'])
def set_prioriry(message):
    bot.send_message(message.chat.id, "Выберите приоритеты:", reply_markup=keyboards.priority_key())
    bot.register_next_step_handler(message, get_priority)

def get_priority(message):
    if(message.text == "Завершить"):
        bot.send_message(message.chat.id, "Мы Вас запомнили",reply_markup=keyboards.delete_keyboard())
        report(message,'success of priority')
        return 0
    elif (message.text == "Экзамены" or message.text == "Изучение языков" or message.text =="Путешествие" or message.text=="Спорт"):
        report(message,'priority')
        bd_def.create_perfonal_bd(message.chat.id,message.chat.username,message.text)
        bot.send_message(message.chat.id, "Выберите время:", reply_markup=keyboards.time_key())
        bot.register_next_step_handler(message, set_time)
    else:
        bot.send_message(message.chat.id, "Неверный приоритет, попробуйте снова")
        bot.register_next_step_handler(message, get_priority)



def set_time(message):
    bot.send_message(message.chat.id, "Время принято", reply_markup=keyboards.delete_keyboard())
    bd_def.set_time(message.chat.id,message.text)
    report(message,'time of priority')
    bot.send_message(message.chat.id, "Выберите приоритеты:", reply_markup=keyboards.priority_key())
    bot.register_next_step_handler(message, get_priority)



bot.polling()
