[1mdiff --git a/__pycache__/keyboards.cpython-36.pyc b/__pycache__/keyboards.cpython-36.pyc[m
[1mindex 095c5bb..124a6cd 100644[m
Binary files a/__pycache__/keyboards.cpython-36.pyc and b/__pycache__/keyboards.cpython-36.pyc differ
[1mdiff --git a/database.db b/database.db[m
[1mindex cb26631..39ee10e 100644[m
Binary files a/database.db and b/database.db differ
[1mdiff --git a/keyboards.py b/keyboards.py[m
[1mindex 2bbe7b4..c6ad22a 100644[m
[1m--- a/keyboards.py[m
[1m+++ b/keyboards.py[m
[36m@@ -5,7 +5,7 @@[m [mdef category_key():[m
     c1 = types.KeyboardButton('Студент')[m
     c2 = types.KeyboardButton('Школьник')[m
     c3 = types.KeyboardButton('Работающий')[m
[31m-    c4 = types.KeyboardButton('Безделник')[m
[32m+[m[32m    c4 = types.KeyboardButton('Бездельник')[m
     markup.add(c1, c2, c3, c4)[m
     return markup[m
 def delete_keyboard():[m
[36m@@ -27,4 +27,4 @@[m [mdef time_key():[m
     c3 = types.KeyboardButton('18:00')[m
     c4 = types.KeyboardButton('20:00')[m
     markup.add(c1, c2, c3, c4)[m
[31m-    return markup[m
\ No newline at end of file[m
[32m+[m[32m    return markup[m
[1mdiff --git a/main.py b/main.py[m
[1mold mode 100644[m
[1mnew mode 100755[m
[1mindex 0ccb857..ec16a53[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -5,7 +5,7 @@[m [mimport keyboards[m
 import data[m
 import bd_def  # файл, в котором будут собраны функции для работы с базой данных[m
 [m
[31m-#apihelper.proxy = {'https': data.get_proxy()}  # proxy[m
[32m+[m[32mapihelper.proxy = {'https': data.get_proxy()}  # proxy[m
 bot = telebot.TeleBot(data.get_token())  # инициализация бота[m
 [m
 def report(message, event): # отчет в pycharm об инициализации пользователя[m
