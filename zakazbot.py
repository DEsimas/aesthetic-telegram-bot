import json
import os
from telebot import types
import telebot
from dotenv import load_dotenv
from Order import Order

load_dotenv()

token = '5705423313:AAGooiTBMzzCv9hPmNATbqzPf1NBiUiuVTQ'

bot = telebot.TeleBot(token)




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("Сделать Заказ")
    button2 = types.KeyboardButton("Предыдущий заказ")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Здравствуйте, Спасибо что пользуетесь хуйботом. Вы желаете сделать заказ, или просмотреть предыдущий заказ?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text is not None and '/' not in message.text)
def reply(message):
    if message.text == "Сделать Заказ":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        button1 = types.KeyboardButton("Ресторан 1")
        markup.add(button1)
        bot.send_message(message.chat.id, "Выберите ресторан", reply_markup=markup)



file = open('data.json', 'r')
data = json.load(file)

state = {}
orders = {}
endpoints = ['Finish', 'Back', 'Discard']




def getKeyboard(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)

    for line in data:
        item = types.InlineKeyboardButton(line)
        keyboard.add(item)

    item = types.InlineKeyboardButton('Finish')
    keyboard.add(item)

    item = types.InlineKeyboardButton('Back')
    keyboard.add(item)

    item = types.InlineKeyboardButton('Discard')
    keyboard.add(item)

    return keyboard


def getRestaurantByName(name):
    for r in data:
        if (r['name'] == name):
            return r


def getCategoryByName(rest, name):
    categories = getRestaurantByName(rest)['menu']['categories']
    for c in categories:
        if c['name'] == name:
            return c


def getDishByName(rest, category, name):
    dishes = getCategoryByName(rest, category)['dishes']
    for d in dishes:
        if d['name'] == name:
            return d


def handleCommand(message):
    if (message.text == 'Finish'):
        cmd_finish(message)
    if (message.text == 'Back'):
        cmd_back(message)
    if message.text == 'Discard':
        cmd_discard(message)


def cmd_finish(message):
    if (len(orders[message.chat.id]) == 0):
        return cmd_discard(message)
    for o in orders[message.chat.id]:
        o.print()
    bot.send_message(message.chat.id, 'Готово')


def cmd_back(message):
    order = state[message.chat.id]
    if order.dish != None:
        order.dish = None
        dish(message)
        return
    if order.category != None:
        order.category = None
        category(message)
        return
    if order.restaurant != None:
        bot.send_message(
            message.chat.id,
            'Нельзя заказывать из двух ресторанов сразу, создайте два заказа')
        category(message)
        return
    if order.restaurant == None:
        cmd_discard(message)
        return


def cmd_discard(message):
    bot.send_message(message.chat.id, 'Заказ отменён')
    return


def handleExtraCommand(message, next):
    try:
        endpoints.index(message.text)
    except:
        next(message)
    else:
        handleCommand(message)


@bot.message_handler(commands=['test'])
def menu(message):
    session = Order(message.chat.id)
    state[message.chat.id] = session
    orders[message.chat.id] = []
    restaurant(message)


def restaurant(message):
    elements = []
    for r in data:
        elements.append(r['name'])

    bot.send_message(message.chat.id,
                     'Выберите ресторан:',
                     reply_markup=getKeyboard(elements))
    bot.register_next_step_handler(message, handleExtraCommand, saveRestaurant)


def saveRestaurant(message):
    try:
        endpoints.index(message.text)
    except:
        if getRestaurantByName(message.text) == None:
            bot.send_message(message.chat.id, "Ресторан введён неверно")
            restaurant(message)
        else:
            state[message.chat.id].restaurant = message.text
            category(message)
    else:
        handleCommand(message)


def category(message):
    elements = []
    for c in getRestaurantByName(
            state[message.chat.id].restaurant)['menu']['categories']:
        elements.append(c['name'])

    bot.send_message(message.chat.id,
                     'Выберите категорию:',
                     reply_markup=getKeyboard(elements))

    bot.register_next_step_handler(message, handleExtraCommand, saveCategory)


def saveCategory(message):
    if getCategoryByName(state[message.chat.id].restaurant,
                         message.text) == None:
        bot.send_message(message.chat.id, "Категория введёна неверно")
        category(message)
    else:
        state[message.chat.id].category = message.text
        dish(message)


def dish(message):
    elements = []
    for c in getCategoryByName(state[message.chat.id].restaurant,
                               state[message.chat.id].category)['dishes']:
        elements.append(c['name'] + '..........' + str(c['price']))

    bot.send_message(message.chat.id,
                     'Выберите блюдо:',
                     reply_markup=getKeyboard(elements))

    bot.register_next_step_handler(message, handleExtraCommand, saveDish)


def saveDish(message):
    text = message.text.split('..........')[0]
    if getDishByName(state[message.chat.id].restaurant,
                     state[message.chat.id].category, text) == None:
        bot.send_message(message.chat.id, "Блюдо введёно неверно")
        dish(message)
    else:
        state[message.chat.id].dish = text
        volume(message)


def volume(message):
    dish = getDishByName(state[message.chat.id].restaurant,
                         state[message.chat.id].category,
                         state[message.chat.id].dish)
    try:
        dish['volumes']
    except:
        saveToOrder(message)
        return

    elements = []
    for v in dish['volumes']:
        elements.append(v['volume'] + '..........' + str(v['price']))

    bot.send_message(message.chat.id,
                     'Выберите опцию:',
                     reply_markup=getKeyboard(elements))

    bot.register_next_step_handler(message, handleExtraCommand, saveVolume)


def saveVolume(message):
    text = message.text.split('..........')[0]
    volumes = getDishByName(state[message.chat.id].restaurant,
                            state[message.chat.id].category,
                            state[message.chat.id].dish)['volumes']

    contains = False
    for v in volumes:
        if v['volume'] == text:
            contains = True
            break

    if (not contains):
        bot.send_message(message.chat.id, "Опция введёна неверно")
        volume(message)
    else:
        state[message.chat.id].volume = text
        saveToOrder(message)


def saveToOrder(message):
    order = Order(chatId=message.chat.id)
    order.restaurant = state[message.chat.id].restaurant
    order.category = state[message.chat.id].category
    order.dish = state[message.chat.id].dish
    order.volume = state[message.chat.id].volume
    orders[message.chat.id].append(order)

    state[message.chat.id].category = None
    state[message.chat.id].dish = None
    state[message.chat.id].volume = None

    category(message)

@bot.message_handler(content_types=['text'])
def start(message):
    if save == '':
        bot.send_message(message.chat.id, 'Напиши /reg')
    else:
        bot.send_message(message.chat.id, 'Напиши /start')

bot.infinity_polling()




