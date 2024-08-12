from aiogram.dispatcher.filters.state import State, StatesGroup

class RoleStateFSM(StatesGroup):
    num_players = State()

class NumberInput(StatesGroup):
    input = State()
