import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config import BOT_TOKEN
from bot.routers import start


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Добавляем маршрутизатор к диспетчеру
dp.include_router(start.router)

async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="slots", description="Посмотреть доступные слоты"),
        BotCommand(command="cancel_booking", description="Отменить запись"),
        BotCommand(command="help", description="Показать список команд"),
    ]
    # if ADMIN_ID:  # Команды администратора
    #     admin_commands = [
    #         BotCommand(command="send_link", description="Отправить ссылку пользователю"),
    #     ]
    #     commands.extend(admin_commands)

    await bot.set_my_commands(commands)


async def on_startup(dp):
    await set_bot_commands()
