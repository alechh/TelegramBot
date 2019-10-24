from telebot import types

def category_key():
    markup = types.ReplyKeyboardMarkup(row_width=2)  # клавиатура
    c1 = types.KeyboardButton('Студент')
    c2 = types.KeyboardButton('Школьник')
    c3 = types.KeyboardButton('Работающий')
    c4 = types.KeyboardButton('Бездельник')
    markup.add(c1, c2, c3, c4)
    return markup
def delete_keyboard():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup
def priority_key():
    markup = types.ReplyKeyboardMarkup(row_width=2)  # клавиатура
    c1 = types.KeyboardButton('Экзамены')
    c2 = types.KeyboardButton('Изучение языков')
    c3 = types.KeyboardButton('Путешествие')
    c4 = types.KeyboardButton('Спорт')
    c5 = types.KeyboardButton('Завершить')
    markup.add(c1, c2, c3, c4,c5)
    return markup
def time_key():
    markup= types.ReplyKeyboardMarkup(row_width=2)  # клавиатура
    c1 = types.KeyboardButton('12:00')
    c2 = types.KeyboardButton('15:00')
    c3 = types.KeyboardButton('18:00')
    c4 = types.KeyboardButton('20:00')
    markup.add(c1, c2, c3, c4)
    return markup
