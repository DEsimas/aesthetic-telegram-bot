from telebot import types

from DataAccessFunctions import getCourierByOffice, getUserByTelegramChatId

def validate(bot, m):
    def check_function(message):
        @bot.callback_query_handler(func=lambda m: True)
        def money(callback):
            bot.edit_message_reply_markup(callback.message.chat.id, message_id = callback.message.id, reply_markup = None)
            if callback.data == 'yes':
                bot.send_message(message.chat.id, 'Заказ начали собирать')
            if callback.data == 'no':
                item1 = types.InlineKeyboardButton(text='Отправить фото еще раз', callback_data='remove')
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(item1)
                bot.send_message(message.chat.id, 'Вы не оплатили заказ', reply_markup=keyboard)
            if callback.data == 'remove':
                check_function(message)

        def get_photo(message):
            photo = max(message.photo, key=lambda x: x.height)
            file_id = photo.file_id
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton(text='Деньги есть', callback_data='yes')
            item2 = types.InlineKeyboardButton(text='Денег нет', callback_data='no')
            keyboard.add(item1, item2)
            bot.send_photo(chat_id = getCourierByOffice(getUserByTelegramChatId(message.chat.id)['office'])['telegramChatId'],reply_markup=keyboard, photo = file_id)
        
        bot.send_message(message.chat.id, 'Отправь фото с подтверждением оплаты')
        bot.register_next_step_handler(message, get_photo)

    check_function(m)