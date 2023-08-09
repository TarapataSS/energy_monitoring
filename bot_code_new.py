import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

STATION, NUM_MECH, CLOSE, GET_NAME = range(4)
# user_list = [236872275]
user_list = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation"""
    reply_keyboard = [["Начать работу на установке", "Завершить работу"]]

    user_id = update.message.from_user.id
    if user_id not in user_list:
        await update.message.reply_text(
            "Привет! Я вас еще не знаю, введите имя и фамилию",
        )
        return GET_NAME

    await update.message.reply_text(
        "Привет! "
        "Отправь /cancel, сели захотите завершить сессию\n\n"
        "Вы планируете начать или закончить работу?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Начинаете или завершаете работу?"
        ),
    )

    return STATION


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("введенное имя  %s: %s", user.first_name, update.message.text)

    user_list.append(user.id)

    reply_keyboard = [["Начать работу на установке", "Завершить работу"]]

    await update.message.reply_text(
        "Отправь /cancel, сели захотите завершить сессию\n\n"
        "Вы планируете начать или закончить работу?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Начинаете или завершаете работу?"
        ),
    )

    return STATION
    # return PHOTO


async def station(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Пользователь %s: выбрал %s", user.first_name, update.message.text)

    reply_keyboard = [["1", "2", "3"]]
    await update.message.reply_text(
        "Отлично, выберите номер установки",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Номер установки?"
        ),
    )

    return NUM_MECH


async def select_num_mech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Пользователь %s: выбрал %s", user.first_name, update.message.text)

    await update.message.reply_text(
        "Спасибо, ответ записан", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s закончил диалог", user.first_name)
    await update.message.reply_text(
        "Спасибо, ответ записан", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6277486014:AAEMMkI5tC5jphAlH9yA3pnC08VZrVWQnwU").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STATION: [MessageHandler(filters.Regex("^(Начать работу на установке|Завершить работу)$"), station)],
            NUM_MECH: [MessageHandler(filters.Regex("^(1|2|3)$"), select_num_mech)],
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CLOSE: [CommandHandler("cancel", cancel)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
