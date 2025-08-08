import telebot
import handler
import getter
import time
import config

bot = telebot.TeleBot(config.token)


def findRecByType(Type):
    rec = getter.getRec()
    L = []
    for key in rec.keys():
        if rec[key]['type'] == Type:
            L.append(key)
    return L


def is_int(S):
    for i in range(len(S)):
        if S[i] < '0' or S[i] > '9':
            return False
    return True


def sendListBuy(L, message):
    ID = message.chat.id
    S = 'Сегодня понадобиться купит:\n'
    for key, value in L.items():
        S += f'{key}: {value}\n'
    bot.send_message(ID, S)
    




def listBuy(message):
    print(123)
    todayL = {}
    sch = getter.getSch()
    cur = time.localtime()
    today = (cur.tm_year, cur.tm_mon, cur.tm_mday, 0, 0, 0, cur.tm_wday, cur.tm_yday, cur.tm_isdst)
    today = time.mktime(today)
    Log = getter.getLog()
    sortedL = sorted(sch.keys(), key=int)
    rec = getter.getRec()
    i = 0
    print(sortedL)
    while i < len(sortedL) and today >= int(sortedL[i]):
        print(i)
        i += 1
    sortedL = sortedL[i-1:]
    print(sortedL)
    i = 0
    while  i < len(sortedL) and i <= Log['config']['rotation']:
        print(sch[sortedL[i]])
        for key in sch[sortedL[i]].keys():
            food = sch[sortedL[i]][key]
            foodRec = rec[food]
            for elem in foodRec['ingrs'].keys():
                if elem not in todayL:
                    todayL[elem] = foodRec['ingrs'][elem] * Log['config']['people']
                else: 
                    todayL[elem] += foodRec['ingrs'][elem] * Log['config']['people']
            for elem in foodRec['need']:
                for Elem in rec[elem]['ingrs']:
                    if Elem not in todayL:
                        todayL[Elem] = rec[elem]['ingrs'][Elem] * Log['config']['people']
                    else: 
                        todayL[Elem] += rec[elem]['ingrs'][Elem] * Log['config']['people']
        i += 1
    print(321)
    sendListBuy(todayL, message)


def listCurr(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(
        text="Показать, что есть",
        callback_data='show_curr'
    )
    markup.add(btn)
    btn = telebot.types.InlineKeyboardButton(
        text='Обновить список',
        callback_data='curr_update'
    )
    markup.add(btn)
    btn = telebot.types.InlineKeyboardButton(
        text='Редактировать список',
        callback_data='curr_red'
    )
    markup.add(btn)
    bot.send_message(message.chat.id, text='Что делаем со списком?', reply_markup=markup)


def currClear():
    cur = getter.getCur()
    for key in cur.keys():
        if cur[key]['count'] != 0:
            cur[key]['count'] == 0
    getter.setCur(cur)


def findTypesCurr():
    cur = getter.getCur()
    types = set()
    for key in cur.keys():
        types.add(cur[key]['type'])
    return list(types)


def findCurrByType(Type):
    cur = getter.getCur()
    l = []
    for key in cur.keys():
        if cur[key]['type'] == Type:
            l.append(key)
    return l


def currMakeMainMenu(message):
    types = findTypesCurr()
    markup = telebot.types.InlineKeyboardMarkup()
    for elem in types:
        btn = telebot.types.InlineKeyboardButton(
            text=elem,
            callback_data=f'currMM_{elem}'
        )
        markup.add(btn)
    bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup)


def chooseCurrCategory(call):
    markup = telebot.types.InlineKeyboardMarkup()
    Type = call.data[call.data.index('_') + 1:]
    foods = findCurrByType(Type)
    for elem in foods:
        btn = telebot.types.InlineKeyboardButton(
            text=elem,
            callback_data=f'chCurrProd_{elem}'
        )
        markup.add(btn)
    btn = telebot.types.InlineKeyboardButton(
        text='Отмена',
        callback_data=f'back_chCurrProd'
    )
    markup.add(btn)
    bot.send_message(call.message.chat.id, text='Выбери продукт:', reply_markup=markup)    


def ruleRec(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for elem in config.types:
        call = 'chooseTypeRuleRec!' + elem
        btn = telebot.types.InlineKeyboardButton(elem, callback_data=call)
        markup.add(btn)
    btn = telebot.types.InlineKeyboardButton('Отмена', callback_data='cancel')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Выбери категорию рецептов.', reply_markup=markup)


def makeUltraShortMenu():
    cur = time.localtime()
    today = (cur.tm_year, cur.tm_mon, cur.tm_mday, 0, 0, 0, cur.tm_wday, cur.tm_yday, cur.tm_isdst)
    today = time.mktime(today)
    menu = getter.getSch()
    text = ""
    for key in menu.keys():
        if int(key) >= today:
            S = f'{time.strftime("%d.%m.%Y", time.localtime(today))}'
            text += S
    return text


def makeDayMenu(day):
    menu = getter.getSch()
    text = ''
    for key in menu[day].keys():
        S = f'{key}: {menu[day][key]} \n'
        text += S
    return text


def ruleMenu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton('Изменить имеющиеся меню', callback_data='change_curMenu')
    markup.add(btn)
    btn = telebot.types.InlineKeyboardButton('Добавить в меню', callback_data='add_menu_start')
    markup.add(btn)
    text = "Вот такие даты уже отмечены: \n" + makeUltraShortMenu()
    bot.send_message(message.chat.id, text=text, reply_markup=markup)
