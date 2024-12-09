from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "/help")
async def send_help(message: Message):
    help_text = """
Доступные команды:
/start - Начать работу с ботом
"""

    # /slots - Посмотреть список доступных слотов
    # /cancel_booking - Отменить запись
    # /help - Показать это сообщение

    await message.answer(help_text)
