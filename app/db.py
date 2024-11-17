from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при работе с базой данных: {e}")
            raise
        finally:
            session.close()

@contextmanager
def context_session():
    yield from get_session()


SessionDep = Annotated[Session, Depends(get_session)]
