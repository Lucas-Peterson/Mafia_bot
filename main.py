from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config import TOKEN
from bot.handlers import register_handlers

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def main():
    # Register handlers
    register_handlers(dp)

    # Start polling
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
