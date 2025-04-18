import requests
from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from .states import AddExpense, GetReport
from .keyboards import main_menu
from datetime import datetime


router = Router()


@router.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    await message.answer("Привіт! Обери дію з меню 👇", reply_markup=main_menu())
    await state.clear()


@router.callback_query(F.data == "add_expense")
async def add_expense_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddExpense.title)
    await callback.message.answer("Введіть назву витрати:")
    await callback.answer()


@router.message(AddExpense.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddExpense.amount)
    await message.answer("Введіть суму витрати у грн:")


@router.message(AddExpense.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        await state.update_data(amount=amount)
        await state.set_state(AddExpense.date)
        await message.answer("Введіть дату витрати у форматі `dd.mm.yyyy`:")
    except ValueError:
        await message.answer("⚠️ Введіть коректну суму (наприклад, 123.45):")


@router.message(AddExpense.date)
async def process_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
        await state.update_data(date=str(date))
        await state.set_state(AddExpense.description)
        await message.answer("Введіть опис витрати (або напишіть `-`, якщо без опису):")
    except ValueError:
        await message.answer("⚠️ Невірний формат дати. Спробуй ще раз (dd.mm.yyyy):")


@router.message(AddExpense.description)
async def process_description(message: Message, state: FSMContext):
    description = message.text if message.text.strip() != "-" else ""
    await state.update_data(description=description)
    data = await state.get_data()
    await state.clear()

    try:
        if "expense_id" in data:
            expense_id = data["expense_id"]
            response = requests.put(f"http://127.0.0.1:8000/expenses/{expense_id}", json={
                "category": data["title"],
                "amount_uah": data["amount"],
                "date": data["date"],
                "description": data["description"],
            })

            if response.status_code == 200:
                await message.answer("✅ Витрату успішно оновлено!", reply_markup=main_menu())
            else:
                await message.answer(f"⚠️ Помилка при оновленні: {response.text}", reply_markup=main_menu())
        else:
            # Иначе создаем новую запись
            response = requests.post("http://127.0.0.1:8000/expenses/", json={
                "category": data['title'],
                "amount_uah": data['amount'],
                "date": data['date'],
                "description": data['description'],
            })

            if response.status_code == 200:
                await message.answer("✅ Витрату успішно додано!", reply_markup=main_menu())
            else:
                await message.answer(f"⚠️ Помилка при додаванні: {response.text}", reply_markup=main_menu())

    except Exception as e:
        await message.answer(f"❌ Помилка: {e}", reply_markup=main_menu())


@router.callback_query(F.data == "get_report")
async def handle_get_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введіть **початкову дату** у форматі `dd.mm.yyyy`:")
    await state.set_state(GetReport.start_date)
    await callback.answer()


@router.message(GetReport.start_date)
async def process_start_date(message: Message, state: FSMContext):
    try:
        start_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        await state.update_data(start_date=str(start_date))
        await message.answer("Тепер введіть **кінцеву дату** у форматі `dd.mm.yyyy`:")
        await state.set_state(GetReport.end_date)
    except ValueError:
        await message.answer("⚠️ Невірний формат. Спробуй ще раз (dd.mm.yyyy):")


@router.message(GetReport.end_date)
async def process_end_date(message: Message, state: FSMContext):
    try:
        end_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        data = await state.get_data()
        start_date = data['start_date']
        end_date_str = str(end_date)
        await state.clear()

        url = f"http://127.0.0.1:8000/expenses/?start_date={start_date}&end_date={end_date_str}"
        response = requests.get(url)

        if response.status_code == 200:
            expenses = response.json()
            if not expenses:
                await message.answer("💸 Витрат за цей період не знайдено.")
            else:
                text = "📄 Звіт витрат:\n\n"
                for exp in expenses:
                    text += f"📅 {exp['date']}: {exp['category']} — {exp['amount_uah']} грн\n"
                await message.answer(text)
        else:
            await message.answer(f"⚠️ Помилка сервера: {response.text}")

    except ValueError:
        await message.answer("⚠️ Невірний формат. Спробуй ще раз (dd.mm.yyyy):")


@router.callback_query(F.data == "delete_expense")
async def handle_delete_expense(callback: CallbackQuery):
    response = requests.get("http://127.0.0.1:8000/expenses/")
    if response.status_code == 200:
        expenses = response.json()
        if not expenses:
            await callback.message.answer("💸 У вас немає витрат для видалення.")
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=f"{e['category']} - {e['amount_uah']} грн", callback_data=f"delete_{e['id']}")]
                    for e in expenses
                ]
            )
            await callback.message.answer("🗑 Оберіть витрату для видалення:", reply_markup=keyboard)
    else:
        await callback.message.answer("⚠️ Помилка при отриманні списку витрат.")
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def confirm_delete(callback: CallbackQuery):
    expense_id = callback.data.split("_")[1]
    response = requests.delete(f"http://127.0.0.1:8000/expenses/{expense_id}")

    if response.status_code == 200:
        await callback.message.answer("✅ Витрату успішно видалено!", reply_markup=main_menu())
    else:
        await callback.message.answer(f"❌ Помилка при видаленні: {response.text}", reply_markup=main_menu())

    await callback.answer()


@router.callback_query(F.data == "edit_expense")
async def handle_edit_expense(callback: CallbackQuery, state: FSMContext):
    response = requests.get("http://127.0.0.1:8000/expenses/")
    expenses = response.json()

    if not expenses:
        await callback.message.answer("У вас поки що немає витрат.")
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"{e['category']} - {e['amount_uah']} грн",
                    callback_data=f"edit_{e['id']}"
                )] for e in expenses
            ]
        )
        await callback.message.answer("Оберіть витрату для редагування:", reply_markup=keyboard)

    await callback.answer()


@router.callback_query(F.data.startswith("edit_"))
async def handle_edit_choice(callback: CallbackQuery, state: FSMContext):
    expense_id = callback.data.split("_")[1]
    await state.update_data(expense_id=expense_id)
    await state.set_state(AddExpense.title)
    await callback.message.answer("Введіть нову назву витрати:")
    await callback.answer()


@router.callback_query(F.data == "get_all_expenses")
async def handle_get_all_expenses(callback: CallbackQuery):
    response = requests.get("http://127.0.0.1:8000/expenses/")

    if response.status_code == 200:
        expenses = response.json()
        if not expenses:
            await callback.message.answer("💸 У вас ще немає витрат.")
        else:
            text = "📋 Всі витрати:\n\n"
            for exp in expenses:
                text += f"📅 {exp['date']}: {exp['category']} — {exp['amount_uah']} грн\n"
            await callback.message.answer(text)
    else:
        await callback.message.answer("⚠️ Помилка при завантаженні витрат.")

    await callback.answer()
