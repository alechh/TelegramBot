import sqlite3

def add_user(user_id,username,firstname,secondname,name,category): # добавление пользователя в базу данных
        #подключение к базе данных
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
        #создание таблицы, если она еще не создана
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, firstname TEXT, secondname TEXT, name TEXT,category TEXT, UNIQUE(user_id,username,firstname,secondname,name,category))')
        #добавление пользователя в таблицу
    cur.execute('INSERT OR IGNORE INTO users VALUES(' + str(user_id) + ',"' + username + '", "' + firstname + '", "' + secondname + '", "'+ name +'", "'+str(category)+'")')
        #сохранение изменений в базе данных
    con.commit()
        #отключение от базы данных
    cur.close()
    con.close()

def set_category(user_id,category):  # добавление категории пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE users SET category = "'+str(category) +'" WHERE user_id ='+str(user_id))
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
    cur.execute(
        'CREATE TABLE IF NOT EXISTS notes' + str(user_id) + '(number INT,user_id INT, username TEXT, note TEXT, time TEXT)')
    cur.execute('INSERT INTO notes' + str(user_id) + ' VALUES(' + str(number) +',' + str(user_id) + ',"' + str(username) + '","' + note + '","None")')
    con.commit()
    cur.close()
    con.close()

def get_notes(user_id): # получение заметок пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT note FROM notes' + str(user_id))
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

def number_of_notes(message): # кол-во заметок пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes' + str(message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    return int(count)

def delete_note(message): # удаление заметки пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM notes' + str(message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    count = int(count)
    cur.execute('DELETE FROM notes' +str(message.chat.id) + ' WHERE number=' + message.text)
    i = int(message.text)+1
    while i<=count:
        cur.execute(
            'UPDATE notes' +str(message.chat.id) + ' SET number = ' + str(i-1) + ' WHERE number = ' + str(i))
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

def number_of_priority(message): # кол-во приоритетов пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id='+ str(message.chat.id) )
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    return int(count)

def delete_priority(message): # удаление приоритетов
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM prior WHERE user_id=' + str(message.chat.id))
    count = str(cur.fetchall())
    count = count[2:]
    l = len(count)
    count = count[:(l - 3)]
    count = int(count)
    cur.execute('DELETE FROM prior WHERE user_id='+str(message.chat.id)+' and number=' + message.text)
    i = int(message.text)+1
    while i<=count:
        cur.execute(
            'UPDATE prior SET number = ' + str(i-1) + ' WHERE number = ' + str(i) +' and user_id='+ str(message.chat.id))
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

def update_user(user_id, username, firstname, secondname, name, category): # обновить информацию о пользователе в таблице users
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE users SET username = "'+str(username) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET firstname = "'+str(firstname) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET secondname = "'+str(secondname) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET name = "'+str(name) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET name = "'+str(name) +'" WHERE user_id ='+str(user_id))
    cur.execute('UPDATE users SET category = "'+str(category) +'" WHERE user_id ='+str(user_id))
    con.commit()
    cur.close()
    con.close()

def get_category(user_id): # получение категории пользователя
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('SELECT category FROM users WHERE user_id='+ str(user_id))
    info = cur.fetchall()
    info = str(info[0])
    info = info[2:]
    l = len(info)
    info = info[:(l - 3)]
    return info
