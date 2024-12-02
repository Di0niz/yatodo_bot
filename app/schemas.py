import datetime

from pydantic import BaseModel


# Модель события
class Event(BaseModel):
    event_time: datetime.datetime
    message: str
