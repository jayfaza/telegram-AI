from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Модель 📖", callback_data="model")],
        [InlineKeyboardButton(text="История 📝", callback_data="history")],
    ]
)

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль 🪪")],
        [KeyboardButton(text="Очистить историю 📝"), KeyboardButton(text="История 📝")],
        [KeyboardButton(text="Модель 📖"), KeyboardButton(text="Сменить промпт ⌨️")],
    ],
    resize_keyboard=True,
)

close_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть ❌", callback_data="remove_msg")]
    ]
)
