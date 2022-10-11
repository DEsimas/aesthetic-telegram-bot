from telebot import types
from DataAccessFunctions import getUsersByOffice
from order import order
from validate import validate


def notification(bot, office, time):
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        bot.edit_message_reply_markup(call.message.chat.id, message_id = call.message.id, reply_markup = None)
        if call.data == 'Join':
            order(bot, call.message)
        if call.data.split(' ')[0] == 'yes':
            bot.send_message(int(call.data.split(' ')[1]), 'Заказ начали собирать')
        if call.data.split(' ')[0] == 'no':
            item1 = types.InlineKeyboardButton(text='Отправить фото еще раз', callback_data='remove ' + call.data.split(' ')[2])
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(item1)
            bot.send_message(int(call.data.split(' ')[1]), 'Вы не оплатили заказ', reply_markup=keyboard)
        if call.data.split(' ')[0] == 'remove':
            validate(bot, call.message, int(call.data.split(' ')[1]))

    users = getUsersByOffice(office)
    for u in users:
        markup = types.InlineKeyboardMarkup()
        button= types.InlineKeyboardButton(text='Присоединиться', callback_data='Join')
        markup.add(button)
        bot.send_message(u['telegramChatId'], 'Начат сбор заказов в офисе: ' + office + '. Сбор закончится через ' + str(time) + ' минут.', reply_markup=markup)