import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import points

with open("BOT_KEY", "r") as keyFile:
    bot = telebot.TeleBot(keyFile.readline().strip())

points.init_db()


def keyboard():
    return ReplyKeyboardMarkup(row_width=3).add(
        *[KeyboardButton(x) for x in ("-1", "clear", "+1")]
    )


def main_keyboard():
    return ReplyKeyboardMarkup(row_width=1).add(
        *[KeyboardButton(x) for x in ("/open_class", "/new_class", "/remove_class")]
    )


@bot.message_handler(commands=["help", "start"])
def cmd_main(msg):
    bot.reply_to(
        msg, """hi there! this is a main menu!""", reply_markup=main_keyboard()
    )


@bot.message_handler(commands=["open_class"])
def cmd_open_class(msg):
    bot.send_message(
        msg.chat.id,
        f"Select the class:\n"
        + "\n".join(map(lambda x: x[1], points.get_classes(msg.chat.id))),
    )
    bot.register_next_step_handler(msg, select_class)


def select_class(msg):
    try:
        selected = next(
            (x[0] for x in points.get_classes(msg.chat.id) if x[1] == msg.text)
        )
        bot.send_message(
            msg.chat.id,
            "List of class students:\n"
            + "\n".join(
                [f"{x} {y}"
                 for x, y in enumerate(points.get_students(selected))]
            ),
            parse_mode="Markdown"
        )
    except:
        bot.send_message(msg.chat.id, "Oops!")


@bot.message_handler(commands=["new_class"])
def cmd_new_class(msg):
    bot.send_message(
        msg.chat.id,
        f'Enter the new class name. Or enter "cancel" (case-insensitive) to cancel the operation',
    )
    bot.register_next_step_handler(msg, add_new_class)


def add_new_class(msg):
    if msg.text.lower() == "cancel":
        bot.send_message(msg.chat.id, "Cancelled!")
    else:
        try:
            points.add_class(msg.chat.id, msg.text)
            bot.send_message(msg.chat.id, f"Added {msg.text}")
        except:
            bot.send_message(msg.chat.id, "Oops!")


@bot.message_handler(commands=["reset_points"])
def cmd_clear_points(msg):
    pass


@bot.message_handler(commands=["edit_class"])
def cmd_edit_class(msg):
    pass


@bot.message_handler(commands=["remove_class"])
def cmd_remove_class(msg):
    pass


@bot.message_handler(commands=["test"])
def msg_test(msg):
    bot.send_message(msg.chat.id, "enter your name:")
    bot.register_next_step_handler(msg, get_name)


def get_name(msg):
    bot.send_message(msg.chat.id, f"hello, {msg.text}!")


bot.infinity_polling()
