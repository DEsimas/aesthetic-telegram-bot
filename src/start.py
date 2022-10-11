from telebot import types
from DataAccessFunctions import getUserByTelegramChatId
from order import order

def start(b, m):
    global bot
    bot = b

    @bot.message_handler(func=lambda message: message.text is not None and '/' not in message.text)
    def reply(message):
        if message.text == "Сделать Заказ":
            order(bot, message, 'Ресторан 1', 1)

    validate_user(m)

def validate_user(message):
    if getUserByTelegramChatId(message.chat.id) == None:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы! Используйте /reg')
        return
    else:
        start_func(message)

def start_func(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("Сделать Заказ")
    button2 = types.KeyboardButton("Текущий заказ")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Здравствуйте, вы желаете сделать заказ, или просмотреть предыдущий заказ?", reply_markup=markup)