import asyncio
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import notify
from bot.loader import bot, dp, on_startup
from app.db import engine


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при запуске приложения
    asyncio.create_task(dp.start_polling(bot, on_startup=on_startup))

    yield  # Переход к выполнению FastAPI
    # Действия при завершении приложения
    await dp.storage.close()
    await bot.session.close()
    engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(notify.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
