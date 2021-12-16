import random
import telebot
import pycbrf
import datetime
from answer import not_know, know
from config import TOKEN

HELP = """
/add  добавить ему фразу (/add *фраза*)
/rate курс доллара
"""
bot = telebot.TeleBot(TOKEN)

alphabet = {"а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
            "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"}


# Вывод курса
@bot.message_handler(commands=["rate"])
def rate(message):
    rates = pycbrf.ExchangeRates(datetime.datetime.now())
    bot.send_message(message.chat.id, str(rates['USD'].value) + ' ₽')

# Что напишет бот при старте
@bot.message_handler(commands=["start"])
def welkome(message):
    bot.send_message(message.chat.id, HELP)

# Вывод команды help
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

# Добавление фразы в БД
@bot.message_handler(commands=["add"])
def add(message):
    word = open("nikita_phrases.txt", "r").readlines()
    text = ' '.join(message.text.split()[1:])
    print(text)
    try:
        if bool(alphabet.intersection(set(text.lower()))):
            if text + '\n' in word:
                answer = (random.choice(know))
            else:
                word_write = open("nikita_phrases.txt", "a")
                word_write.write(text + '\n')
                word_write.close()
                answer = (random.choice(not_know))
        else:
            answer = 'Английский не знаю'
    except UnicodeEncodeError:
        answer = 'На смайлики не отвчаю'
    bot.send_message(message.chat.id, answer)

# Ответ бота на сообщение
@bot.message_handler(content_types=["text"])
def speech(message):
    text = random_word()
    bot.send_message(message.chat.id, text)

# Функция для рандмного ответа
def random_word():
    word = open('nikita_phrases.txt').readlines()
    return random.choice(word)


bot.polling(none_stop=True)
