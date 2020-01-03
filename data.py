def get_token():
    return 'secret'

def get_test_token():
    return 'secret'

def get_greeting():
    return "Приветствую тебя. Я бот, который будет напоминать тебе о твоих делах, мотивировать и давать полезные советы, чтобы ты справлялся со всеми задачами\nЧто я умею:\n1) Напоминать о ежедневных делах, просто напиши что и когда напомнить\n2) Давать мотивационные советы и отправлять цитаты великих мыслителей\n3) Сохранять заметки"

def get_help():
    return "Команды:\n/notes - заметки\n/daily - ежедневные напоминания\n/advice - получить совет\n/set_daily - установить ежедневное напоминание\n/set_time - выбрать время для советов\n/del_notes - удалить заметки\n/del_daily - удалить ежедневные напоминания\nЧтобы добавить заметку, пришлите её обычным сообщением"

def get_my_id():
    return 260009462

def is_me(chat_id):
    if int(chat_id) == get_my_id():
        return True
    return False

def is_admins(user_id):
    if int(user_id) == get_my_id() or int(user_id) == 944242100:
        return True
    return False

