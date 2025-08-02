import telebot
import sqlli
import getter
import config

bot = telebot.TeleBot(config.token)


def sendListBuy(L, message):
    ID = message.chat.id
    S = 'Сегодня понадобиться купит:\n'
    for key, value in L.items():
        S += f'{key}: {value}\n'
    bot.send_message(ID, S)
    


def listBuy(message):
    Log = getter.getLog()
    rec = getter.getRec()
    todayL = {}
    needed = list(config.needed)[0]
    rot = Log['config']["order_rotation"]
    for i in range(len(needed) * Log['config']['rotation']):
        foods = Log['config']['order'][needed[i % len(needed)]]
        food = foods[rot[needed[i % len(needed)]] % len(foods)]
        for key in rec[food]['ingrs'].keys():
            if todayL.get(key):
                todayL[key] += rec[food]['ingrs'][key] * Log['config']['people']
            else:
                todayL[key] = rec[food]['ingrs'][key] * Log['config']['people']
        if rec[food]['need_every_day']:
            dopFood = rec[needed[i % len(needed)]]
            for key in dopFood['ingrs'].keys():
                if todayL.get(key):
                    todayL[key] += dopFood['ingrs'][key] * Log['config']['people']
                else:
                    todayL[key] = dopFood['ingrs'][key] * Log['config']['people']
        rot[needed[i % len(needed)]] += 1
    Log["config"]['order_rotation']
    getter.setLog(Log)
    print(todayL)
    sendListBuy(todayL, message)


def listCurr(message):
    ...

def changePeople(message):
    Log = getter.getLog()
    if int(message.text):
        Log['config']['people'] = int(message.text)
    getter.setLog(Log)


def countPeople(message):
    Log = getter.getLog()
    msg = bot.send_message(message.chat.id, f'Сейчас записано столько человек: {Log['config']['people']}.\n Напиши цифрами сколько теперь человек в лесу.')
    bot.register_next_step_handler(msg, changePeople)


def ruleRec(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for elem in config.types:
        call = 'chooseTypeRuleRec!' + elem
        btn = telebot.types.InlineKeyboardButton(elem, callback_data=call)
        markup.add(btn)
    btn = telebot.types.InlineKeyboardButton('Отмена', callback_data='cancel')
    markup.add(btn)
    bot.send_message(message.chat.id, 'Выбери категорию рецептов.', reply_markup=markup)


def ruleRot(message):
    ...