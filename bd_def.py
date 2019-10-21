    #библиотека для работы с базой данных
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

def create_perfonal_bd(user_id,username,priority):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    # создание таблицы, если она еще не создана
    cur.execute(
        'CREATE TABLE IF NOT EXISTS prior'+ str(user_id) +'(user_id INT, username TEXT, priority TEXT, time TEXT)')
    # добавление пользователя в таблицу
    cur.execute('INSERT INTO prior'+ str(user_id) +' VALUES(' + str(user_id) + ',"' + str(username) + '","'+priority+'","None")')
    # сохранение изменений в базе данных
    con.commit()
    # отключение от базы данных
    cur.close()
    con.close()
def set_time(user_id,time):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('UPDATE prior'+ str(user_id)+' SET time = "'+str(time) +'" WHERE user_id ='+str(user_id) +' and time="None"')
    con.commit()
    cur.close()
    con.close()