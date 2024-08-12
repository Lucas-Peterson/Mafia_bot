from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    role_button = InlineKeyboardButton("Roles", callback_data='role')
    num_button = InlineKeyboardButton("Numbers", callback_data='num')
    keyboard.add(role_button, num_button)
    return keyboard
