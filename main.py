import telebot
#from telebot import apihelper
import keyboards
import data
import time
import datetime
import bd_def
import random

#apihelper.proxy = {'https': data.get_proxy()}  # proxy
bot = telebot.TeleBot(data.get_token())  # инициализация бота
#q = True # глобальная переменная для корректной работы цикла с проверкой времени

def report(message, event,text=None, prior=None): # отчет в консоль об инициализации пользователя
    if event == 'priority':
        print(message.chat.first_name + ' выбрал приоритет : '+ message.text)
    elif event =='time of priority':
        print(message.chat.first_name + ' выбрал время для приоритета : '+message.text)
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
    elif event == 'set_user_time':
        print(message.chat.first_name + ' установил время для советов ' + text)
    elif event == 'advice':
        print(message.chat.first_name + ' получил совет : ' + text)


@bot.message_handler(commands=['message_to_users'])
def start_mtou(message):
    bot.send_message(message.chat.id, "Что написать пользователям ?")
    bot.register_next_step_handler(message, messge_to_users)

def messge_to_users(message):
    info = bd_def.get_from_bd('users', 'user_id')
    for i in info:
        bot.send_message(int(i),message.text)

def is_user_time_correct(message):
    time = message.text
    if(time == '-'):
        set_user_time(message,False)
        return 0
    l = len(time)
    if (l == 5):
        hour = time[:2]
        min = time[3:]
    elif (l == 4):
        hour = time[:1]
        min = time[2:]
    else:
        error_user_time(message)
        return 0
    if (hour.isdigit() and min.isdigit() and int(hour) < 24 and int(min) < 60):
        set_user_time(message)
        return 0
    error_user_time(message)

def is_time_correct(message): #проверка правильности времени
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

@bot.message_handler(commands=['start'])
def start(message):  # получение имени
    bot.send_message(message.chat.id, data.get_greeting())
    if (not bd_def.table_exists('users')):
        bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')
    elif(not bd_def.user_exists('users',message.chat.id)):
        bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')  # добавление пользователя в базу данных
    else:
        bd_def.update_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')
    bot.send_message(message.from_user.id, '/set_priority - установить приоритеты \n /set_time - установить время отправки советов')

@bot.message_handler(commands=['del_key'])
def delete_keyboard(message):
    bot.send_message(message.chat.id, "Клавиатура удалена ", reply_markup=keyboards.delete_keyboard())

@bot.message_handler(commands=['set_time'])
def set_u_time(message):
    bot.send_message(message.chat.id,"Введите время, когда вам было бы удобно получать советы (например, 12:00)\nЕсли хотите отключить отправку советов, напишите -")
    bot.register_next_step_handler(message, is_user_time_correct)

def set_user_time(message, q = True):
    global adv_k
    if (q):
        bd_def.set_user_time(message.chat.id,message.text)
        bot.send_message(message.chat.id, "Время принято\n /set_time - изменить время")
        report(message,'set_user_time',message.text)
        adv_k = False
        time.sleep(2)
        send_advices(message)
        return 0
    else:
        bd_def.set_user_time(message.chat.id, "None")
        bot.send_message(message.chat.id, "Готово")
        report(message,'set_user_time',"None")
        adv_k = False
        time.sleep(2)
        send_advices(message)
        return 0

def error_user_time(message):
    bot.send_message(message.chat.id, "Неверный формат времени.")
    set_u_time(message)

@bot.message_handler(commands=['set_priority'])
def start_prioriry(message):
    bot.send_message(message.chat.id, "Выберите приоритеты:", reply_markup=keyboards.priority_key())
    bot.register_next_step_handler(message, set_priority)

def set_priority(message, q = True):
    if(message.text == "Завершить"):
        bot.send_message(message.chat.id, "Готово \n /priority - посмотреть приоритеты \n /del_priority - удалить приоритеты",reply_markup=keyboards.delete_keyboard())
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
            bd_def.set_priority(number+1,message.chat.id,message.chat.username,message.text)
        bot.send_message(message.chat.id, "Выберите или введите время", reply_markup=keyboards.time_key())
        bot.register_next_step_handler(message, is_time_correct)

def set_time(message):
    bot.send_message(message.chat.id, "Время принято", reply_markup=keyboards.delete_keyboard())
    bd_def.set_time(message.chat.id,message.text)
    global k
    k = False
    time.sleep(2)
    priority_message(message)
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
    notes = bd_def.get_notes((message.chat.id))
    res = ''
    count = 1
    for i in notes:
        res += str(count)+'. ' + str(i) + '\n'
        count += 1
    bot.send_message(message.chat.id,res)
    report(message,"list of notes")

@bot.message_handler(commands=['priority_time'])
def priority_message(message):
    global k
    k = True
    print('Начало цикла приоритетов')
    while k:
        min = datetime.datetime.now().minute
        hour = datetime.datetime.now().hour
        if (min < 10):
            min = '0' + str(min)
        current_time = str(hour) + ':' + str(min)
        print('Итерация приоритетов '+ current_time)
        info = bd_def.get_prior()
        for i in range(len(info)):
            if(info[i][2] == current_time):
                bot.send_message(info[i][0],info[i][1])
                report(message,'message by priority',current_time,info[i][1])
        for i in range(60):
            if not k:
                break
            time.sleep(1)
    print('Конец цикла приоритетов')

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

@bot.message_handler(commands=['priority'])
def print_priorities(message):
    if (not bd_def.table_exists('prior')):
        bot.send_message(message.chat.id,"У вас нет выбранных приоритетов")
        report(message,'not priority')
        return 0
    info = bd_def.get_priority(message.chat.id)
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

@bot.message_handler(commands=['advices_time'])
def send_advices(message):
    global adv_k
    adv_k = True
    print('Начало цикла cоветов')
    while adv_k:
        min = datetime.datetime.now().minute
        hour = datetime.datetime.now().hour
        if (min < 10):
            min = '0' + str(min)
        current_time = str(hour) + ':' + str(min)
        print('Итерация советов '+ current_time)
        info = bd_def.get_users_time()
        for i in range(len(info)):
            if(info[i][1] == current_time):
                advices = bd_def.get_from_bd('advices','advice')
                rand = random.randint(0,len(advices)-1)
                bot.send_message(info[i][0], advices[rand])
                report(message,'advice',advices[rand])
        for i in range(60):
            if not adv_k:
                break
            time.sleep(1)
    print('Конец цикла советов')



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

