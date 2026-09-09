from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.keybuttons import keyboard

router = Router()

users_data = {}


class Registration(StatesGroup):
    name = State()
    age = State()
    confirm = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - приветствие\n"
        "/help - список команд\n"
        "/register - регистрация\n"
        "/profile - выводит информацию о текущем пользователе"
    )



@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer("Шаг 1: Введите ваше имя:")
    await state.set_state(Registration.name)


@router.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Шаг 2: Введите ваш возраст:")
    await state.set_state(Registration.age)


@router.message(Registration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Это не число! Пожалуйста, введите возраст цифрами:")
        return

    age = int(message.text)
    if age <= 0:
        await message.answer("Возраст должен быть больше нуля! Введите возраст ещё раз:")
        return

    await state.update_data(age=age)
    data = await state.get_data()

    await message.answer(
        f"Проверьте данные:\n\nИмя: {data['name']}\nВозраст: {data['age']}\n\nВсё верно?",
        reply_markup=keyboard
    )
    await state.set_state(Registration.confirm)


@router.callback_query(Registration.confirm, F.data == "confirm_reg")
async def confirm_reg(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_data[callback.from_user.id] = {"name": data["name"], "age": data["age"]}
    await callback.message.edit_text("Регистрация завершена!")
    await state.clear()
    await callback.answer()


@router.callback_query(Registration.confirm, F.data == "restart_reg")
async def restart_reg(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Начнем заново. Шаг 1: Введите ваше имя:")
    await state.set_state(Registration.name)
    await callback.answer()


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user = users_data.get(message.from_user.id)
    if user:
        await message.answer(f"Ваши данные:\n\nИмя — {user['name']}\nВозраст — {user['age']}")
    else:
        await message.answer("Вы не зарегистрированы. Напишите /register, чтобы пройти регистрацию.")