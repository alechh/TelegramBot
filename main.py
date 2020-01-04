import telebot
import keyboards
import data
import time
import datetime
import bd_def
import random
import traceback
import time_def

bot = telebot.TeleBot(data.get_token())
k = False

try:
    @bot.message_handler(commands=['del_key'])
    def del_keyboard(message):
        bot.send_message(message.chat.id, "Клавиатура удалена ✅", reply_markup=keyboards.del_keyboard())


    @bot.message_handler(commands=['message_to_users'])
    def message_to_users(message):
        if data.is_me(message.chat.id):
            bot.send_message(message.chat.id, "Что написать пользователям ?")
            bot.register_next_step_handler(message, send_message_to_users)


    def send_message_to_users(message):
        info = bd_def.get_column_from_table('users', 'user_id')
        for i in info:
            try:
                bot.send_message(int(i), message.text)
            except IndexError:
                print(i + ' заблокировал бота')


    @bot.message_handler(commands=['add_advice'])
    def start_add_advice(message):
        if data.is_admins(message.chat.id):
            bot.send_message(message.chat.id, "Какой совет добавить?")
            bot.register_next_step_handler(message, add_advice)


    def add_advice(message):
        bd_def.add_advice(message.text)
        bot.send_message(message.chat.id, "Совет добавлен ✅\nТеперь их: " + str(bd_def.number_of_advices()))


    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.send_message(message.chat.id, data.get_help())


    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, data.get_greeting())
        if not bd_def.user_exists('users', message.chat.id):
            bd_def.add_user(message.chat.id, str(message.chat.username), str(message.chat.first_name),
                            str(message.chat.last_name), 'None', 'None')
            bot.send_message(data.get_my_id(), "New user")
        else:
            bd_def.update_user(message.chat.id, str(message.chat.username), str(message.chat.first_name),
                               str(message.chat.last_name), 'None', 'None')
        bot.send_message(message.chat.id, '/help - список команд ')


    @bot.message_handler(commands=['on'])
    def notifications(message="None"):
        if data.is_me(message.chat.id):
            bot.send_message(message.chat.id, "👌")
        global k
        k = True
        print('Начало цикла')
        while k:
            minute = datetime.datetime.now().minute
            hour = datetime.datetime.now().hour
            day = datetime.datetime.now().day
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            if minute < 10:
                minute = '0' + str(minute)
            if day < 10:
                day = '0' + str(day)
            if month < 10:
                month = '0' + str(month)
            current_date = str(day) + '.' + str(month) + '.' + str(year) + ' ' + str(hour) + ':' + str(minute)
            current_time = str(hour) + ':' + str(minute)
            if int(minute) % 30 == 0:
                print('Итерация ' + current_date)
            info_daily = bd_def.get_daily_n()
            info_user_time = bd_def.get_advice_time_n()
            info_note_time = bd_def.get_users_notes_n()
            for i in range(len(info_daily)):
                if info_daily[i][2] == current_time:
                    try:
                        bot.send_message(info_daily[i][0], info_daily[i][1])
                    except IndexError:
                        print(str(info_daily[i][0]) + ' заблокировал бота')
            for i in range(len(info_user_time)):
                if info_user_time[i][1] == current_time:
                    advices = bd_def.get_column_from_table('advices', 'advice')
                    rand = random.randint(0, len(advices) - 1)
                    try:
                        bot.send_message(info_user_time[i][0], advices[rand])
                    except IndexError:
                        print(str(info_user_time[i][0]) + ' заблокировал бота')
            for i in range(len(info_note_time)):
                if info_note_time[i][3] == current_date:
                    try:
                        bot.send_message(info_note_time[i][1], info_note_time[i][2])
                        bd_def.delete_note_time(info_note_time[i][0], str(info_note_time[i][1]),
                                                str(info_note_time[i][2]), info_note_time[i][3])
                    except IndexError:
                        print(str(info_note_time[i][1]) + ' заблокировал бота')
            for i in range(60):
                if not k:
                    break
                time.sleep(1)
        print('Конец цикла')


    @bot.message_handler(commands=['set_time'])
    def advice_time(message):
        bot.send_message(message.chat.id, "Установленное время : " + bd_def.get_advice_time(
            message.chat.id) + "\nВведите время, когда вам было бы удобно получать советы (например, 12:00)\nЕсли "
                               "хотите отключить отправку советов, напишите -")
        bot.register_next_step_handler(message, set_advice_time)


    def set_advice_time(message):
        if message.text == "-":
            bd_def.set_advice_time(message.chat.id, "None")
            bot.send_message(message.chat.id, "Готово ✅\n /advice - получить совет")
            return 0
        if time_def.is_advice_time_correct(message):
            bot.send_message(message.chat.id, "Время принято ✅\n /set_time - изменить время\n /advice - получить совет")
            global k
            k = False
            time.sleep(2)
            notifications()
        else:
            error_advice_time(message)


    def error_advice_time(message):
        bot.send_message(message.chat.id, "Неверный формат времени ❌")
        bot.send_message(message.chat.id, "Введите время, когда вам было бы удобно получать советы (например, "
                                          "12:00)\nЕсли хотите отключить отправку советов, напишите -")
        bot.register_next_step_handler(message, set_advice_time)


    @bot.message_handler(commands=['advice'])
    def send_advice(message):
        advices = bd_def.get_column_from_table('advices', 'advice')
        rand = random.randint(0, len(advices) - 1)
        try:
            bot.send_message(message.chat.id, advices[rand])
        except IndexError:
            print(str(message.chat.id) + ' заблокировал бота')


    @bot.message_handler(commands=['daily'])
    def print_daily(message):
        if not bd_def.table_exists('prior'):
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            return 0
        info = bd_def.get_daily(message.chat.id)
        if len(info) == 0:
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            return 0
        res = ''
        for i in range(len(info)):
            res = res + str(i + 1) + '. ' + info[i][0] + ' (' + info[i][1] + ')\n'
        bot.send_message(message.chat.id, res)


    @bot.message_handler(commands=['set_daily'])
    def start_daily(message):
        bot.send_message(message.chat.id, "Введите или выберите ежедневное напоминание:",
                         reply_markup=keyboards.daily_key())
        bot.register_next_step_handler(message, daily)


    def daily(message):
        if message.text == "Завершить":
            bot.send_message(message.chat.id, "Готово ✅\n/daily - посмотреть ежедневные напоминания\n/del_daily - "
                                              "удалить ежедневные напоминания", reply_markup=keyboards.del_keyboard())
            global k
            k = False
            time.sleep(2)
            notifications()
            return 0
        else:
            try:
                number = bd_def.number_of_daily(message.chat.id)
            except IndexError:
                number = 0
            bd_def.set_daily(number + 1, message.chat.id, message.chat.username, message.text)
            bot.send_message(message.chat.id, "Выберите или введите время", reply_markup=keyboards.time_key())
            bot.register_next_step_handler(message, set_daily)


    def set_daily(message):
        if time_def.is_daily_time_correct(message):
            bot.send_message(message.chat.id, "Ежедневное напоминание создано ✅\n/daily - посмотреть ежедневные "
                                              "напоминания\n/del_daily - удалить ежедневные напоминания",
                             reply_markup=keyboards.del_keyboard())
            global k
            k = False
            time.sleep(2)
            notifications()
        else:
            error_daily_time(message)


    def error_daily_time(message):
        bot.send_message(message.chat.id, "Неверный формат времени ❌")
        bot.send_message(message.chat.id, "Выберите или введите время", reply_markup=keyboards.time_key())
        bot.register_next_step_handler(message, set_daily)


    @bot.message_handler(commands=['del_daily'])
    def print_del_daily(message, q=True):
        info = bd_def.get_daily(message.chat.id)
        if len(info) == 0:
            bot.send_message(message.chat.id, "У вас нет ежедневных напоминаний")
            return 0
        res = 'Выберите, какое напоминание удалить:\n'
        for i in range(len(info)):
            res = res + str(i + 1) + '. ' + info[i][0] + ' (' + info[i][1] + ')\n'
        key = keyboards.inline_daily(len(info))
        if q:
            bot.send_message(message.chat.id, res, reply_markup=key)
        else:
            bot.edit_message_text(text=res, chat_id=message.chat.id, message_id=message.message_id, reply_markup=key)


    @bot.message_handler(commands=['notes'])
    def print_notes(message):
        count = bd_def.number_of_notes(message.chat.id)
        if count == 0:
            bot.send_message(message.chat.id, "У вас нет заметок")
            return 0
        notes = bd_def.get_notes(message.chat.id)
        res = ''
        count = 1
        for i in notes:
            if bd_def.get_note_time(message.chat.id, str(i)) != 'None':
                res += str(count) + '. ' + str(i) + ' (' + bd_def.get_note_time(message.chat.id, str(i)) + ')\n'
            else:
                res += str(count) + '. ' + str(i) + '\n'
            count += 1
        bot.send_message(message.chat.id, res)


    @bot.message_handler(commands=['del_notes'])
    def print_del_notes(message, q=True):
        count = bd_def.number_of_notes(message.chat.id)
        if count == 0:
            bot.send_message(message.chat.id, "У вас нет заметок")
            return 0
        notes = bd_def.get_notes(message.chat.id)
        res = 'Выберите заметку, которую хотите удалить:\n'
        count = 1
        for i in notes:
            if bd_def.get_note_time(message.chat.id, str(i)) != 'None':
                res += str(count) + '. ' + str(i) + ' (' + bd_def.get_note_time(message.chat.id, str(i)) + ')\n'
            else:
                res += str(count) + '. ' + str(i) + '\n'
            count += 1
        key = keyboards.inline_note(count)
        if q:
            bot.send_message(message.chat.id, res, reply_markup=key)
        else:
            bot.edit_message_text(text=res, chat_id=message.chat.id, message_id=message.message_id, reply_markup=key)


    @bot.message_handler(content_types=['text'])
    def note(message, q=True):
        if q:
            try:
                number = bd_def.number_of_notes(message.chat.id)
            except IndexError:
                number = 0
            bd_def.add_note(number + 1, message.chat.id, message.chat.username, message.text)
        bot.send_message(message.chat.id, "Сохраните как заметку или введите дату напоминания (дд.мм.гггг чч:мм)\n("
                                          "если напомнить в ближайшие сутки, то только время)",
                         reply_markup=keyboards.as_note_key())
        bot.register_next_step_handler(message, set_note)


    def set_note(message):
        if message.text == "Сохранить как заметку ✓":
            just_note(message)
            bot.send_message(message.chat.id, "Готово ✅\n/notes - посмотреть заметки\n/del_notes - удалить заметки",
                             reply_markup=keyboards.del_keyboard())
            return 0
        elif message.text == "Отмена ✖":
            bd_def.cancel_note(message.chat.id)
            bot.send_message(message.chat.id, "😉", reply_markup=keyboards.del_keyboard())
            return 0
        if time_def.is_note_time_correct(message):
            bot.send_message(message.chat.id, "Напоминание создано ✅", reply_markup=keyboards.del_keyboard())
            global k
            k = False
            time.sleep(2)
            notifications()
        else:
            error_note_time(message)


    def error_note_time(message):
        bot.send_message(message.chat.id, "Неверный формат даты или этот день уже прошел ❌")
        bot.send_message(message.chat.id, "Сохраните как заметку или введите дату напоминания (дд.мм.гггг чч:мм)\n("
                                          "если напомнить в ближайшие сутки, то только время)",
                         reply_markup=keyboards.as_note_key())
        bot.register_next_step_handler(message, set_note)


    def just_note(message):
        bd_def.just_note(message.chat.id)
        return 0


    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if "d" not in call.data:
            count = bd_def.number_of_notes(call.message.chat.id)
            bd_def.delete_note(call)
            if count == 1:
                bot.edit_message_text(text="Заметок нет ✅", chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                return 0
            print_del_notes(call.message, False)
        else:
            count = bd_def.number_of_daily(call.message.chat.id)
            bd_def.delete_daily(call)
            if count == 1:
                bot.edit_message_text(text="Напоминаний нет ✅", chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
                return 0
            print_del_daily(call.message, False)


    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            bot.send_message(data.get_my_id(), "Поломка: " + str(e) + '\n' + str(traceback.format_exc()))
            time.sleep(10)
            bot.send_message(data.get_my_id(), "Работаю")

except Exception as err:
    bot.send_message(data.get_my_id(), "Ошибка: " + str(err) + '\n' + str(traceback.format_exc()))
