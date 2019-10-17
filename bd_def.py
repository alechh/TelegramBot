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
    cur.execute('UPDATE users SET category = "'+str(category) +'" WHERE user_id ='+str(user_id))
    con.commit()
    cur.close()
    con.close()
