
import logging
import telebot
import sqlite3
import schedule
import time
from multiprocessing import Process

TOKEN = '1297621234:AAHxnGhQhb4vvpbMDl9cSoO82Le0Qu54zKs'
bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

connection = None

@bot.message_handler(content_types=['text', 'video', 'url'])
def handle_text(message):
    connection = sqlite3.connect('chats.sqlite')
    cursor = connection.cursor()

    if message.text == "/hi":
        key = telebot.types.ReplyKeyboardMarkup(True, False)
        key.row('/bye')
        cursor.execute('INSERT INTO Chats(chat_id) values (?)', (message.chat.id,))
        bot.send_message(message.chat.id, 'Hellow, fellow ;)', reply_markup=key)
        connection.commit()

    elif message.text == "/bye":
        cursor.execute('DELETE FROM Chats where chat_id=?', (message.chat.id,))
        connection.commit()


def run_schedule():
    schedule.every().day.at("02:10").do(say_hi)
    while True:
        schedule.run_pending()
        time.sleep(10)


def say_hi():
    connection = sqlite3.connect('chats.sqlite')
    cursor = connection.cursor()

    for row in cursor.execute('SELECT chat_id from Chats').fetchall():
        bot.send_message(row[0], 'Hi there :)')


if __name__ == '__main__':
    connection = sqlite3.connect('chats.sqlite')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Chats (chat_id integer)')

    try:
        scheduler_process = Process(target=run_schedule)
        scheduler_process.start()

        bot.polling(none_stop=True)
    
    finally:
        if scheduler_process:
            scheduler_process.terminate()
            scheduler_process.join()



