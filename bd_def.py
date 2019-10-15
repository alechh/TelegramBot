import sqlite3
def add_user(user_id,username,firstname,secondname):
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, firstname TEXT, secondname TEXT, UNIQUE(user_id,username,firstname,secondname))')
    cur.execute('INSERT OR IGNORE INTO users VALUES(' + str(user_id) + ',"' + username + '", "' + firstname + '", "' + secondname + '")')
    con.commit()
    cur.close()
    con.close()