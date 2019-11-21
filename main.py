import telebot
#from telebot import apihelper
import keyboards
import data
import time
import datetime
import bd_def

#apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота
q = True # глобальная переменная для корректной работы цикла с проверкой времени

def report(message, event,text=None, prior=None): # отчет в консоль об инициализации пользователя
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
        print(message.chat.first_name + " получил сообщение " +prior+" по времени " + text)
    elif event == "delete note":
        print(message.chat.first_name + " удалил заметку")
    elif event == 'not notes':
        print('У '+ message.chat.first_name +' нет заметок')
    elif event == 'delete priority':
        print(message.chat.first_name + ' удалил приоритет')
    elif event == 'not priority':
        print('У ' + message.chat.first_name + ' нет приоритетов')

def is_time_correct(message): #проверка правилности времени
    time = message.text
    l = len(time)
    if (l ==5):
        hour = time[:2]
        min = time[3:]
    elif (l==4):
        hour = time[:1]
        min = time[2:]
    else:
        error_time(message)
        return 0
    if (hour.isdigit() and min.isdigit() and int(hour) <24 and int(min) <60):
        set_time(message)
        return 0
    error_time(message)

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
    bot.send_message(message.from_user.id, 'Теперь по команде /set_category Вы можете установить свою категорию')
    report(message,'name')
    bd_def.add_user(user_id, username, firstname, secondname, name, 'None')  # добавление пользователя в базу данных

@bot.message_handler(commands=['del_key'])
def delete_keyboard(message):
    bot.send_message(message.chat.id, "Клавиатура удалена ", reply_markup=keyboards.delete_keyboard())

@bot.message_handler(commands=['set_category'])
def start_category(message):
    bot.send_message(message.from_user.id, 'К какой категории вы относитесь?')
    bot.send_message(message.from_user.id, "Выбирите категорию:", reply_markup=keyboards.category_key())
    bot.register_next_step_handler(message, set_category)

def set_category(message):
    category = message.text
    if (message.text == 'Студент' or message.text == 'Школьник' or message.text == 'Работающий' or message.text == 'Бездельник'):
        bot.send_message(message.chat.id,"Замечательно, теперь по команде /set_priority Вы можете выбрать приоритеты", reply_markup=keyboards.delete_keyboard())
        bd_def.set_category(message.chat.id, category)
        report(message,'category')
    else:
        bot.send_message(message.chat.id,"Неверная категория, попробуйте снова")
        bot.register_next_step_handler(message, set_category)

@bot.message_handler(commands=['set_priority'])
def start_prioriry(message):
    bot.send_message(message.chat.id, "Выберите приоритеты:", reply_markup=keyboards.priority_key())
    bot.register_next_step_handler(message, set_priority)

def set_priority(message, q = True):
    if(message.text == "Завершить"):
        bot.send_message(message.chat.id, "Готово \n /show_priority - посмотреть приоритеты \n /del_priority - удалить приоритеты",reply_markup=keyboards.delete_keyboard())
        global k
        k = False
        time.sleep(2)
        priority_message(message) #запуск цикла с проверкой времени
        report(message,'success of priority')
        return 0
    else:
        if (q):
            report(message,'priority')
            try:
                number = bd_def.number_of_priority(message)
            except:
                number = 0
            bd_def.create_perfonal_bd(number+1,message.chat.id,message.chat.username,message.text)
        bot.send_message(message.chat.id, "Выберите или введите время", reply_markup=keyboards.time_key())
        bot.register_next_step_handler(message, is_time_correct)

def set_time(message):
    bot.send_message(message.chat.id, "Время принято", reply_markup=keyboards.delete_keyboard())
    bd_def.set_time(message.chat.id,message.text)
    report(message,'time of priority')


@bot.message_handler(commands=['time_error'])
def error_time(message): #нужная функция для проверки времени на корректность
    bot.send_message(message.chat.id,"Неверный формат времени")
    set_priority(message,False)

