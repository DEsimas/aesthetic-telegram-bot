from telebot import types

from DataAccessFunctions import getUserByTelegramChatId, saveUser, getOffices
from start import start

class User:
    def __init__(self) -> None:
        self.surname = ''
        self.name = ''
        self.bat = ''
        self.office = ''

def registration(bot, m):
    def already_registered(message):
        bot.send_message(message.chat.id, 'Вы уже зарегестрированны!')

    def get_surname(message):
        bot.send_message(message.chat.id, 'Давай начнем нашу регестрацию! \nНапиши свою фамилию')
        bot.register_next_step_handler(message, get_name)

    def get_name(message):
        user.surname = message.text
        bot.send_message(message.chat.id, 'Напиши свое имя')
        bot.register_next_step_handler(message, get_bat)

    def get_bat(message):
        user.name = message.text
        bot.send_message(message.chat.id, 'Напиши свое отчество')
        bot.register_next_step_handler(message, get_office)

    def get_office(message):
        user.bat = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
        for office in getOffices():
            item = types.InlineKeyboardButton(office)
            keyboard.add(item)    
        bot.send_message(message.chat.id, 'В каком офисе вы работаете?', reply_markup=keyboard)
        bot.register_next_step_handler(message, verificate)

    def verificate(message):
        try:
            getOffices().index(message.text)
        except:
            bot.send_message(message.chat.id, 'Неверный офис')
            get_office(message)
        else:
            user.office = message.text
            keyboard = types.ReplyKeyboardMarkup(row_width=2)
            menuYes = types.InlineKeyboardButton(text='Да, все верно')
            menuNo = types.InlineKeyboardButton(text='Нет, изменить')
            keyboard.add(menuYes,menuNo)
            bot.send_message(message.chat.id, 'Значит Вы у нас: ' + user.surname + ' ' + user.name + ' ' + user.bat + ' из офиса: ' + user.office + '\nВсе верно?', reply_markup=keyboard)
            bot.register_next_step_handler(message, save)

    def save(message):
        if message.text == 'Да, все верно':
            saveUser(user.name, user.surname, user.bat, user.office, message.chat.id)
            bot.send_message(message.chat.id, 'Регистрация завершена, ждите уведомление о сборе заказов')
            start(bot, message)
        else:
            get_surname(message)
    
    user = User()

    if getUserByTelegramChatId(m.chat.id):
        already_registered(m)
    else:
        get_surname(m)