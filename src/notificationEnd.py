from DataAccessFunctions import getUsersByOffice

def notificationEnd(bot, office):
    users = getUsersByOffice(office)
    for u in users:
        bot.send_message(u['telegramChatId'], 'Сбор заказов окончен')