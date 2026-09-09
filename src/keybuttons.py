from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить", callback_data="confirm_reg"
            ),
            InlineKeyboardButton(
                text="Начать заново", callback_data="restart_reg"
            ),
        ]
    ]
)