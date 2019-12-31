from telebot import types

def delete_keyboard():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup
def priority_key():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    c1 = types.KeyboardButton('Экзамены')
    c2 = types.KeyboardButton('Изучение языков')
    c3 = types.KeyboardButton('Путешествие')
    c4 = types.KeyboardButton('Спорт')
    c5 = types.KeyboardButton('Завершить')
    markup.add(c1, c2, c3, c4,c5)
    return markup

def time_key():
    markup= types.ReplyKeyboardMarkup(row_width=2)
    c1 = types.KeyboardButton('12:00')
    c2 = types.KeyboardButton('15:00')
    c3 = types.KeyboardButton('18:00')
    c4 = types.KeyboardButton('20:00')
    markup.add(c1, c2, c3, c4)
    return markup

def complete_key():
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    c1 = types.KeyboardButton('Завершить')
    markup.add(c1)
    return markup

def as_note_key():
    markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
    c1 = types.KeyboardButton('Сохранить как заметку')
    markup.add(c1)
    return markup

def inline_note(number):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    if(number ==1):
        buttons.append(types.InlineKeyboardButton(text=str(1),callback_data=str(1)))
    for i in range(int(number)-1):
        buttons.append(types.InlineKeyboardButton(text=str(i+1),callback_data=str(i+1)))
    keyboard.row(*buttons)
    return keyboard

def inline_daily(number):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    if(number ==1):
        keyboard.row(types.InlineKeyboardButton(text=str(1),callback_data="d_1"))
        return keyboard
    for i in range(int(number)):
        buttons.append(types.InlineKeyboardButton(text=str(i+1),callback_data="d_"+str(i+1)))
    keyboard.row(*buttons)
    return keyboard