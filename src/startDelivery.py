from telebot import types
import time
from notification import notification
from DataAccessFunctions import getCouriersIds, getUserByTelegramChatId, getUsers
from notificationEnd import notificationEnd

def startDelivery(bot, message):
    def Inittime(message):
        if message.text == "Да, начать":
            bot.send_message(message.chat.id, "Сколько времени будет длиться сборка заказов (в минутах)?")
            bot.register_next_step_handler(message, Inittime2)
        if message.text == "Нет, отменить":
            bot.send_message(message.chat.id, "Отменено")
    
    def Inittime2(message):
        try:
            ti = float(message.text)
        except:
            bot.send_message(message.chat.id, "Вы выбрали некорректное время")
            Inittime(message)
        else:
            bot.send_message(message.chat.id, "Через " + str(ti) + " минут вы можете начать собирать заказы")
            notification(bot, getUserByTelegramChatId(message.chat.id)['office'], ti)
            time.sleep(ti*60)
            notificationEnd(bot, getUserByTelegramChatId(message.chat.id)['office'])

    try:
        getCouriersIds().index(message.chat.id)
    except:
        return
    
    type = types.ReplyKeyboardMarkup(row_width = 2, one_time_keyboard=True)
    a = types.KeyboardButton("Да, начать")
    b = types.KeyboardButton("Нет, отменить")
    type.add(a, b)
    bot.send_message(message.chat.id, "Вы желаете начать сборку заказов", reply_markup=type)
    bot.register_next_step_handler(message, Inittime)