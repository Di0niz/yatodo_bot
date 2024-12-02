import datetime

from sqlmodel import select

from app.db import context_session
from app.models.booking import Slot, BookingSlot


def get_available_slots(event_id: int):
    """
    Возвращает список доступных слотов для события.
    """
    with context_session() as session:
        available_slots = session.exec(
            select(Slot)
            .outerjoin(
                BookingSlot,
                (Slot.id == BookingSlot.slot_id) & (BookingSlot.canceled_dt is None),
            )
            .where(Slot.event_id == event_id, BookingSlot.id is None)  # Слот без активной брони
        ).all()

        return available_slots


def book_slot(slot_id: int, telegram_id: str):
    with context_session() as session:
        # Проверяем, свободен ли слот
        booking = session.exec(
            select(BookingSlot).where(
                BookingSlot.slot_id == slot_id,
                BookingSlot.canceled_dt is None,
            )
        ).first()
        if booking:
            return False  # Слот уже занят

        # Создаем запись бронирования
        new_booking = BookingSlot(slot_id=slot_id, telegram_id=telegram_id)
        session.add(new_booking)
        session.commit()
        return True


def cancel_booking(event_id: int, telegram_id: str):
    with context_session() as session:
        booking = session.exec(
            select(BookingSlot).where(
                event_id == event_id,
                BookingSlot.telegram_id == telegram_id,
                BookingSlot.canceled_dt is None,
            )
        ).first()
        if not booking:
            return False  # Активной записи нет

        # Отменяем запись
        booking.canceled_dt = datetime.datetime.utcnow()
        session.add(booking)
        session.commit()
        return True
