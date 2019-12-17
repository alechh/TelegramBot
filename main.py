import telebot
import keyboards
import data
import time
import datetime
import bd_def
import random

bot = telebot.TeleBot(data.get_token())  # инициализация бота

try:
    def report(message, event,text=None, prior=None):# отчет в консоль об инициализации пользователя (устаревшая версия)
        try:
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
        except: print('У '+ str(message.chat.id) +' нет username или firstname')

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
        if(time == 'Сохранить как заметку'):
            just_note(message)
            bot.send_message(message.chat.id, "Готово\n/notes - посмотреть заметки\n/del_notes - удалить заметки",reply_markup=keyboards.delete_keyboard())
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
            print(cmin)
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
        if (not bd_def.table_exists('users')):
            bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')
        elif(not bd_def.user_exists('users',message.chat.id)):
            bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')  # добавление пользователя в базу данных
        else:
            bd_def.update_user(message.chat.id, str(message.chat.username), str(message.chat.first_name), str(message.chat.last_name), 'None', 'None')
        bot.send_message(message.from_user.id, '/set_priority - установить ежедневные напоминания \n /set_time - установить время отправки советов')

    @bot.message_handler(commands=['del_key'])
    def delete_keyboard(message): # удаление клавиатуры в телеграме
        bot.send_message(message.chat.id, "Клавиатура удалена ", reply_markup=keyboards.delete_keyboard())

    @bot.message_handler(commands=['set_time'])
    def set_u_time(message): # начало установки времени для советов
        bot.send_message(message.chat.id,"Установленное время : "+ bd_def.get_advice_time(message.chat.id) +"\nВведите время, когда вам было бы удобно получать советы (например, 12:00)\nЕсли хотите отключить отправку советов, напишите -")
        bot.register_next_step_handler(message, is_user_time_correct)

    def set_user_time(message, q = True): # установка времени для советов
        if q:
            bd_def.set_user_time(message.chat.id,message.text)
            bot.send_message(message.chat.id, "Время принято\n /set_time - изменить время\n /advice - получить совет")
            report(message,'set_user_time',message.text)
        else:
            bd_def.set_user_time(message.chat.id, "None")
            bot.send_message(message.chat.id, "Готово\n /advice - получить совет")
            report(message,'set_user_time',"None")
        global k
        k = False
        time.sleep(2)
        notifications(message)
        return 0

    def error_user_time(message): # обработка неправильного времени для советов
        bot.send_message(message.chat.id, "Неверный формат времени.")
        set_u_time(message)

    @bot.message_handler(commands=['set_priority'])
    def start_prioriry(message): # начало установки приоритетов
        bot.send_message(message.chat.id, "Введите или выберите ежедневное напоминание:", reply_markup=keyboards.priority_key())
        bot.register_next_step_handler(message, set_priority)

    def set_priority(message, q = True): # установка приоритетов
        if(message.text == "Завершить"):
            bot.send_message(message.chat.id, "Готово \n /priority - посмотреть ежедневные напоминания \n /del_priority - удалить ежедневные напоминания",reply_markup=keyboards.delete_keyboard())
            global k
            k = False
            time.sleep(2)
            notifications(message)
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

    def set_time(message): # установка времени для приоритета
        bot.send_message(message.chat.id, "Ежедневное напоминание создано\n/priority - посмотреть ежедневные напоминания\n/del_priority - удалить ежедневные напоминания", reply_markup=keyboards.delete_keyboard())
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
        report(message,'time of priority')

    def error_time(message): # обработка неправильного времени для приоритета
        bot.send_message(message.chat.id,"Неверный формат времени")
        set_priority(message,False)

    @bot.message_handler(commands=['notes'])
    def print_notes(message): # вывод заметок пользователя
        count = bd_def.number_of_notes(message.chat.id)
        if(count==0):
            bot.send_message(message.chat.id,"У вас нет заметок")
            report(message,'not notes')
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
        report(message,"list of notes")

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
            print('Итерация '+ current_date)
            info_prior = bd_def.get_prior()
            info_user_time = bd_def.get_users_time()
            info_note_time = bd_def.get_note_time()
            for i in range(len(info_prior)):
                if(info_prior[i][2] == current_time):
                    try:
                        bot.send_message(info_prior[i][0],info_prior[i][1])
                        report(message,'message by priority',current_time,info_prior[i][1])
                    except:
                        print(str(info_prior[i][0]) +' заблокировал бота')
            for i in range(len(info_user_time)):
                if(info_user_time[i][1] == current_time):
                    advices = bd_def.get_from_bd('advices','advice')
                    rand = random.randint(0,len(advices)-1)
                    try:
                        bot.send_message(info_user_time[i][0], advices[rand])
                        report(message,'advice',advices[rand])
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

    @bot.message_handler(commands=['del_notes'])
    def start_del_nodes(message): # начало удаления заметок
        count = bd_def.number_of_notes(message.chat.id)
        if (count == 0):
            bot.send_message(message.chat.id, "У вас нет заметок")
            report(message, 'not notes')
            return 0
        bot.send_message(message.chat.id, "Введите номер заметки, которую хотите удалить",reply_markup=keyboards.complete_key())
        print_notes(message)
        bot.register_next_step_handler(message, del_notes)

    def del_notes(message): # удаление заметок пользователя
        count = bd_def.number_of_notes(message.chat.id)
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
            bot.send_message(message.chat.id, "Должно быть натуральное число меньше "+ str(count+1))
            bot.register_next_step_handler(message, del_notes)

    @bot.message_handler(commands=['priority'])
    def print_priorities(message): # вывод приоритетов пользователя
        if (not bd_def.table_exists('prior')):
            bot.send_message(message.chat.id,"У вас нет ежедневных напоминаний")
            report(message,'not priority')
            return 0
        info = bd_def.get_priority(message.chat.id)
        if (len(info) == 0):
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            report(message,'not priority')
            return 0
        res = ''
        for i in range(len(info)):
            res = res +str(i+1)+'. '+ info[i][0] + ' ('+info[i][1]+')\n'
        bot.send_message(message.chat.id,res)

    @bot.message_handler(commands=['del_priority'])
    def start_del_priority(message): # начало удаления приоритетов
        count = bd_def.number_of_priority(message)
        if (count == 0):
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            report(message,'not priority')
            return 0
        bot.send_message(message.chat.id, "Введите номер напоминания, который хотите удалить",reply_markup=keyboards.complete_key())
        print_priorities(message)
        bot.register_next_step_handler(message, del_priority)

    def del_priority(message): # удаление приоритетов пользователя
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
            bot.send_message(message.chat.id, "Должно быть натуральное число меньше "+ str(count+1))
            bot.register_next_step_handler(message, del_priority)

    @bot.message_handler(commands=['advice'])
    def send_advice(message):
        advices = bd_def.get_from_bd('advices', 'advice')
        rand = random.randint(0, len(advices) - 1)
        try:
            bot.send_message(message.chat.id, advices[rand])
            report(message, 'advice', advices[rand])
        except:
            print(str(message.chat.id) + ' заблокировал бота')

    @bot.message_handler(commands=['add_advice'])
    def start_add_advice(message):
        if(message.chat.id == 260009462 or message.chat.id == 944242100):
            bot.send_message(message.chat.id,"Какой совет добавить?")
            bot.register_next_step_handler(message, add_advice)

    def add_advice(message):
        bd_def.add_advice(message.text)
        bot.send_message(message.chat.id,"Совет добавлен")

    @bot.message_handler(content_types=['text'])
    def note(message, q = True): # довавление заметки пользователя
        if (q):
            try:
                number = bd_def.number_of_notes(message.chat.id)
            except:
                number = 0
            bd_def.add_note(number+1,message.chat.id,message.chat.username,message.text)
        bot.send_message(message.chat.id,"Нажмите Сохранить как заметку или напишите, когда вам напомнить (ДД.ММ.ГГГГ ЧЧ:ММ)\n(если нужно напомнить в ближайшие сутки, то только время)",reply_markup=keyboards.as_note_key())
        bot.register_next_step_handler(message, is_note_time_correct)

    def set_note_time(message,curtime):
        bot.send_message(message.chat.id, "Напоминание создано",reply_markup=keyboards.delete_keyboard())
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
        bot.send_message(message.chat.id, "Неверный формат даты или этот день уже прошел")
        note(message,False)

    def just_note(message):
        bd_def.just_note(message.chat.id)
        return 0


    bot.polling()

except Exception as err:
    bot.send_message(260009462, "Ошибка:  \n" + str(err))

