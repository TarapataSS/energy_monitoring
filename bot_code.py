import telebot
from datetime import datetime
from to_db import DBConnection
telebot.apihelper.ENABLE_MIDDLEWARE = True

db = DBConnection()

# Укажем token полученный при регистрации бота
bot = telebot.TeleBot("6277486014:AAEMMkI5tC5jphAlH9yA3pnC08VZrVWQnwU")


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    пользователь вызвал \start
    """

    worker_id = message.from_user.id

    # проверка есть ли работник в БД
    if not db.check_workers(worker_id):
        bot.send_message(message.from_user.id, "Я Вас еще не знаю. "
                                               "Введите пожалуйста свое имя")
        bot.register_next_step_handler(message, get_name)
    else:
        exchange_command(message)


def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Начало работы на установке', callback_data='get-start')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Окончание работы за установкой', callback_data='get-finish')
    )
    bot.send_message(message.chat.id, 'Отметить:', reply_markup=keyboard)


def get_name(message):  # получаем фамилию
    name = message.text
    worker_id = message.from_user.id
    db.add_new_workers(worker_id, name)
    bot.send_message(message.from_user.id, "Я Вас запомнил :)")
    exchange_command(message)


def get_mechanism(message, action=1):
    """
    сохранить действие в БД
    :param message:
    :param action:
    :return:
    """
    mechanism = message.text
    worker_id = message.from_user.id
    now = datetime.now()
    db.add_new_event(value=(now, worker_id, action, mechanism))
    bot.send_message(message.from_user.id, 'Спасибо, ответ записан')


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data

    if data.endswith('-start'):
        # если нажата кнопка start
        action = 1
    else:
        action = 0
    bot.send_message(query.from_user.id, 'За какой установкой Вы работаете?')
    bot.register_next_step_handler(query.message, get_mechanism, action=action)


if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=5)