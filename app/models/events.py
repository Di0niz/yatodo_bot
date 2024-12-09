from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum
from sqlmodel.sql.sqltypes import AutoString


class EventType(str, Enum):
    WEBINAR = "webinar"
    MENTOR_SESSION = "mentor_session"


class Event(SQLModel, table=True):
    __tablename__ = "events_event"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    date: datetime
    description: str
    type: EventType = Field(sa_type=AutoString, nullable=False)


class SubscribeUser(SQLModel, table=True):
    class Meta:
        tablename: str = "events_subscribeuser"

    __tablename__ = "events_subscribeuser"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    telegram_id: str = Field(nullable=False)
    date_registered: datetime = Field(default_factory=datetime.utcnow)
    event_id: int | None = Field(default=None, foreign_key="events_event.id")
