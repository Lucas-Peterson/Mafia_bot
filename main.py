from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import Message
from random import shuffle

bot_token = '5998393415:AAHqAPrCCFf9aLZahFFcFA0D5uVtvfBNCAE'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['role'])
async def process_role_command(message: Message):
    # Отправляем запрос на количество игроков
    await bot.send_message(message.chat.id, "Введите количество игроков:")


@dp.message_handler(commands=['rules'])
async def process_rules_command(message: Message):
    # Отправляем сообщение с правилами игры
    rules_message = "Правила игры:\n\n7-8:\n4-5 мирных соответственно, 1 мафия, 1 дон, 1 шериф\n\n9-10:\n5-6 мирных соответственно, 2 мафии, 1 дон, 1 шериф"
    await bot.send_message(message.chat.id, rules_message)

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    # Приветственное сообщение
    await bot.send_message(message.chat.id, "Привет! Чтобы получить список ролей, напишите команду /role, чтобы узнать колл-во ролей, можешь ввести команду /rules")


@dp.message_handler()
async def process_message(message: Message):
    if message.text.startswith('/role'):
        return

    if message.text.isdigit():
        num_players = int(message.text)

        if num_players < 7:
            await bot.send_message(message.chat.id, "Слишком мало игроков.")
            return
        elif num_players == 7:
            roles = ["Мирный"] * 4 + ["Мафия", "Дон", "Шериф"]
        elif num_players == 8:
            roles = ["Мирный"] * 5 + ["Мафия", "Дон", "Шериф"]
        elif num_players == 9:
            roles = ["Мирный"] * 5 + ["Мафия"] * 2 + ["Дон", "Шериф"]
        elif num_players == 10:
            roles = ["Мирный"] * 6 + ["Мафия"] * 2 + ["Дон", "Шериф"]
        else:
            await bot.send_message(message.chat.id, "Слишком много игроков.")
            return

        # Рандомизируем роли
        shuffle(roles)

        # Отправляем сообщение с ролями
        result_message = "Игроки и роли:\n"
        for i, role in enumerate(roles):
            result_message += f"{i + 1}-{role}\n"
        await bot.send_message(message.chat.id, result_message)
        #print(result_message)
    else:
        # Отправляем запрос на количество игроков
        await bot.send_message(message.chat.id, "Введите количество игроков:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
