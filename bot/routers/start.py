from aiogram import Router, F
from aiogram.types import Message
from sqlmodel import select

from app.db import context_session
from app.models.events import Event, SubscribeUser

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    chat_id = str(message.chat.id)
    first_name = message.from_user.first_name or "Неизвестно"
    last_name = message.from_user.last_name or "Неизвестно"

    with context_session() as session:
        event = session.exec(select(Event).where(Event.name == "test_event")).first()

        statement = (
            select(SubscribeUser)
            .where(
                SubscribeUser.telegram_id == chat_id,
                SubscribeUser.event_id == event.id,
            )
            .limit(1)
        )
        existing_user = session.exec(statement)
        if existing_user.first():
            await message.answer("Все хорошо, бот уже запущен!")
        else:
            new_user = SubscribeUser(
                title=f"{first_name} {last_name}",
                telegram_id=chat_id,
                event_id=event.id,
            )
            session.add(new_user)
            await message.answer(event.description)
