import datetime
import bd_def

'''Time for note'''
def is_note_time_correct(message):  # проверка на корректность времени для напоминаний
    try:
        time = message.text
        q = False
        if (len(time) == 16):
            cday = time[:2]
            cmonth = time[3:]
            cmonth = cmonth[:2]
            cyear = time[6:]
            cyear = cyear[:4]
            chour = time[11:]
            chour = chour[:2]
            cmin = time[14:]
            q = True

        elif (len(time) == 15):
            cday = time[:2]
            cmonth = time[3:]
            cmonth = cmonth[:2]
            cyear = time[6:]
            cyear = cyear[:4]
            chour = time[11:]
            chour = chour[:1]
            cmin = time[13:]
            q = True

        elif (len(time) == 5):
            chour = time[:2]
            cmin = time[3:]
            if (int(chour) < datetime.datetime.now().hour):
                cday = str(datetime.datetime.now().day + 1)
            elif (int(chour) == datetime.datetime.now().hour and int(cmin) <= datetime.datetime.now().minute):
                cday = str(datetime.datetime.now().day + 1)
            else:
                cday = str(datetime.datetime.now().day)
            if (int(cday) < 10):
                cday = "0" + cday
            cmonth = str(datetime.datetime.now().month)
            cyear = str(datetime.datetime.now().year)
            q = True

        elif (len(time) == 4):
            chour = time[:1]
            cmin = time[2:]
            if (int(chour) < datetime.datetime.now().hour):
                cday = str(datetime.datetime.now().day + 1)
            elif (int(chour) == int(datetime.datetime.now().hour) and int(cmin) <= datetime.datetime.now().minute):
                cday = str(datetime.datetime.now().day + 1)
            else:
                cday = str(datetime.datetime.now().day)
            if (int(cday) < 10):
                cday = "0" + cday
            cmonth = str(datetime.datetime.now().month)
            cyear = str(datetime.datetime.now().year)
            q = True

        if (q and cmin.isdigit() and cmonth.isdigit()):
            if (int(cmin) < 10 and int(cmin) != 0 and len(cmin) == 1):
                cmin = '0' + cmin
            if (int(cmonth) < 10 and int(cmonth) != 0 and len(cmonth) == 1):
                cmonth = '0' + cmonth
        if (q):
            if (cday.isdigit() and cmonth.isdigit() and cyear.isdigit() and chour.isdigit() and cmin.isdigit() and int(
                    cyear) > 2018 and int(cmonth) > 0 and int(cmonth) < 13 and int(cday) > 0 and int(cday) < 32 and int(
                    chour) >= 0 and int(chour) < 24 and int(cmin) >= 0 and int(cmin) < 60):
                set_note_time(message,cday+'.'+cmonth+'.'+cyear+' '+chour+':'+cmin)
                return True
        else:
            return False
        return False
    except:
        return False
def set_note_time(message,curtime):
    if not ':' in curtime:
        if len(curtime)==4:
             h = curtime[:2]
             m = curtime[2:]
        elif len(curtime)==3:
            h = curtime[:1]
            m = curtime[1:]
        curtime = h + ':' + m
    bd_def.set_note_time(message.chat.id,curtime)

'''Time for advice'''
def is_advice_time_correct(message): #проверка на корректность времени для советов
    try:
        time = message.text
        l = len(time)
        if (l == 5):
            hour = time[:2]
            min = time[3:]
        elif (l == 4):
            hour = time[:1]
            min = time[2:]
        elif (l==3):
            hour = time[:1]
            min = time[1:]
        else:
            return False
        if (hour.isdigit() and min.isdigit() and int(hour) < 24 and int(min) < 60):
            bd_def.set_advice_time(message.chat.id, message.text)
            return True
        return False
    except:
        return False

'''Time for Daili notifications'''
def is_daily_time_correct(message): #проверка времени на корректность для приоритетов
    try:
        time = message.text
        l = len(time)
        if (l ==5):
            hour = time[:2]
            min = time[3:]
        elif (l==4):
            hour = time[:1]
            min = time[2:]
        elif (l==3):
            hour = time[:1]
            min = time[1:]
        else:
            return False
        if (hour.isdigit() and min.isdigit() and int(hour) <24 and int(min) <60):
            set_daily_time(message)
            return True
        return False
    except:
        return False
def set_daily_time(message): # установка времени для приоритета
    ctime = message.text
    if not ':' in ctime:
        if len(ctime)==4:
            h = ctime[:2]
            m = ctime[2:]
        elif len(ctime)==3:
            h = ctime[:1]
            m = ctime[1:]
        ctime = h + ':' + m
    bd_def.set_daily_time(message.chat.id,ctime)