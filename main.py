import telebot
import keyboards
import data
import time
import datetime
import bd_def
import random
import traceback

bot = telebot.TeleBot(data.get_token())  # инициализация бота

try:
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id,data.get_help())

    @bot.message_handler(commands=['message_to_users'])
    def start_mtou(message):
        bot.send_message(message.chat.id, "Что написать пользователям ?")
        bot.register_next_step_handler(message, message_to_users)

    def message_to_users(message):
        info = bd_def.get_from_bd('users', 'user_id')
        for i in info:
            try:
                bot.send_message(int(i),message.text)
            except:
                print(i +' заблокировал бота')

    def is_note_time_correct(message): #проверка на корректность времени для напоминаний
        time = message.text
        if(time == "Отмена ✖"):
            bd_def.cancel_note(message.chat.id)
            bot.send_message(message.chat.id, "😉",reply_markup=keyboards.delete_keyboard())
            return 0
        if(time == 'Сохранить как заметку ✓'):
            just_note(message)
            bot.send_message(message.chat.id, "Готово ✅\n/notes - посмотреть заметки\n/del_notes - удалить заметки",reply_markup=keyboards.delete_keyboard())
            return 0
        q = False
        if(len(time) == 16):
            cday = time[:2]
            cmonth = time[3:]
            cmonth = cmonth[:2]
            cyear = time[6:]
            cyear = cyear[:4]
            chour = time[11:]
            chour = chour[:2]
            cmin = time[14:]
            q = True
        elif(len(time)==15):
            cday = time[:2]
            cmonth = time[3:]
            cmonth = cmonth[:2]
            cyear = time[6:]
            cyear = cyear[:4]
            chour = time[11:]
            chour = chour[:1]
            cmin = time[13:]
            q = True
        elif (len(time) == 5):
            chour = time[:2]
            cmin = time[3:]
            if(int(chour)<datetime.datetime.now().hour):
                cday = str(datetime.datetime.now().day+1)
            elif (int(chour)==datetime.datetime.now().hour and int(cmin)<= datetime.datetime.now().minute):
                cday = str(datetime.datetime.now().day+1)
            else:
                cday = str(datetime.datetime.now().day)
            cmonth = str(datetime.datetime.now().month)
            cyear = str(datetime.datetime.now().year)

            q = True
        elif (len(time) == 4):
            chour = time[:1]
            cmin = time[2:]
            if(int(chour)<datetime.datetime.now().hour):
                cday = str(datetime.datetime.now().day+1)
            elif (int(chour)==int(datetime.datetime.now().hour) and int(cmin)<= datetime.datetime.now().minute):
                cday = str(datetime.datetime.now().day+1)
            else:
                cday = str(datetime.datetime.now().day)
            cmonth = str(datetime.datetime.now().month)
            cyear = str(datetime.datetime.now().year)
            q = True
        if(q and cmin.isdigit() and cmonth.isdigit()):
            if (int(cmin) < 10 and int(cmin) != 0 and len(cmin)==1):
                cmin = '0' + cmin
            if (int(cmonth) < 10 and int(cmonth)!= 0 and len(cmonth)==1):
                cmonth = '0' + cmonth
        #l = len(time)
        if(q):
            if(cday.isdigit() and cmonth.isdigit() and cyear.isdigit() and chour.isdigit() and cmin.isdigit() and int(cyear) >2018 and int(cmonth)>0 and int(cmonth)<13 and int(cday)>0 and int(cday)<32 and int(chour)>=0 and int(chour)<24 and int(cmin)>=0 and int(cmin)<60 ):
                set_note_time(message,cday+'.'+cmonth+'.'+cyear+' '+chour+':'+cmin)
                return 0
        else:
            error_note_time(message)
            return 0
        error_note_time(message)
        return 0

    def is_user_time_correct(message): #проверка на корректность времени для советов
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
        elif (l==3):
            hour = time[:1]
            min = time[1:]
        else:
            error_user_time(message)
            return 0
        if (hour.isdigit() and min.isdigit() and int(hour) < 24 and int(min) < 60):
            set_user_time(message)
            return 0
        error_user_time(message)

    def is_time_correct(message): #проверка времени на корректность для приоритетов
        time = message.text
        l = len(time)
        if (l ==5):
            hour = time[:2]
            min = time[3:]
        elif (l==4):
            hour = time[:1]
            min = time[2:]
        elif (l==3):
            hour = time[:1]
            min = time[1:]
        else:
            error_time(message)
            return 0
        if (hour.isdigit() and min.isdigit() and int(hour) <24 and int(min) <60):
            set_time(message)
            return 0
        error_time(message)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, data.get_greeting())
        if(not bd_def.user_exists('users',message.chat.id)):
            bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')  # добавление пользователя в базу данных
        else:
            bd_def.update_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')
        bot.send_message(message.from_user.id, '/help - список команд ')

    @bot.message_handler(commands=['del_key'])
    def delete_keyboard(message): # удаление клавиатуры в телеграме
        bot.send_message(message.chat.id, "Клавиатура удалена ✅", reply_markup=keyboards.delete_keyboard())

    @bot.message_handler(commands=['set_time'])
    def set_u_time(message): # начало установки времени для советов
        bot.send_message(message.chat.id,"Установленное время : "+ bd_def.get_advice_time(message.chat.id) +"\nВведите время, когда вам было бы удобно получать советы (например, 12:00)\nЕсли хотите отключить отправку советов, напишите -")
        bot.register_next_step_handler(message, is_user_time_correct)

    def set_user_time(message, q = True): # установка времени для советов
        if q:
            bd_def.set_user_time(message.chat.id,message.text)
            bot.send_message(message.chat.id, "Время принято ✅\n /set_time - изменить время\n /advice - получить совет")
        else:
            bd_def.set_user_time(message.chat.id, "None")
            bot.send_message(message.chat.id, "Готово ✅\n /advice - получить совет")
        global k
        k = False
        time.sleep(2)
        notifications(message)
        return 0

    def error_user_time(message): # обработка неправильного времени для советов
        bot.send_message(message.chat.id, "Неверный формат времени ❌")
        set_u_time(message)

    @bot.message_handler(commands=['set_daily'])
    def start_prioriry(message): # начало установки приоритетов
        bot.send_message(message.chat.id, "Введите или выберите ежедневное напоминание:", reply_markup=keyboards.priority_key())
        bot.register_next_step_handler(message, set_priority)

    def set_priority(message, q = True): # установка приоритетов
        if(message.text == "Завершить"):
            bot.send_message(message.chat.id, "Готово ✅\n /daily - посмотреть ежедневные напоминания \n /del_daily - удалить ежедневные напоминания",reply_markup=keyboards.delete_keyboard())
            global k
            k = False
            time.sleep(2)
            notifications(message)
            return 0
        else:
            if (q):
                try:
                    number = bd_def.number_of_priority(message.chat.id)
                except:
                    number = 0
                bd_def.set_priority(number+1,message.chat.id,message.chat.username,message.text)
            bot.send_message(message.chat.id, "Выберите или введите время", reply_markup=keyboards.time_key())
            bot.register_next_step_handler(message, is_time_correct)

    def set_time(message): # установка времени для приоритета
        bot.send_message(message.chat.id, "Ежедневное напоминание создано ✅\n/daily - посмотреть ежедневные напоминания\n/del_daily - удалить ежедневные напоминания", reply_markup=keyboards.delete_keyboard())
        ctime = message.text
        if not ':' in ctime:
            if len(ctime)==4:
                h = ctime[:2]
                m = ctime[2:]
            elif len(ctime)==3:
                h = ctime[:1]
                m = ctime[1:]
            ctime = h + ':' + m

        bd_def.set_time(message.chat.id,ctime)
        global k
        k = False
        time.sleep(2)
        notifications(message)

    def error_time(message): # обработка неправильного времени для приоритета
        bot.send_message(message.chat.id,"Неверный формат времени ❌")
        set_priority(message,False)

    @bot.message_handler(commands=['notes'])
    def print_notes(message): # вывод заметок пользователя
        count = bd_def.number_of_notes(message.chat.id)
        if(count==0):
            bot.send_message(message.chat.id,"У вас нет заметок")
            return 0
        notes = []
        notes = bd_def.get_notes(message.chat.id)
        res = ''
        count = 1
        for i in notes:
            if(bd_def.get_time_for_note(message.chat.id,str(i)) != 'None'):
                res += str(count) + '. ' + str(i) +' ('+bd_def.get_time_for_note(message.chat.id,str(i)) +')\n'
            else:
                res += str(count)+'. ' + str(i) + '\n'
            count += 1
        bot.send_message(message.chat.id,res)

    @bot.message_handler(commands=['del_notes'])
    def print_del_notes(message, q = True):
        count = bd_def.number_of_notes(message.chat.id)
        if (count == 0):
            bot.send_message(message.chat.id, "У вас нет заметок")
            return 0
        notes = []
        notes = bd_def.get_notes(message.chat.id)
        res = 'Выберите заметку, которую хотите удалить:\n'
        count = 1
        for i in notes:
            if(bd_def.get_time_for_note(message.chat.id,str(i)) != 'None'):
                res += str(count) + '. ' + str(i) +' ('+bd_def.get_time_for_note(message.chat.id,str(i)) +')\n'
            else:
                res += str(count)+'. ' + str(i) + '\n'
            count += 1
        key= keyboards.inline_note(count)
        if q:
            bot.send_message(message.chat.id,res,reply_markup=key)
        else:
            bot.edit_message_text(text=res,chat_id=message.chat.id,message_id=message.message_id,reply_markup=key)

    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if not "d" in call.data:
            number = call.data
            count = bd_def.number_of_notes(call.message.chat.id)
            bd_def.delete_note(call)
            if count == 1:
                bot.edit_message_text(text="Заметок нет ✅",chat_id=call.message.chat.id,message_id=call.message.message_id)
                return 0
            print_del_notes(call.message,False)
        else:
            number = call.data
            count = bd_def.number_of_priority(call.message.chat.id)
            bd_def.delete_priority(call)
            if count == 1:
                bot.edit_message_text(text="Напоминаний нет ✅", chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                return 0
            print_del_priorities(call.message,False)

    @bot.message_handler(commands=['on'])
    def notifications(message): # отправка советов и напоминаний пользователю
        global k
        k = True
        print('Начало цикла')
        while k:
            min = datetime.datetime.now().minute
            hour = datetime.datetime.now().hour
            day = datetime.datetime.now().day
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            if (min < 10):
                min = '0' + str(min)
            if(day <10):
                day = '0'+str(day)
            if(month<10):
                month = '0'+str(month)
            current_date= str(day)+'.'+str(month)+'.'+str(year)+' '+str(hour)+':'+str(min)
            current_time = str(hour) + ':' + str(min)
            if (int(min) % 30 == 0):
                print('Итерация '+ current_date)
            info_prior = bd_def.get_prior()
            info_user_time = bd_def.get_users_time()
            info_note_time = bd_def.get_note_time()
            for i in range(len(info_prior)):
                if(info_prior[i][2] == current_time):
                    try:
                        bot.send_message(info_prior[i][0],info_prior[i][1])
                    except:
                        print(str(info_prior[i][0]) +' заблокировал бота')
            for i in range(len(info_user_time)):
                if(info_user_time[i][1] == current_time):
                    advices = bd_def.get_from_bd('advices','advice')
                    rand = random.randint(0,len(advices)-1)
                    try:
                        bot.send_message(info_user_time[i][0], advices[rand])
                    except:
                        print(str(info_user_time[i][0])+' заблокировал бота')
            for i in range(len(info_note_time)):
                if(info_note_time[i][3] == current_date):
                    try:
                        bot.send_message(info_note_time[i][1],info_note_time[i][2])
                        bd_def.delete_note_time(info_note_time[i][0],str(info_note_time[i][1]),str(info_note_time[i][2]),info_note_time[i][3])
                    except:
                        print(str(info_note_time[i][1])+' заблокировал бота')
            for i in range(60):
                if not k:
                    break
                time.sleep(1)
        print('Конец цикла')

    @bot.message_handler(commands=['daily'])
    def print_priorities(message): # вывод приоритетов пользователя
        if (not bd_def.table_exists('prior')):
            bot.send_message(message.chat.id,"У вас нет ежедневных напоминаний")
            return 0
        info = bd_def.get_priority(message.chat.id)
        if (len(info) == 0):
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            return 0
        res = ''
        for i in range(len(info)):
            res = res +str(i+1)+'. '+ info[i][0] + ' ('+info[i][1]+')\n'
        bot.send_message(message.chat.id,res)

    @bot.message_handler(commands=['del_daily'])
    def print_del_priorities(message,q=True):
        info = bd_def.get_priority(message.chat.id)
        if (len(info) == 0):
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            return 0
        res = 'Выберите, какое напоминание удалить:\n'
        for i in range(len(info)):
            res = res + str(i + 1) + '. ' + info[i][0] + ' (' + info[i][1] + ')\n'
        key =keyboards.inline_daily(len(info))
        if q:
            bot.send_message(message.chat.id, res,reply_markup=key)
        else:
            bot.edit_message_text(text=res, chat_id=message.chat.id, message_id=message.message_id, reply_markup=key)

    @bot.message_handler(commands=['advice'])
    def send_advice(message):
        advices = bd_def.get_from_bd('advices', 'advice')
        rand = random.randint(0, len(advices) - 1)
        try:
            bot.send_message(message.chat.id, advices[rand])
        except:
            print(str(message.chat.id) + ' заблокировал бота')

    @bot.message_handler(commands=['add_advice'])
    def start_add_advice(message):
        if(message.chat.id == 260009462 or message.chat.id == 944242100):
            bot.send_message(message.chat.id,"Какой совет добавить?")
            bot.register_next_step_handler(message, add_advice)

    def add_advice(message):
        bd_def.add_advice(message.text)
        bot.send_message(message.chat.id,"Совет добавлен ✅\nТеперь их: "+str(bd_def.number_of_advices()))

    @bot.message_handler(content_types=['text'])
    def note(message, q = True): # довавление заметки пользователя
        if (q):
            try:
                number = bd_def.number_of_notes(message.chat.id)
            except:
                number = 0
            bd_def.add_note(number+1,message.chat.id,message.chat.username,message.text)
        bot.send_message(message.chat.id,"Сохраните как заметку или введите дату напоминания (дд.мм.гггг чч:мм)\n(если напомнить в ближайшие сутки, то только время)",reply_markup=keyboards.as_note_key())
        bot.register_next_step_handler(message, is_note_time_correct)

    def set_note_time(message,curtime):
        bot.send_message(message.chat.id, "Напоминание создано ✅",reply_markup=keyboards.delete_keyboard())
        if not ':' in curtime:
            if len(curtime)==4:
                h = curtime[:2]
                m = curtime[2:]
            elif len(curtime)==3:
                h = curtime[:1]
                m = curtime[1:]
            curtime = h + ':' + m
        bd_def.set_note_time(message.chat.id,curtime)
        global k
        k = False
        time.sleep(2)
        notifications(message)

    def error_note_time(message):
        bot.send_message(message.chat.id, "Неверный формат даты или этот день уже прошел ❌")
        note(message,False)

    def just_note(message):
        bd_def.just_note(message.chat.id)
        return 0

    while True:
        try:
            bot.polling()
        except Exception as e:
            bot.send_message(260009462, "Поломка: " + str(e) + '\n' + str(traceback.format_exc()))
            time.sleep(10)
            bot.send_message(260009462, "Работаю")

except Exception as err:
    bot.send_message(260009462, "Ошибка: " + str(err) + '\n' + str(traceback.format_exc()))

