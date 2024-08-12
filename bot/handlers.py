from bot.roles import generate_roles, format_roles_message
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.dispatcher.filters import Command
from bot.states import RoleStateFSM, NumberInput
from bot.keyboards import create_menu_keyboard
from aiogram.dispatcher import Dispatcher

# В функции process_num_players
@dp.message_handler(state=RoleStateFSM.num_players)
async def process_num_players(message: Message, state: FSMContext):
    menu_markup = create_menu_keyboard()

    if message.text.isdigit():
        num_players = int(message.text)

        try:
            roles = generate_roles(num_players)
            result_message = format_roles_message(roles)
            await message.answer(result_message, reply_markup=menu_markup)
            print(result_message)
        except ValueError as e:
            await message.answer(str(e), reply_markup=menu_markup)
            await state.finish()
            return
    else:
        await message.answer("Please enter a valid number of players:")

    await state.finish()
