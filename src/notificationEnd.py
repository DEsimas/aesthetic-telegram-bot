from DataAccessFunctions import clearOrders, getCourierByOffice, getOrders, getUsersByOffice, stopOrders

def notificationEnd(bot, office):
    users = getUsersByOffice(office)
    for u in users:
        bot.send_message(u['telegramChatId'], 'Сбор заказов окончен')
    bot.send_message(getCourierByOffice(office)['telegramChatId'], getOrders(office))
    stopOrders(office)
    clearOrders(office)