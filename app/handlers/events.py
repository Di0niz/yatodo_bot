import datetime

from sqlmodel import select

from app.db import context_session
from app.models.events import Event


def get_upcoming_event():
    """
    Возвращает ближайшее мероприятие по дате.
    """
    with context_session as session:
        now = datetime.utcnow()
        event = session.exec(
            select(Event)
            .where(Event.date >= now)  # Только будущие события
            .order_by(Event.date)  # Сортировка по дате
            .limit(1)  # Берем первое событие
        ).first()
        return event
