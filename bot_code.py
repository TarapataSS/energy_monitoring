import telebot

telebot.apihelper.ENABLE_MIDDLEWARE = True

# Укажем token полученный при регистрации бота
bot = telebot.TeleBot("6277486014:AAHq7ReYRAb8WsooxwaE_l8nlu1cZUpf1LU")

name = ''
mechanism = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введите пожалуйста свое имя");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');


def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'За какой установкой Вы работаете?');
    bot.register_next_step_handler(message, get_mechanism);


def get_mechanism(message):
    global mechanism
    mechanism = message.text
    bot.send_message(message.from_user.id, 'Спасибо, ответы записаны')


bot.infinity_polling(timeout=10, long_polling_timeout=5)

