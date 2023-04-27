import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from random import shuffle
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token='5998393415:AAHqAPrCCFf9aLZahFFcFA0D5uVtvfBNCAE')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class RoleStateFSM(StatesGroup):
    num_players = State()
class NumberInput(StatesGroup):
    input = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    # Приветственное сообщение
    await bot.send_message(message.chat.id, "Тест механик начат, используйте тест команды /role и /num ")


@dp.message_handler(Command('role'))
async def process_role_command(message: Message):
    # Устанавливаем состояние num_players, ожидаем количество игроков
    await RoleStateFSM.num_players.set()

    # Отправляем запрос на количество игроков
    await bot.send_message(message.chat.id, "Введите количество игроков:")


@dp.message_handler(state=RoleStateFSM.num_players)
async def process_num_players(message: Message, state: FSMContext):
    if message.text.isdigit():
        num_players = int(message.text)

        if num_players < 7:
            await bot.send_message(message.chat.id, "Слишком мало игроков.")
            await state.finish()
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
            await state.finish()
            return

        # Рандомизируем роли
        shuffle(roles)

        # Отправляем сообщение с ролями
        result_message = "Игроки и роли:\n"
        for i, role in enumerate(roles):
            result_message += f"{i + 1}-{role}\n"
        await bot.send_message(message.chat.id, result_message)
        print(result_message)

    else:
        # Отправляем запрос на количество игроков
        await bot.send_message(message.chat.id, "Введите количество игроков:")

    await state.finish()


@dp.message_handler(commands=['num'])
async def num_command_handler(message: types.Message):
    await message.answer('Введите количество игроков (от 7 до 10):')
    await NumberInput.input.set()

@dp.message_handler(lambda message: message.text.isdigit() and int(message.text) in range(7, 11), state=NumberInput.input)
async def process_num(message: types.Message, state: FSMContext):
    num_players = int(message.text)
    player_numbers = random.sample(range(1, num_players + 1), num_players)

    # Создаем словарь с заменами номеров игроков
    replacements = {i: player_numbers[(i + 2) % num_players] for i in range(1, num_players + 1)}

    # Формируем ответное сообщение со списком замен
    response_message = 'Замена номеров для игроков:\n'
    for i, new_number in replacements.items():
        response_message += f'{i} => {new_number}\n'

    await message.answer(response_message)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
