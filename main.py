import telebot
from telebot import apihelper
import keyboards
import data
import time
import datetime
import bd_def

apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота
q = True # глобальная переменная для корректной работы цикла с проверкой времени

def report(message, event,time=None, prior=None): # отчет в pycharm об инициализации пользователя
    if event == 'name':
        print(message.chat.first_name + ' просит называть себя : ' + message.text)
    elif event == 'category':
        print(message.chat.first_name + ' выбрал категорию : ' + message.text)
    elif event == 'priority':
        print(message.chat.first_name + ' выбрал приоритет : '+ message.text)
    elif event =='time of priority':
        print(message.chat.first_name + ' выбрал время для приоритета : '+message.text)
    elif event =="success of priority":
        print(message.chat.first_name + ' завершил выбирать приоритеты')
    elif event == "note":
        print(message.chat.first_name + " добавил заметку : "+ message.text)
    elif event == "list of notes":
        print(message.chat.first_name + " посмотрел список заметок")
    elif event == "message by priority":
        print(message.chat.first_name + " получил сообщение " +prior+" по времени " + time)

@bot.message_handler(commands=['start'])  # распознование команды /start
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую')
    bot.send_message(message.from_user.id, 'Как Вас зовут?')
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name

def get_name(message):  # получение имени
    name = str(message.text)
    user_id = message.chat.id
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

@bot.message_handler(commands=['category'])
def start_category(message):
    bot.send_message(message.from_user.id, 'К какой категории вы относитесь?')
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
        global k
        k = False
        time.sleep(2)
        priority_message(message) #запуск цикла с проверкой времени
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

@bot.message_handler(commands=['notes'])
def print_notes(message):
    notes = []
    notes = bd_def.print_notes((message.chat.id))
    res = ''
    count = 1
    for i in notes:
        res += str(count)+'. ' + str(i) + '\n'
        count += 1
    bot.send_message(message.chat.id,res)
    report(message,"list of notes")

def priority_message(message):
    global k
    k = True
    print('Начало цикла')
    while k:
        min = datetime.datetime.now().minute
        hour = datetime.datetime.now().hour
        if (min < 10):
            min = '0' + str(min)
        current_time = str(hour) + ':' + str(min)
        print('Итерация '+ current_time)
        info = bd_def.get_prior()
        for i in range(len(info)):
            if(info[i][2] == current_time):
                bot.send_message(info[i][0],info[i][1])
                report(message,'message by priority',current_time,info[i][1])
        for i in range(60):
            if not k:
                break
            time.sleep(1)
    print('Конец цикла')

@bot.message_handler(content_types=['text'])
def note(message):
    bd_def.add_note(message.chat.id,message.chat.username,message.text)
    bot.send_message(message.chat.id,"Заметка добавлена. По команде /notes Вы можете посмотреть все свои заметки")
    report(message,"note")

bot.polling()