@bot.message_handler(commands=['notes'])
def print_notes(message):
    if (not bd_def.table_exists('notes'+ str(message.chat.id))):
        bot.send_message(message.chat.id,"У вас нет заметок")
        report(message,'not notes')
        return 0
    count = bd_def.number_of_notes(message)
    if(count==0):
        bot.send_message(message.chat.id,"У вас нет заметок")
        report(message,'not notes')
        return 0
    notes = []
    notes = bd_def.print_notes((message.chat.id))
    res = ''
    count = 1
    for i in notes:
        res += str(count)+'. ' + str(i) + '\n'
        count += 1
    bot.send_message(message.chat.id,res)
    report(message,"list of notes")

@bot.message_handler(commands=['time'])
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

@bot.message_handler(commands=['del_notes'])
def start_del_nodes(message):
    if (not bd_def.table_exists('notes'+ str(message.chat.id))):
        bot.send_message(message.chat.id,"У вас нет заметок")
        report(message,'not notes')
        return 0
    count = bd_def.number_of_notes(message)
    if (count == 0):
        bot.send_message(message.chat.id, "У вас нет заметок")
        report(message, 'not notes')
        return 0
    print_notes(message)
    bot.send_message(message.chat.id, "Введите номер заметки, которую хотите удалить")
    bot.register_next_step_handler(message, del_notes)

def del_notes(message):
    count = bd_def.number_of_notes(message)
    if(message.text == "Завершить"):
        bot.send_message(message.chat.id, "Готово", reply_markup=keyboards.delete_keyboard())
        return 0
    elif (message.text.isdigit() and int(message.text) <= count and int(message.text)>0):
        bd_def.delete_note(message)
        report(message,'delete note')
        if count ==1 :
            bot.send_message(message.chat.id, "Готово", reply_markup=keyboards.delete_keyboard())
            return 0
        print_notes(message)
        bot.send_message(message.chat.id, "Введите следующий номер или нажмите Завершить", reply_markup=keyboards.complete_key())
        bot.register_next_step_handler(message, del_notes)
    else:
        bot.send_message(message.chat.id, "Должно быть натуральное число")
        bot.register_next_step_handler(message, del_notes)

@bot.message_handler(commands=['show_priority'])
def print_priorities(message):
    if (not bd_def.table_exists('prior')):
        bot.send_message(message.chat.id,"У вас нет выбранных приоритетов")
        report(message,'not priority')
        return 0
    info = bd_def.print_priority(message.chat.id)
    if (len(info) == 0):
        bot.send_message(message.chat.id, "У вас нет выбранных приоритетов")
        report(message,'not priority')
        return 0
    res = ''
    for i in range(len(info)):
        res = res +str(i+1)+'. '+ info[i][0] + ' ('+info[i][1]+')\n'
    bot.send_message(message.chat.id,res)

@bot.message_handler(commands=['del_priority'])
def start_del_priority(message):
    count = bd_def.number_of_priority(message)
    if (count == 0):
        bot.send_message(message.chat.id, "У вас нет выбранных приоритетов")
        report(message,'not priority')
        return 0
    print_priorities(message)
    bot.send_message(message.chat.id, "Введите номер приоритета, который хотите удалить")
    bot.register_next_step_handler(message, del_priority)

def del_priority(message):
    count = bd_def.number_of_priority(message)
    if(message.text == "Завершить"):
        bot.send_message(message.chat.id, "Готово", reply_markup=keyboards.delete_keyboard())
        return 0
    elif (message.text.isdigit() and int(message.text) <= count and int(message.text) >0):
        bd_def.delete_priority(message)
        report(message,'delete priority')
        if count == 1 :
            bot.send_message(message.chat.id, "Готово", reply_markup=keyboards.delete_keyboard())
            return 0
        print_priorities(message)
        bot.send_message(message.chat.id, "Введите следующий номер или нажмите Завершить", reply_markup=keyboards.complete_key())
        bot.register_next_step_handler(message, del_priority)
    else:
        bot.send_message(message.chat.id, "Должно быть натуральное число")
        bot.register_next_step_handler(message, del_priority)

@bot.message_handler(content_types=['text'])
def note(message):
    try:
        number = bd_def.number_of_notes(message)
    except:
        number = 0
    bd_def.add_note(number+1,message.chat.id,message.chat.username,message.text)
    bot.send_message(message.chat.id,"Заметка добавлена. \n/notes - посмотреть заметки \n/del_notes - удалить заметки")
    report(message,"note")

bot.polling()

