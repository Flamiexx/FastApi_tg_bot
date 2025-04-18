from aiogram.fsm.state import StatesGroup, State


class AddExpense(StatesGroup):
    title = State()
    date = State()
    amount = State()
    description = State()


class GetReport(StatesGroup):
    start_date = State()
    end_date = State()
