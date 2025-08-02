import telebot
import config
import commandForUs
import sqlli
import getter


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
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
        commandForUs.countPeople(message)
    elif message.text == 'Управление рецептами':
        commandForUs.ruleRec(message)
    elif message.text == 'Управление ротацией':
        commandForUs.ruleRot(message)


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


def main():
    print('a')
    bot.infinity_polling()