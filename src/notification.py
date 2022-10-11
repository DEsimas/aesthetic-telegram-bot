from telebot import types
from DataAccessFunctions import getUsersByOffice
from order import order


def notification(bot, office):
    @bot.callback_query_handler(func=lambda m: True)
    def join(call):
        order(bot, call.message)

    users = getUsersByOffice(office)
    for u in users:
        markup = types.InlineKeyboardMarkup()
        button= types.InlineKeyboardButton(text='Присоединиться', callback_data='Join')
        markup.add(button)
        bot.send_message(u['telegramChatId'], 'Начат сбор заказов в офисе: ' + office, reply_markup=markup)