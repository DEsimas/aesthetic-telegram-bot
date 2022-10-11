from telebot import types

from DataAccessFunctions import getCategories, getDishes, getPaymentByOffice, getRestaurants, getUserByTelegramChatId

class Order:
    def __init__(self) -> None:
        self.restaurant = ''
        self.category = ''
        self.name = ''
        self.price = -1

def order(bot, m):
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

    def get_price():
        sum = 0
        for el in orderArr:
            sum += el['price']
        return sum

    def cmd_finish(message):
        if len(orderArr) == 0:
            cmd_discard(message)
        else:
            bot.send_message(message.chat.id, 'Вам нужно перевести ' + str(get_price()) + ' рублей. ' + getPaymentByOffice(getUserByTelegramChatId(message.chat.id)['office']))
            print(orderArr)

    def cmd_back(message):
        if current.restaurant == '':
            cmd_discard()
        get_category(message)

    def cmd_discard(message):
        bot.send_message(message.chat.id, 'Заказ отменён')
        return

    def get_restaurant(message):
        keyboard = types.ReplyKeyboardMarkup(row_width = 3)
        for i in getRestaurants():
            key = types.InlineKeyboardButton(i)
            keyboard.add(key)
        bot.send_message(message.chat.id, "Из какого Ресторана вы хотите сделать заказ?", reply_markup=keyboard)
        bot.register_next_step_handler(message, handleCommands, save_restaurant)

    def save_restaurant(message):
        try:
            getRestaurants().index(message.text)
        except:
            bot.send_message(message.chat.id, 'Ресторан введён неверно')
            get_restaurant(message)
        else:
            current.restaurant = message.text
            get_category(message)

    def get_category(message):
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=getKeyboard(getCategories(current.restaurant)))
        bot.register_next_step_handler(message, handleCommands, save_category)

    def save_category(message):
        try:
            getCategories(current.restaurant).index(message.text)
        except:
            bot.send_message(message.chat.id, 'Категория введёна неверно')
            get_category(message)
        else:
            current.category = message.text
            get_dish(message)

    def get_dish(message):
        bot.send_message(message.chat.id, 'Выберите блюдо:', reply_markup=getKeyboard(getDishes(current.restaurant, current.category)))
        bot.register_next_step_handler(message, handleCommands, save_dish)

    def save_dish(message):
        try:
            getDishes(current.restaurant, current.category).index(message.text)
        except:
            bot.send_message(message.chat.id, 'Блюдо введёно неверно')
            get_dish(message)
        else:
            current.dish = message.text.split('..........')[0]
            current.price = int(message.text.split('..........')[1])
            save(message)

    def save(message):
        orderArr.append({
            'category': current.category,
            'dish': current.dish,
            'price': current.price
        })
        bot.send_message(message.chat.id, 'Блюдо добавлено')
        get_category(message)

    orderArr = []
    commands = {
        'finish': 'Завершить заказ',
        'back': 'Назад',
        'discard': 'Отменить заказ'
    }
    current = Order()
    get_restaurant(m)
