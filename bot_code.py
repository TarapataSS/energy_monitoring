import telebot
from datetime import datetime
from to_db_example import DBConnection


telebot.apihelper.ENABLE_MIDDLEWARE = True
db = DBConnection()
# Укажем token полученный при регистрации бота
bot = telebot.TeleBot("6277486014:AAEMMkI5tC5jphAlH9yA3pnC08VZrVWQnwU")

name = ''
mechanism = 0
position = 0
worker_id = 0


@bot.message_handler(commands=['start'])
def start_command(message):
    global worker_id
    worker_id = message.from_user.id

    if not db.check_workers(worker_id):
        bot.send_message(message.from_user.id, "Я Вас еще не знаю. "
                                               "Введите пожалуйста свое имя")
        bot.register_next_step_handler(message, get_name)
    else:
        exchange_command(message)


# @bot.message_handler(commands=['log'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Начала работы на установке', callback_data='get-start')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Окончания работы за установкой', callback_data='get-finish')
    )
    bot.send_message(message.chat.id, 'Запись:', reply_markup=keyboard)
    return 1
# @bot.message_handler(content_types=['text'])
# @bot.callback_query_handler(func=lambda call: True)


def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введите пожалуйста свое имя");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');


def get_name(message):  # получаем фамилию
    name = message.text
    worker_id = message.from_user.id
    db.add_new_workers(worker_id, name)
    bot.send_message(message.from_user.id, "Я Вас запомнил :)")
    exchange_command(message)


def get_mechanism(message):
    global mechanism
    mechanism = message.text

    now = datetime.now()
    db.to_db(value=(now, worker_id, mechanism))
    bot.send_message(message.from_user.id, 'Спасибо, ответы записаны')


@bot.message_handler(commands=['start2'])
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data

    if data.endswith('-start'):
        print('1')
        position = 1
    else:
        position = 2
    bot.send_message(query.from_user.id, 'За какой установкой Вы работаете?')
    bot.register_next_step_handler(query.message, get_mechanism)

   #     get_ex_callback(query)

bot.infinity_polling(timeout=10, long_polling_timeout=5)