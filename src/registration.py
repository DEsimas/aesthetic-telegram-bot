from telebot import types

from DataAccessFunctions import getUserByTelegramChatId, saveUser, getOffices

def registration(b, m):
    global bot
    bot = b    
    if getUserByTelegramChatId(m.chat.id):
        already_registered(m)
    else:
        get_surname(m)

def already_registered(message):
    bot.send_message(message.chat.id, 'Вы уже зарегестрированны!')

def get_surname(message):
    bot.send_message(message.chat.id, 'Давай начнем нашу регестрацию! \nНапиши свою фамилию')
    bot.register_next_step_handler(message, get_name)
    
def get_name(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, 'Напиши свое имя')
    bot.register_next_step_handler(message, get_bat)
    
def get_bat(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Напиши свое отчество')
    bot.register_next_step_handler(message, get_office)

def get_office(message):
    global bat
    bat = message.text
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
        global office
        office = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        menuYes = types.InlineKeyboardButton(text='Да, все верно')
        menuNo = types.InlineKeyboardButton(text='Нет, изменить')
        keyboard.add(menuYes,menuNo)
        bot.send_message(message.chat.id, 'Значит Вы у нас: ' + surname + ' ' + name + ' ' + bat + ' из офиса: ' + office + '\nВсе верно?', reply_markup=keyboard)
        bot.register_next_step_handler(message, save)

def save(message):
    if message.text == 'Да, все верно':
        saveUser(name, surname, bat, office, message.chat.id)
    else:
        get_surname(message)