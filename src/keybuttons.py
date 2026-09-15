from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = InlineKeyboardMarkup(
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

gender_button = InlineKeyboardMarkup(

    inline_keyboard =[
        [
            InlineKeyboardButton(text = 'женский', callback_data='female'),
            InlineKeyboardButton(text = 'мужской', callback_data='male')
        ]
])


edit_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = 'Имя', callback_data= 'edit_name'), 
            InlineKeyboardButton(text = 'Возрост', callback_data='edit_age')
        ], 
        [
            InlineKeyboardButton(text='Город',callback_data='edit_city'),
            InlineKeyboardButton(text='Пол', callback_data='edit_gender')
        ]
    ]
)