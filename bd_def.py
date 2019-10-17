    #библиотека для работы с базой данных
import sqlite3

    #добавление пользователя в базу данных
def add_user(user_id,username,firstname,secondname):
        #подключение к базе данных
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
        #создание таблицы, если она еще не создана
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, firstname TEXT, secondname TEXT, UNIQUE(user_id,username,firstname,secondname))')
        #добавление пользователя в таблицу
    cur.execute('INSERT OR IGNORE INTO users VALUES(' + str(user_id) + ',"' + username + '", "' + firstname + '", "' + secondname + '")')
        #сохранение изменений в базе данных
    con.commit()
        #отключение от базы данных
    cur.close()
    con.close()