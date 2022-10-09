from telebot import types

from DataAccessFunctions import getCategories, getDishes, getRestaurants, getUserByTelegramChatId

def order(b, m):
    global orderArr
    orderArr = []
    global commands
    commands = ['Завершить заказ', 'Назад', 'Отменить заказ']
    global bot
    bot = b
    if getUserByTelegramChatId(m.chat.id) == None:
        bot.send_message(m.chat.id, 'Вы не зарегистрированы! Используйте /reg')
        return
    get_restaurant(m)

def getKeyboard(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for line in data:
        item = types.InlineKeyboardButton(line)
        keyboard.add(item)
    item = types.InlineKeyboardButton(commands[0])
    keyboard.add(item)
    item = types.InlineKeyboardButton(commands[1])
    keyboard.add(item)
    item = types.InlineKeyboardButton(commands[2])
    keyboard.add(item)
    return keyboard

def handleCommands(message, next):
    try:
        commands.index(message.text)
    except:
        next(message)
    else:
        if (message.text == commands[0]):
            cmd_finish(message)
        if (message.text == commands[1]):
            cmd_back(message)
        if message.text == commands[2]:
            cmd_discard(message)

def cmd_finish(message):
    if len(orderArr) == 0:
        cmd_discard(message)
    else:
        print(orderArr)

def cmd_back(message):
    print('back')

def cmd_discard(message):
    bot.send_message(message.chat.id, 'Заказ отменён')
    return

def get_restaurant(message):
    bot.send_message(message.chat.id, 'Выберите ресторан:', reply_markup=getKeyboard(getRestaurants()))
    bot.register_next_step_handler(message, handleCommands, get_category)

def get_category(message):
    try:
        getRestaurants().index(message.text)
    except:
        bot.send_message(message.chat.id, 'Ресторан введён неверно')
        get_restaurant(message)
    else:
        global restaurant
        restaurant = message.text
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=getKeyboard(getCategories(restaurant)))
        bot.register_next_step_handler(message, handleCommands, get_dish)

def get_dish(message):
    try:
        getCategories(restaurant).index(message.text)
    except:
        bot.send_message(message.chat.id, 'Категория введёна неверно')
        get_restaurant(message)
    else:
        global category
        category = message.text
        bot.send_message(message.chat.id, 'Выберите блюдо:', reply_markup=getKeyboard(getDishes(restaurant, category)))
        bot.register_next_step_handler(message, handleCommands, save)

def save(message):
    try:
        getDishes(restaurant, category).index(message.text)
    except:
        bot.send_message(message.chat.id, 'Блюдо введёно неверно')
        get_dish(message)
    else:
        global dish
        dish = message.text.split('..........')[0]
        orderArr.append({
            'restaurant': restaurant,
            'category': category,
            'dish': dish
        })
        get_category(message)
