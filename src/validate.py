from re import M
from telebot import types
from DataAccessFunctions import getCourierByOffice, getUserByTelegramChatId

def validate(bot, m, price):
    def check_function(message):
        def get_photo(message):
            bot.send_message(getCourierByOffice(getUserByTelegramChatId(message.chat.id)['office'])['telegramChatId'], 'Должен быть перевод на ' + str(price) + ' рублей')
            photo = max(message.photo, key=lambda x: x.height)
            file_id = photo.file_id
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton(text='Деньги есть', callback_data='yes ' + str(message.chat.id))
            item2 = types.InlineKeyboardButton(text='Денег нет', callback_data='no ' + str(message.chat.id) + ' ' + str(price))
            keyboard.add(item1, item2)
            bot.send_photo(chat_id = getCourierByOffice(getUserByTelegramChatId(message.chat.id)['office'])['telegramChatId'],reply_markup=keyboard, photo = file_id)
        
        bot.send_message(message.chat.id, 'Отправь фото с подтверждением оплаты')
        bot.register_next_step_handler(message, get_photo)    

    check_function(m)