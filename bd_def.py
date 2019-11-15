import sqlite3


    #добавление пользователя в базу данных
def add_user(user_id,username,firstname,secondname,name,category):
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

def set_category(user_id,category):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE OR IGNORE users SET category = "'+str(category) +'" WHERE user_id ='+str(user_id))
    con.commit()
    cur.close()
    con.close()

def create_perfonal_bd(number,user_id,username,priority):
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
def set_time(user_id,time):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE prior SET time = "'+str(time) +'" WHERE user_id ='+str(user_id) +' and time="None"')
    con.commit()
    cur.close()
    con.close()

def add_note(number,user_id,username,note):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS notes' + str(user_id) + '(number INT,user_id INT, username TEXT, note TEXT, time TEXT)')
    cur.execute('INSERT INTO notes' + str(user_id) + ' VALUES(' + str(number) +',' + str(user_id) + ',"' + str(username) + '","' + note + '","None")')
    con.commit()
    cur.close()
    con.close()

def print_notes(user_id):
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

def get_prior():
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

def delete_note(message):
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

def print_priority(user_id):
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

def delete_priority(message):
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