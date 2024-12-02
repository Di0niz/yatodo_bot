from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship


class EventType(str, Enum):
    WEBINAR = "webinar"
    MENTOR_SESSION = "mentor_session"


class Event(SQLModel, table=True):
    class Meta:
        tablename: str = "events_event"
    __tablename__ = "events_event"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    date: datetime
    description: str
    type: EventType = Field(nullable=False)  # Тип события: webinar или mentor_session

    slots: list = Relationship(back_populates="event")

class SubscribeUser(SQLModel, table=True):
    class Meta:
        tablename: str = "events_subscribeuser"
    __tablename__ = "events_subscribeuser"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    telegram_id: str = Field(nullable=False)
    date_registered: datetime = Field(default_factory=datetime.utcnow)
    event_id: int | None = Field(default=None, foreign_key="events_event.id")
