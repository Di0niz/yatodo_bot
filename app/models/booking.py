from datetime import datetime

from sqlmodel import Field, SQLModel

class Slot(SQLModel, table=True):
    class Meta:
        tablename: str = "bookings_slot"
    __tablename__ = "bookings_slot"
    id: int | None = Field(default=None, primary_key=True)
    event_id: int | None = Field(default=None, foreign_key="events_event.id")
    time_slot: datetime = Field(nullable=False)

class BookingSlot(SQLModel, table=True):
    class Meta:
        tablename: str = "bookings_book"
    __tablename__ = "bookings_book"
    id: int | None = Field(default=None, primary_key=True)
    slot_id: int | None = Field(default=None, foreign_key="bookings_slot.id")
    telegram_id: str = Field(nullable=True)
    canceled_dt: datetime | None = Field(nullable=True)
