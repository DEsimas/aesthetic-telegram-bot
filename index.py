import os
import telebot
from telebot import types
from dotenv import load_dotenv

def main():
    load_dotenv()
    bot = telebot.TeleBot(os.environ.get('API_KEY'))

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
    
    bot.infinity_polling()

if __name__ == '__main__':
    main()