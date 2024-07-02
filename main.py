import time
import telebot
from crypto_module import Crypto
import sqlite3
import asyncio
import ast

# Replace 'YOUR_BOT_API_TOKEN' with your actual bot token
API_TOKEN = 'your api token'

bot = telebot.TeleBot(API_TOKEN)
conn = sqlite3.connect('main.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        favorite_crypto TEXT,
        number_crypto INTEGER     
    )
''')
conn.commit()
cursor.close()

def get_info(message):
    crypto = Crypto()
    target = get_db(message, argument="favorite_crypto")[0]
    target_list = ast.literal_eval(target)
    prices = []
    for i in target_list:
        price = crypto.fetch_specific_crypto_prices(i)
        prices.append(price)
    return prices



def add_info(user_id, favorite_crypto, number_cryptos):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, favorite_crypto, number_crypto) VALUES (?, ?, ?)",
                   (user_id, favorite_crypto, number_cryptos))
    conn.commit()

def get_db(message, argument):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT {argument} FROM users WHERE id = ?", (message.chat.id,))
    return cursor.fetchone()

async def emergency(message):
    while True:
        list1 = []
        list2 = []
        price1 = get_info(message)
        await asyncio.sleep(5)
        price2 = get_info(message)
        for i in price1:
            items = list(i.items())
            list1.append(items[0][1])
        for i in price2:
            items = list(i.items())
            list2.append(items[0][1])
        for i in list1:
            alarm = i - list2[list1.index(i)]
            if abs(alarm) >= i * 0.05:
                bot.send_message(message.chat.id,f"резкое изенение цены {list(i.items())[0][list1[list1.index(i)]]}")
            else:
                pass


@bot.message_handler(commands=['emrgency'])
def emergency1(message):
    bot.send_message(message.chat.id, "каждый час вслучаи обвала ввы получите ссобщение")
    asyncio.run(emergency(message))

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "привет это крипта биржа введите /help ")

# Handler for echoing messages
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "все функции: \n /help - помощь \n /start - старт \n /crypto_price - цена крипты \n /user_prefernce - предпочтение пользователей ")

@bot.message_handler(commands=['crypto_price'])
def send_crupto_info(message):
    crypto = Crypto()
    crypto_prices = crypto.fetch_crypto_prices(get_db(message, "number_crypto")[0])
    bot.send_message(message.chat.id, "\n".join(crypto_prices))

@bot.message_handler(commands=['user_prefernce'])
def registrate(message):
    bot.send_message(message.chat.id,"привет укажите нужные данные для качетсва сервиса")
    bot.send_message(message.chat.id,"ваша любимая или любимые криптовалюты (краткое название из 3 букв) если не хотите напишите нет")
    list1 = []
    bot.register_next_step_handler(message,add_data,list1)
def add_data(message,list1):
    if len(message.text) > 4:
        bot.send_message(message.chat.id,"ошибка название слишком длинное более 4 сиволов!")
        bot.register_next_step_handler(message, add_data, list1)
    elif message.text.lower() == "нет":
        bot.register_next_step_handler(message, add_data_step2, list1)
    else:
        bot.send_message(message.chat.id, "напшите ещё елси хотите или напишите нет")
        list1.append(message.text)
        print(list1)
        bot.register_next_step_handler(message, add_data, list1)
def add_data_step2(message,list1):
    bot.send_message(message.chat.id,"ок , введите сколько крипотовалют будет выводиться на главной странице (по дефолту 100)")
    bot.register_next_step_handler(message, add_data_step3, list1)

def add_data_step3(message, list1):
    count = message.text
    try:
        count = int(count)
        Status = True
    except ValueError:
        Status = False

    if count < 4000 and Status == True:
        bot.send_message(message.chat.id, "ок опреации прошла успешно")
        add_info(message.chat.id, str(list1), count)

    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, add_data_step3, list1)

bot.infinity_polling()
