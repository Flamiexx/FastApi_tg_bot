from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Додати витрату", callback_data="add_expense")],
        [InlineKeyboardButton(text="📄 Отримати звіт", callback_data="get_report")],
        [InlineKeyboardButton(text="📋 Всі витрати", callback_data="get_all_expenses")],
        [InlineKeyboardButton(text="❌ Видалити витрату", callback_data="delete_expense")],
        [InlineKeyboardButton(text="✏️ Редагувати витрату", callback_data="edit_expense")],
    ])
