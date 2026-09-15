from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from src.keybuttons import buttons, gender_button, edit_buttons

router = Router()

user_data = {}

class Regis(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    confirm = State()

class Edit_Regis(StatesGroup):
    new_name = State()
    new_age = State()
    new_city = State()
    new_gender = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд\n"
        "/register - регистрация\n"
        "/profile - выводит информацию о текущем пользователе\n"
        "/edit - редактирует ваши данные"
    )


@router.message(Command('register'))

async def smd_redis_start(message: Message, state: FSMContext):
    await message.answer('1-Введите ваше имя:')
    await state.set_state(Regis.name)



@router.message(Regis.name)
async def smd_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('2-Введите ваш возрост:')
    await state.set_state(Regis.age)


@router.message(Regis.age)

async def cmd_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('прошу введите число:')
        return

    age = int(message.text)
    if age <= 0:
        await message.answer('прошу введите число больше 0:')
        return

    await state.update_data(age = age)
    await message.answer(f'Введите ваш город:')
    await state.set_state(Regis.city)


@router.message(Regis.city)
async def message(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    await message.answer('выберите ваш пол:', reply_markup=gender_button)
    await state.set_state(Regis.gender)

@router.callback_query(Regis.gender, F.data.in_({'female', 'male'}))
async def cmd_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    gender_answer = 'женский' if callback.data == 'female' else 'мужской'
    await state.update_data(gender=gender_answer)
    data = await state.get_data()
    await callback.message.answer(
        f"Проверьте ваши данные:\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Город: {data['city']}\n"
        f"Пол: {data['gender']}\n\n"
        f"Всё верно?",
        reply_markup=buttons,
    )

    await state.set_state(Regis.confirm)

@router.callback_query(Regis.confirm, F.data == 'confirm_reg')
async def cmd_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    user_data[callback.from_user.id] = {"name": data["name"],
        "age": data["age"],
        "city": data["city"],
        "gender": data["gender"],}
    await callback.message.edit_text('Решистрация завершена')
    await state.clear()

@router.callback_query(Regis.confirm, F.data == 'restart_reg')  
async def cmd_restart(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Начнем заного! Введите ваше имя:')
    await state.set_state(Regis.name)  
    


@router.message(Command('profile'))
async def cmd_profile(message: Message):
    user = user_data.get(message.from_user.id)
    if not user:
        await message.answer('Вы не зарегестрированы, прошу зарегестрируйтесь /register')
    else:
        await message.answer(f'ваши данные\n\nИмя - {user['name']}\nВозрост - {user['age']}\nГород - {user['city']}\nПол - {user['gender']}')


@router.message(Command('edit'))
async def cmd_edit(message: Message):
    user = user_data.get(message.from_user.id)
    if not user:
        await message.answer('Вы не зарегестрированы, прошу зарегестрируйтесь /register')
        return
    else:
        await message.answer('Выберите кнопку параметра которого хотите изменить:', 
                             reply_markup=edit_buttons)

@router.callback_query(F.data == 'edit_name')
async def cmd_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Edit_Regis.new_name)
    await callback.message.answer('Введите новое имя:')

@router.callback_query(F.data == 'edit_age')
async def cmd_edit_age(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Edit_Regis.new_age)
    await callback.message.answer('Введите новый возрост:')

@router.callback_query(F.data == 'edit_city')
async def cmd_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Edit_Regis.new_city)
    await callback.message.answer('Введите новый город:')

@router.callback_query(F.data == 'edit_gender')
async def cmd_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Edit_Regis.new_gender)
    await callback.message.answer('Введите свой пол:', reply_markup=gender_button)

@router.message(Edit_Regis.new_name)
async def cmd_new_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    new_name = message.text
    user_data[user_id]['name'] = new_name
    await message.answer(f'Ваше имя было отредоктирована на:{new_name}')
    await state.clear()

@router.message(Edit_Regis.new_age)
async def cmd_new_age(message: Message, state:FSMContext):
    if not message.text.isdigit():
        await message.answer('прошу введите число:')
        return
    
    new_age = int(message.text)
    if new_age <= 0:
        await message.answer('прошу введите число больше 0:')
        return

    user_id = message.from_user.id
    user_data[user_id]['age'] = new_age  
    await message.answer(f'Ваш возрост был отредоктирован на: {new_age}')
    await state.clear() 

@router.message(Edit_Regis.new_city)
async def cmd_new_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    new_city = message.text
    user_data[user_id]['city'] = new_city
    await message.answer(f'Ваш город был отредоктирован на: {new_city}')
    await state.clear()

@router.callback_query(Edit_Regis.new_gender, F.data.in_({'female', 'male'}))
async def cmd_new_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    new_gender = 'женский' if callback.data == 'female' else 'мужской'

    user_id = callback.from_user.id
    user_data[user_id]['gender'] = new_gender
    await callback.message.edit_text(f'Ваш пол был отредоктирован на: {new_gender}')
    await state.clear()   
    