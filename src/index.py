import os
from validate import validate
import telebot
from dotenv import load_dotenv

from registration import registration
from start import start

def main():
    load_dotenv()
    bot = telebot.TeleBot(os.environ.get('API_KEY'))

    @bot.message_handler(commands=['reg', 'registration'])
    def r(message):
        registration(bot, message)

    @bot.message_handler(commands=['start'])
    def s(message):
        start(bot, message)
    
    @bot.message_handler(commands=['test'])
    def t(message):
        validate(bot, message)

    bot.infinity_polling()

if __name__ == '__main__':
    main()