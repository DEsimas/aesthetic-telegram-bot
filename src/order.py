from telebot import types

from DataAccessFunctions import getCategories, getDishes, getRestaurants, getUserByTelegramChatId

def order(b, m):
    global orderArr
    orderArr = []
    global commands
    commands = {
        'finish': 'Завершить заказ',
        'back': 'Назад',
        'discard': 'Отменить заказ'
    }  
    global bot
    bot = b
    get_restaurant(m)

def getKeyboard(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for line in data:
        item = types.InlineKeyboardButton(line)
        keyboard.add(item)
    item = types.InlineKeyboardButton(commands['finish'])
    keyboard.add(item)
    item = types.InlineKeyboardButton(commands['back'])
    keyboard.add(item)
    item = types.InlineKeyboardButton(commands['discard'])
    keyboard.add(item)
    return keyboard

def handleCommands(message, next):
    if (message.text == commands['finish']):
        return cmd_finish(message)
    if (message.text == commands['back']):
        return cmd_back(message)
    if message.text == commands['discard']:
        return cmd_discard(message)
    next(message)

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
    bot.register_next_step_handler(message, handleCommands, save_restaurant)

def save_restaurant(message):
    try:
        getRestaurants().index(message.text)
    except:
        bot.send_message(message.chat.id, 'Ресторан введён неверно')
        get_restaurant(message)
    else:
        global restaurant
        restaurant = message.text
        get_category(message)

def get_category(message):
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=getKeyboard(getCategories(restaurant)))
    bot.register_next_step_handler(message, handleCommands, save_category)

def save_category(message):
    try:
        getCategories(restaurant).index(message.text)
    except:
        bot.send_message(message.chat.id, 'Категория введёна неверно')
        get_restaurant(message)
    else:
        global category
        category = message.text
        get_dish(message)

def get_dish(message):
    bot.send_message(message.chat.id, 'Выберите блюдо:', reply_markup=getKeyboard(getDishes(restaurant, category)))
    bot.register_next_step_handler(message, handleCommands, save_dish)

def save_dish(message):
    try:
        getDishes(restaurant, category).index(message.text)
    except:
        bot.send_message(message.chat.id, 'Блюдо введёно неверно')
        get_dish(message)
    else:
        global dish
        dish = message.text.split('..........')[0]
        save(message)

def save(message):
    orderArr.append({
        'restaurant': restaurant,
        'category': category,
        'dish': dish
    })
    bot.send_message(message.chat.id, 'Блюдо добавлено')
    get_category(message)
