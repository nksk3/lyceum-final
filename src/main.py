from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup

import points

with open("BOT_KEY", "r") as keyFile:
    bot = AsyncTeleBot(keyFile.readline().strip())

points.init_db()



class States(StatesGroup):
    new_class = State()
    remove_class = State()
    open_class = State()
    open_class_input = State()
    change_points = State()
    add_student = State()
    remove_student = State()
    edit_student = State()
    clear_points = State()



@bot.message_handler(state="*", commands='cancel')
async def cancel_state(msg):
    """
    Cancel state
    """
    await bot.send_message(msg.chat.id, "Your state was cancelled.")
    await bot.delete_state(msg.from_user.id, msg.chat.id)

@bot.message_handler(commands=['new_class', "new"])
async def new_class_cmd(msg):
    await bot.set_state(msg.from_user.id, States.new_class, msg.chat.id)
    await bot.send_message(msg.chat.id, 'Enter new class name')

@bot.message_handler(state=States.new_class)
async def new_class(msg):
    await bot.delete_state(msg.from_user.id, msg.chat.id)
    try:
        points.add_class(msg.chat.id, msg.text)
        await bot.send_message(msg.chat.id, "Class added")
    except:
        await bot.send_message(msg.chat.id, "Oops!")

@bot.message_handler(commands=['remove_class', "remove"])
async def remove_class_cmd(msg):
    await bot.set_state(msg.from_user.id, States.remove_class, msg.chat.id)
    await list_classes(msg.chat.id)
    await bot.send_message(msg.chat.id, 'Enter class name to be deleted')

@bot.message_handler(state=States.remove_class)
async def remove_class(msg):
    await bot.delete_state(msg.from_user.id, msg.chat.id)
    try:
        points.remove_class(msg.chat.id, msg.text)
        await bot.send_message(msg.chat.id, "Class removed")
    except:
        await bot.send_message(msg.chat.id, "Oops!")

@bot.message_handler(commands=['open_class', 'open'])
async def open_class_cmd(msg):
    await bot.set_state(msg.from_user.id, States.open_class, msg.chat.id)
    await list_classes(msg.chat.id)
    await bot.send_message(msg.chat.id, 'Enter class to open')

@bot.message_handler(state=States.open_class)
async def open_class(msg):
    try:
        await bot.set_state(msg.from_user.id, States.open_class_input, msg.chat.id)
        async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
            data['class'] = next((i for i, x in points.get_classes(msg.chat.id) if x == msg.text))
            await bot.send_message(
                msg.chat.id,
                "Class students:\n" + "\n".join((x for x, _ in points.get_students(data["class"])))
            )
        await bot.send_message(msg.chat.id, "Enter student name to change their points")
    except:
        await bot.send_message(msg.chat.id, "Oops!")

@bot.message_handler(state=States.open_class_input, commands=["add", "add_student"])
async def open_class_add_student(msg):
    await bot.set_state(msg.from_user.id, States.add_student, msg.chat.id)
    await bot.send_message(msg.chat.id, "Enter new student name")

@bot.message_handler(state=States.add_student)
async def add_student(msg):
    await bot.set_state(msg.from_user.id, States.open_class, msg.chat.id)
    async with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        points.add_student(data['class'], msg.text)
    await bot.send_message(msg.from_user.id, "Added student")

@bot.message_handler(state=States.open_class_input)
async def open_class_input(msg):
    try:
        pass
    except:
        await bot.send_message(msg.chat.id, "Oops!")

async def list_classes(chat_id):
    await bot.send_message(
        chat_id,
        "Available classes:\n" + "\n".join((x for _, x in points.get_classes(chat_id)))
    )

bot.add_custom_filter(asyncio_filters.StateFilter(bot))

import asyncio
asyncio.run(bot.polling())
