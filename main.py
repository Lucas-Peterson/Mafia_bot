import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Command
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


@dp.message_handler(Command('start'))
async def process_start_command(message: Message):
    # Создаем меню
    menu_markup = InlineKeyboardMarkup(row_width=1)
    role_button = InlineKeyboardButton("Роли", callback_data='role')
    num_button = InlineKeyboardButton("Номера", callback_data='num')
    menu_markup.add(role_button, num_button)

    # Отправляем меню
    await message.answer("БЕТА ТЕСТ НОВОГО ДИЗАЙНА", reply_markup=menu_markup)

@dp.callback_query_handler(lambda query: query.data == 'role')
async def role_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,"Введите колл-во игроков (от 4 до 10)")

    await RoleStateFSM.num_players.set()



@dp.message_handler(state=RoleStateFSM.num_players)
async def process_num_players(message: Message, state: FSMContext):
    # Создаем меню
    menu_markup = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton("Вернуться к меню", callback_data='start')
    menu_markup.add(start_button)

    if message.text.isdigit():
        num_players = int(message.text)

        if num_players < 4:
            await bot.send_message(message.chat.id, "Слишком мало игроков.")
            await state.finish()
            return
        elif num_players == 4:
            roles = ["Мирный"] * 3 + ["Мафия"]
        elif num_players == 5:
            roles = ["Мирный"] * 4 + ["Мафия"]
        elif num_players == 6:
            roles = ["Мирный"] * 4 + ["Мафия"] + ["Шериф"] + ["Дон"]
        elif num_players == 7:
            roles = ["Мирный"] * 4 + ["Мафия", "Дон", "Шериф"]
        elif num_players == 8:
            roles = ["Мирный"] * 5 + ["Мафия", "Дон", "Шериф"]
        elif num_players == 9:
            roles = ["Мирный"] * 5 + ["Мафия"] * 2 + ["Дон", "Шериф"]
        elif num_players == 10:
            roles = ["Мирный"] * 6 + ["Мафия"] * 2 + ["Дон", "Шериф"]
        else:
            await bot.send_message(message.chat.id, "Слишком много игроков.",  reply_markup=menu_markup)
            await state.finish()
            return

        # Рандомизируем роли
        random.shuffle(roles)

        # Отправляем сообщение с ролями
        result_message = "Игроки и роли:\n"
        for i, role in enumerate(roles):
            result_message += f"{i + 1}-{role}\n"
        await bot.send_message(message.chat.id, result_message, reply_markup=menu_markup)
        print(result_message)

    else:
        # Отправляем запрос на количество игроков
        await bot.send_message(message.chat.id, "Введите количество игроков:")

    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'role')
async def num_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите колл-во игроков (от 4 до 10)")

    await NumberInput.input.set()

@dp.message_handler(lambda message: message.text.isdigit() and int(message.text) in range(4, 11), state=NumberInput.input)
async def process_num(message: types.Message, state: FSMContext):

    num_players = int(message.text)
    player_numbers = random.sample(range(1, num_players + 1), num_players)

    # Создаем словарь с заменами номеров игроков
    replacements = {i: player_numbers[(i + 2) % num_players] for i in range(1, num_players + 1)}

    # Формируем ответное сообщение со списком замен
    response_message = 'Замена номеров для игроков:\n'
    for i, new_number in replacements.items():
        response_message += f'{i} => {new_number}\n'

    # Создаем меню
    menu_markup = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton("Вернуться к меню", callback_data='start')
    menu_markup.add(start_button)

    await message.answer(response_message, reply_markup=menu_markup)

    print(response_message)
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'start')
async def process_start_callback(callback_query: types.CallbackQuery):

    menu_markup = InlineKeyboardMarkup(row_width=1)
    role_button = InlineKeyboardButton("Роли", callback_data='role')
    num_button = InlineKeyboardButton("Номера", callback_data='num')
    menu_markup.add(role_button, num_button)

    # Отправляем меню
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=menu_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
