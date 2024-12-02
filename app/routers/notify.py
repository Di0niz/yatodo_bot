import datetime

from fastapi import APIRouter, BackgroundTasks
from sqlmodel import select

from app.db import SessionDep
from app.models.events import SubscribeUser, Event as EventSchema
from app.schemas import Event
from bot.loader import bot

router = APIRouter()


@router.post("/notify/")
async def schedule_event(event: Event, background_tasks: BackgroundTasks, session: SessionDep):
    """Планирует рассылку уведомлений всем зарегистрированным пользователям."""
    delay = (event.event_time - datetime.datetime.now()).total_seconds()

    event_db = session.exec(select(EventSchema).where(EventSchema.name == "test_event")).first()
    users = session.exec(select(SubscribeUser).where(SubscribeUser.event_id == event_db.id))

    if delay > 0:
        for user in users:
            background_tasks.add_task(send_notification, user.telegram_id, event.message, delay)
        return {"status": "Notification scheduled successfully"}
    else:
        return {"error": "Event time must be in the future"}

async def send_notification(chat_id: int, message: str, delay: float):
    """Отправляет уведомление после указанной задержки."""
    # await asyncio.sleep(delay)
    await bot.send_message(chat_id, message, disable_notification=False, parse_mode="HTML")
