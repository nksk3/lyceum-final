from random import randint
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import points


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def add_class(update: Update, context: CallbackContext):
    name = str(randint(0, 99999))
    points.add_class(update.effective_user.id, name)
    update.message.reply_text(name)


def get_classes(update: Update, context: CallbackContext):
    update.message.reply_text(str(points.get_classes(update.effective_user.id)))


if __name__ == "__main__":
    """Start the bot."""
    points.init_db()
    updater = Updater("5383383919:AAFn0onV6ifKX_QwbhqmH5DAG41eFGkBQsw")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add_class", add_class))
    dispatcher.add_handler(CommandHandler("get_classes", get_classes))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, lambda *_: 1)
    )

    updater.start_polling()

    updater.idle()
