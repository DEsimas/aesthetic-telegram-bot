import os
import telebot
from dotenv import load_dotenv
from DataAccessFunctions import getCategories, getDishes
from notification import notification

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
    
    notification(bot, 'Октябрьское Поле', 1)
    bot.infinity_polling()

if __name__ == '__main__':
    main()