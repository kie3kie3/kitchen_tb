import telebot
import config
import commandForUs
import sqlli
import getter
import time


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, text='Назовись')
    bot.register_next_step_handler(msg, register)


def countPeople(message):
    Log = getter.getLog()
    msg = bot.send_message(message.chat.id, f'Сейчас записано столько человек: {Log['config']['people']}.\n Напиши цифрами сколько теперь человек в лесу.')
    bot.register_next_step_handler(msg, changePeople)


def changePeople(message):
    Log = getter.getLog()
    if commandForUs.is_int(message.text):
        Log['config']['people'] = int(message.text)
    getter.setLog(Log)


def register(message):
    name = message.text
    Log = getter.getLog()
    Log[str(message.chat.id)] = name
    getter.setLog(Log=Log)
    markup = telebot.types.ReplyKeyboardMarkup()
    for elem in config.commands:
        markup.add(elem)
    bot.send_message(message.chat.id, 'Привет, добавил тебе кнопочек', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in config.commands)
def commands(message):
    if message.text == 'Составить список покупок':
        commandForUs.listBuy(message)
    elif message.text == 'Обновить список имеющегося':
        commandForUs.listCurr(message)
    elif message.text == 'Изменить число людей':
        countPeople(message)
    elif message.text == 'Управление рецептами':
        commandForUs.ruleRec(message)
    elif message.text == 'Управление меню':
        commandForUs.ruleMenu(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_curMenu'))
def changeCurMenu(call):
    menu = getter.getSch()
    markup = telebot.types.InlineKeyboardMarkup()
    cur = time.localtime()
    today = (cur.tm_year, cur.tm_mon, cur.tm_mday, 0, 0, 0, cur.tm_wday, cur.tm_yday, cur.tm_isdst)
    today = time.mktime(today)
    for key in menu.keys():
        if int(key) > today:
            text = f'{time.strftime("%d.%m.%Y", time.localtime(today))}'
            btn = telebot.types.InlineKeyboardButton(text=text, callback_data=f'changeMenu_{key}')
            markup.add(btn)


@bot.callback_query_handler(func=lambda call: call.data.startswith('changeMenu_'))
def changeMenu(call):
    date = call.data[call.data.index('_') + 1:]
    today = time.strftime('%d.%m.%Y', time.localtime())
    menu = getter.getSch()
    markup = telebot.types.InlineKeyboardMarkup()
    todayMenu = menu[date]
    for key in todayMenu.keys():
        btn = telebot.types.InlineKeyboardButton(
            text=f'{key}: {todayMenu[key]}',
            callback_data=f'changeM_{date}!{key}'
        )
        markup.add(btn)
    bot.send_message(call.message.chat.id, text=f'Меню на {today}:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('changeM_'))
def changeDayMenu(call):     
    date = call.data[call.data.index('_') + 1:call.data.index('!')]
    food = call.data[call.data.index('!') + 1:]

    

@bot.callback_query_handler(func=lambda call: call.data == 'show_curr')
def showCurrFood(call):
    cur = getter.getCur()
    text = 'Вот список имеющегося:\n'
    for key in cur.keys():
        if cur[key]['count'] != 0:
            text += f'{key}: {cur[key]['count']}\n'
    bot.send_message(
        call.message.chat.id,
        text=text
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('back_'))
def backAll(call):
    thing = call.data[call.data.index('_') + 1:]
    if thing == 'chCurrProd':
        commandForUs.currMakeMainMenu(call.message)
    


@bot.callback_query_handler(func=lambda call: call.data.startswith('currMM_'))
def chooseCategoryFood(call):
    commandForUs.chooseCurrCategory(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith('curr_'))
def curr(call):
    if call.data == 'curr_update':
        commandForUs.currClear()
    commandForUs.currMakeMainMenu(call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chooseTypeRuleRec'))
def chooseTypeRuleRec(call):
    message = call.message
    rec = getter.getRec()
    markup = telebot.types.InlineKeyboardMarkup()
    Type = call.data[call.data.index('!') + 1:]
    for elem in sqlli.selectAll(Type=Type, needAll=True):
        callback = "chooseFoodRuleRec!" + elem
        text = elem
        if not rec[elem]['ings']:
            text += ' Неактивен'
        btn = telebot.types.InlineKeyboardButton(text=text, callback_data=callback)
        markup.add(btn)
    btn = telebot.types.InlineKeyboardButton('Отмена', callback_data='cancel')
    markup.add(btn)
    bot.edit_message_text(
        text=f'Так, ты выбрал {Type}. Теперь выбери непосредственно рецепт.',
        message_id=message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('chooseFoodRuleRec'))
def chooseFoodRuleRec(call):
    food = call.data[call.data.index('!') + 1:]
    rec = getter.getRec()
    for elem in sqlli.selectAll():
        text = elem
        callback = 'chaRecIng!' + food + '$' + elem
        btn = telebot.types.InlineKeyboardButton(
            text=text, callback_data=callback
        )


@bot.callback_query_handler(func=lambda call: call.data == 'add_menu_start')
def addMenuStart(call):
    sch = getter.getSch()
    Log = getter.getLog()
    cur = time.localtime()
    today = (cur.tm_year, cur.tm_mon, cur.tm_mday, 0, 0, 0, cur.tm_wday, cur.tm_yday, cur.tm_isdst)
    today = time.mktime(today)
    L = sorted(sch.keys(), key=int)
    a = 0
    if L != []:
        a = str(int(L[-1]) + 86400)
    today = max(int(today), int(a))
    markup = telebot.types.InlineKeyboardMarkup()
    foods = commandForUs.findRecByType(Log['config']['needed'][0])
    for elem in foods:
        btn = telebot.types.InlineKeyboardButton(
            text=elem,
            callback_data=f'addM_{Log['config']['needed'][0]}!{today}*{elem}'
        )
        markup.add(btn)
    text = f'Выбери блюдо\nКатегория: {Log['config']['needed'][0]} \nДень: {time.strftime('%d.%m.%Y', time.localtime(today))}'
    bot.send_message(
        call.message.chat.id,
        text=text,
        reply_markup=markup
    )
    sch[today] = {}
    getter.setSch(sch)


@bot.callback_query_handler(func=lambda call: call.data.startswith('addM_'))
def addMenuNext(call):
    data = call.data
    print(data)
    Case = data[data.index('_') + 1:data.index('!')]
    day = data[data.index('!') + 1:data.index('*')]
    food = data[data.index('*') + 1:]
    sch = getter.getSch()
    Log = getter.getLog()
    markup = telebot.types.InlineKeyboardMarkup()
    print(food, day, Case)
    sch[day][Case] = food
    getter.setSch(sch)
    if Log['config']['needed'][-1] != Case:
        newCase = Log['config']['needed'][Log['config']['needed'].index(Case) + 1]
        for elem in commandForUs.findRecByType(newCase):
            btn = telebot.types.InlineKeyboardButton(
                text=elem,
                callback_data=f'addM_{newCase}!{day}*{elem}'
            )
            print(f'addM_{newCase}!{day}-{elem}', len(f'addM_{newCase}!{day}*{elem}'.encode("utf-8")))
            markup.add(btn)
        text = f'Выбери блюдо\nКатегория: {newCase}\nДень: {time.strftime('%d.%m.%Y', time.localtime(int(day)))}'
        bot.send_message(
            call.message.chat.id,
            text=text,
            reply_markup=markup
        )
    else:
        bot.send_message(
            call.message.chat.id,
            text='День заполнен'
        )


def main():
    print('a')
    bot.infinity_polling()