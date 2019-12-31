import sqlite3

def add_user(user_id,username,firstname,secondname,name,time): # добавление пользователя в базу данных
        #подключение к базе данных
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
        #создание таблицы, если она еще не создана
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, firstname TEXT, secondname TEXT, name TEXT,time TEXT, UNIQUE(user_id,username,firstname,secondname,name,time))')
        #добавление пользователя в таблицу
    cur.execute('INSERT OR IGNORE INTO users VALUES(' + str(user_id) + ',"' + username + '", "' + firstname + '", "' + secondname + '", "'+ name +'", "'+str(time)+'")')
        #сохранение изменений в базе данных
    con.commit()
        #отключение от базы данных
    cur.close()
    con.close()

def set_user_time(user_id,time):  # добавление категории пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE users SET time = "'+str(time) +'" WHERE user_id ='+str(user_id))
    con.commit()
    cur.close()
    con.close()

def set_note_time(user_id,time):  # добавление категории пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE notes SET time = "'+str(time) +'" WHERE user_id='+str(user_id)+' AND time =0')
    con.commit()
    cur.close()
    con.close()

def just_note(user_id):  # добавление категории пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE notes SET time = "None" WHERE user_id='+str(user_id)+' AND time =0')
    con.commit()
    cur.close()
    con.close()

def set_priority(number,user_id,username,priority): # добавление приоритета польщователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    # создание таблицы, если она еще не создана
    cur.execute(
        'CREATE TABLE IF NOT EXISTS prior(number INT,user_id INT, username TEXT, priority TEXT, time TEXT)')
    # добавление пользователя в таблицу
    cur.execute('INSERT INTO prior VALUES(' +str(number) +',' + str(user_id) + ',"' + str(username) + '","'+priority+'","None")')
    # сохранение изменений в базе данных
    con.commit()
    # отключение от базы данных
    cur.close()
    con.close()

def set_time(user_id,time): # установка времени для приоритета пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE prior SET time = "'+str(time) +'" WHERE user_id ='+str(user_id) +' and time="None"')
    con.commit()
    cur.close()
    con.close()

def add_note(number,user_id,username,note): # добавление заметки пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO notes VALUES(' + str(number) +',' + str(user_id) + ',"' + str(username) + '","' + note + '","0")')
    con.commit()
    cur.close()
    con.close()

def get_notes(user_id): # получение заметок конкретного пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT note FROM notes WHERE user_id =' +str(user_id))
    rows = cur.fetchall()
    notes = []
    for row in rows:
        row = str(row)
        row = row[2:]
        l = len(row)
        row = row[:(l - 3)]
        notes.append(row)
    return notes

def get_prior(): # получение приоритетов пользователя (для функции отправки уведомления по времени)
    con = sqlite3.connect('./database.db')
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

def number_of_notes(user_id): # кол-во заметок пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id='+str(user_id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    return int(count)

def delete_note(call): # удаление заметки пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id='+str(call.message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    count = int(count)
    cur.execute('DELETE FROM notes WHERE user_id='+str(call.message.chat.id)+' AND number=' + call.data)
    i = int(call.data)+1
    while i<=count:
        cur.execute(
            'UPDATE notes SET number = ' + str(i-1) + ' WHERE user_id='+str(call.message.chat.id)+' AND number = ' + str(i))
        i = i + 1
    con.commit()
    cur.close()
    con.close()

def delete_note_time(number,user_id,note,time): # удаление напоминания после отправки
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes WHERE user_id='+str(user_id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    count = int(count)
    cur.execute('DELETE FROM notes WHERE note=? AND time=? AND user_id='+str(user_id),(note,time))
    i = int(number)+1
    while i<=count:
        cur.execute(
            'UPDATE notes SET number = ' + str(i-1) + ' WHERE user_id='+str(user_id)+' AND number = ' + str(i))
        i = i + 1
    con.commit()
    cur.close()
    con.close()

def table_exists(name): # проверка на существование таблицы
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\''+name + '\';')
    res = cur.fetchall()
    if(len(res) == 0) :
        return False
    return True

def get_priority(user_id): # получение приоритетов пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT priority,time FROM prior WHERE user_id='+ str(user_id))
    rows = cur.fetchall()
    size = len(rows)
    info = []
    for i in range(size):
        info.append([])
        for j in range(2):
            info[i].append(rows[i][j])
    return info

def number_of_priority(chat_id): # кол-во приоритетов пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id='+ str(chat_id) )
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    return int(count)

def delete_priority(call): # удаление приоритетов
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id=' + str(call.message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    count = int(count)
    data = call.data[2:]
    cur.execute('DELETE FROM prior WHERE user_id='+str(call.message.chat.id)+' and number=' + data)
    i = int(data)+1
    while i<=count:
        cur.execute(
            'UPDATE prior SET number = ' + str(i-1) + ' WHERE number = ' + str(i) +' and user_id='+ str(call.message.chat.id))
        i = i + 1
    con.commit()
    cur.close()
    con.close()

def user_exists(table, user_id): # существует ли запись о пользоветеле с user_id в таблице table
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM '+table+' WHERE user_id=' + str(user_id))
    info = str(cur.fetchall())
    if(len(info) == 2):
        return False
    else:
        return True
    cur.close()
    con.close()

def update_user(user_id, username, firstname, secondname, name, time): # обновить информацию о пользователе в таблице users
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET username = "'+str(username) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET firstname = "'+str(firstname) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET secondname = "'+str(secondname) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET name = "'+str(name) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET name = "'+str(name) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET time = "'+str(time) +'" WHERE user_id ='+str(user_id))
    con.commit()
    cur.close()
    con.close()

def get_time_by_user_id(user_id):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM users WHERE user_id='+ str(user_id))
    info = cur.fetchall()
    info = str(info[0])
    info = info[2:]
    l = len(info)
    info = info[:(l - 3)]
    return info

def get_from_bd(table, column): # колонки column из таблицы table
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT '+column+' FROM ' + table)
    rows = cur.fetchall()
    info = []
    for row in rows:
        row = str(row)
        row = row[1:]
        l = len(row)
        row = row[:(l-2)]
        if(column == 'advice' or column == 'time'):
            row = row[1:]
            l = len(row)
            row = row[:(l-1)]
        info.append(row)
    return info

def get_note_time(): # получение заметок пользователя (для функции отправки уведомления по времени)
    con = sqlite3.connect('./database.db')
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

def get_users_time(): # получение приоритетов пользователя (для функции отправки уведомления по времени)
    con = sqlite3.connect('./database.db')
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
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM users WHERE user_id=' +str(user_id))
    time = cur.fetchall()
    time = str(time[0])
    time = time[2:]
    l = len(time)
    time = time[:(l-3)]
    return time

def get_time_for_note(user_id,note):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM notes WHERE user_id=? AND note=?',(str(user_id),note))
    time = cur.fetchall()
    time = str(time[0])
    time = time[2:]
    l = len(time)
    time = time[:(l-3)]
    return time

def add_advice(advice):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO advices VALUES("'+advice+'")')
    con.commit()
    cur.close()
    con.close()

def number_of_advices(): # кол-во советов
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM advices')
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    return int(count)
