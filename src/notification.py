from telebot import types
from DataAccessFunctions import getUsersByOffice
from order import order


def notification(bot, office, restaurant, orderId):
    @bot.callback_query_handler(func=lambda m: True)
    def join(call):
        order(bot, call.message, restaurant, orderId)

    users = getUsersByOffice(office)
    for u in users:
        markup = types.InlineKeyboardMarkup()
        button= types.InlineKeyboardButton(text='Присоединиться', callback_data='Join')
        markup.add(button)
        bot.send_message(u['telegramChatId'], 'Ребята из ' + office + ' заказывают еду из ресторана ' + restaurant, reply_markup=markup)