import psycopg2


def add_user(user_id, username, firstname, secondname, name, time):  # добавление пользователя в базу данных
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('INSERT OR IGNORE INTO users VALUES(' + str(
        user_id) + ',"' + username + '", "' + firstname + '", "' + secondname + '", "' + name + '", "' + str(
        time) + '")')
    con.commit()
    cur.close()
    con.close()


def set_advice_time(user_id, time):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE users SET time = "' + str(time) + '" WHERE user_id =' + str(user_id))
    con.commit()
    cur.close()
    con.close()


def set_note_time(user_id, time):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE notes SET time = "' + str(time) + '" WHERE user_id=' + str(user_id) + ' AND time =0')
    con.commit()
    cur.close()
    con.close()


def just_note(user_id):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE notes SET time = "None" WHERE user_id=' + str(user_id) + ' AND time =0')
    con.commit()
    cur.close()
    con.close()


def set_daily(number, user_id, username, priority):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO prior VALUES(' + str(number) + ',' + str(user_id) + ',"' + str(
        username) + '","' + priority + '","None")')
    con.commit()
    cur.close()
    con.close()


def set_daily_time(user_id, time):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE prior SET time = "' + str(time) + '" WHERE user_id =' + str(user_id) + ' and time="None"')
    con.commit()
    cur.close()
    con.close()


def add_note(number, user_id, username, note):  # добавление заметки пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute(
        'INSERT INTO notes VALUES(' + str(number) + ',' + str(user_id) + ',"' + str(username) + '","' + note + '","0")')
    con.commit()
    cur.close()
    con.close()


def get_notes(user_id):  # получение заметок конкретного пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT note FROM notes WHERE user_id =' + str(user_id))
    rows = cur.fetchall()
    notes = []
    for row in rows:
        row = str(row)
        row = row[2:]
        length = len(row)
        row = row[:(length - 3)]
        notes.append(row)
    return notes


def get_daily_n():  # получение приоритетов пользователя (for notifications)
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT user_id,priority,time FROM prior')
    rows = cur.fetchall()
    size = len(rows)
    info = []
    for i in range(size):
        info.append([])
        for j in range(3):
            info[i].append(rows[i][j])
    return info


def number_of_notes(user_id):  # кол-во заметок пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id=' + str(user_id))
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    return int(count)


def delete_note(call):  # удаление заметки пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id=' + str(call.message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    count = int(count)
    cur.execute('DELETE FROM notes WHERE user_id=' + str(call.message.chat.id) + ' AND number=' + call.data)
    i = int(call.data) + 1
    while i <= count:
        cur.execute(
            'UPDATE notes SET number = ' + str(i - 1) + ' WHERE user_id=' + str(
                call.message.chat.id) + ' AND number = ' + str(i))
        i = i + 1
    con.commit()
    cur.close()
    con.close()


def delete_note_time(number, user_id, note, time):  # удаление напоминания после отправки
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id=' + str(user_id))
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    count = int(count)
    cur.execute('DELETE FROM notes WHERE note=? AND time=? AND user_id=' + str(user_id), (note, time))
    i = int(number) + 1
    while i <= count:
        cur.execute(
            'UPDATE notes SET number = ' + str(i - 1) + ' WHERE user_id=' + str(user_id) + ' AND number = ' + str(i))
        i = i + 1
    con.commit()
    cur.close()
    con.close()


def table_exists(name):  # проверка на существование таблицы
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'' + name + '\';')
    res = cur.fetchall()
    if len(res) == 0:
        return False
    return True


def get_daily(user_id):  # получение приоритетов пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT priority,time FROM prior WHERE user_id=' + str(user_id))
    rows = cur.fetchall()
    size = len(rows)
    info = []
    for i in range(size):
        info.append([])
        for j in range(2):
            info[i].append(rows[i][j])
    return info


def number_of_daily(chat_id):  # кол-во приоритетов пользователя
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id=' + str(chat_id))
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    return int(count)


def delete_daily(call):  # удаление приоритетов
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id=' + str(call.message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    count = int(count)
    data = call.data[2:]
    cur.execute('DELETE FROM prior WHERE user_id=' + str(call.message.chat.id) + ' and number=' + data)
    i = int(data) + 1
    while i <= count:
        cur.execute(
            'UPDATE prior SET number = ' + str(i - 1) + ' WHERE number = ' + str(i) + ' and user_id=' + str(
                call.message.chat.id))
        i = i + 1
    con.commit()
    cur.close()
    con.close()


def user_exists(table, user_id):  # существует ли запись о пользоветеле с user_id в таблице table
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM ' + table + ' WHERE user_id=' + str(user_id))
    info = str(cur.fetchall())
    if len(info) == 2:
        cur.close()
        con.close()
        return False
    else:
        cur.close()
        con.close()
        return True


def update_user(user_id, username, firstname, secondname, name, time):  # обновить информацию в таблице users
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET username = "' + str(username) + '" WHERE user_id =' + str(user_id))
    cur.execute('UPDATE users SET firstname = "' + str(firstname) + '" WHERE user_id =' + str(user_id))
    cur.execute('UPDATE users SET secondname = "' + str(secondname) + '" WHERE user_id =' + str(user_id))
    cur.execute('UPDATE users SET name = "' + str(name) + '" WHERE user_id =' + str(user_id))
    cur.execute('UPDATE users SET name = "' + str(name) + '" WHERE user_id =' + str(user_id))
    cur.execute('UPDATE users SET time = "' + str(time) + '" WHERE user_id =' + str(user_id))
    con.commit()
    cur.close()
    con.close()


def get_column_from_table(table, column):  # column из таблицы table
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT ' + column + ' FROM ' + table)
    rows = cur.fetchall()
    info = []
    for row in rows:
        row = str(row)
        row = row[1:]
        length = len(row)
        row = row[:(length - 2)]
        if column == 'advice' or column == 'time':
            row = row[1:]
            length = len(row)
            row = row[:(length - 1)]
        info.append(row)
    return info


def get_users_notes_n():  # получение заметок пользователя (for notifications)
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT number,user_id,note,time FROM notes')
    rows = cur.fetchall()
    size = len(rows)
    info = []
    for i in range(size):
        info.append([])
        for j in range(4):
            info[i].append(rows[i][j])
    return info


def get_advice_time_n():  # получение времени отправки советов (for nitifications)
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT user_id,time FROM users')
    rows = cur.fetchall()
    size = len(rows)
    info = []
    for i in range(size):
        info.append([])
        for j in range(2):
            info[i].append(rows[i][j])
    return info


def get_advice_time(user_id):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM users WHERE user_id=' + str(user_id))
    time = cur.fetchall()
    time = str(time[0])
    time = time[2:]
    length = len(time)
    time = time[:(length - 3)]
    return time


def get_note_time(user_id, note):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM notes WHERE user_id=? AND note=?', (str(user_id), note))
    time = cur.fetchall()
    time = str(time[0])
    time = time[2:]
    length = len(time)
    time = time[:(length - 3)]
    return time


def add_advice(advice):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO advices VALUES("' + advice + '")')
    con.commit()
    cur.close()
    con.close()


def number_of_advices():  # кол-во советов
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM advices')
    count = str(cur.fetchall())
    count = count[2:]
    length = len(count)
    count = count[:(length - 3)]
    return int(count)


def cancel_note(user_id):
    con = psycopg2.connect('./database.db')
    cur = con.cursor()
    cur.execute("DELETE from notes WHERE user_id=" + str(user_id) + " AND time = 0")
    con.commit()
    cur.close()
    con.close()
