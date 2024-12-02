from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup, InlineKeyboardButton

from app.handlers.booking import get_available_slots, book_slot, cancel_booking

router = Router()


@router.message_handler(commands=["slots"])
async def show_slots(message: Message):
    event_id = ...  # Определите текущий ID события
    slots = get_available_slots(event_id)
    if not slots:
        await message.answer("Нет доступных слотов.")
        return

    keyboard = InlineKeyboardMarkup()
    for slot in slots:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{slot.time_slot.strftime('%Y-%m-%d %H:%M')}",
                callback_data=f"book_{slot.id}",
            )
        )
    await message.answer("Доступные слоты:", reply_markup=keyboard)


@router.callback_query_handler(lambda c: c.data.startswith("book_"))
async def book_slot_handler(callback_query: CallbackQuery):
    slot_id = int(callback_query.data.split("_")[1])
    telegram_id = callback_query.from_user.id

    success = book_slot(slot_id, telegram_id)
    if success:
        await callback_query.message.answer("Слот успешно забронирован!")
    else:
        await callback_query.message.answer("Слот уже занят.")


@router.message_handler(commands=["cancel_booking"])
async def cancel_booking_command(message: Message):
    telegram_id = message.from_user.id
    success = cancel_booking(telegram_id)
    if success:
        await message.answer("Ваша запись успешно отменена.")
    else:
        await message.answer("У вас нет активной записи.")
