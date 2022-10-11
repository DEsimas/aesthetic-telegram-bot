from telebot import types
from DataAccessFunctions import getUserByTelegramChatId
from order import order

def start(bot, message):
    if getUserByTelegramChatId(message.chat.id) == None:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы! Используйте /reg')
    else:
        bot.send_message(message.chat.id, 'Подождите пока начнётся сбор заказов')
