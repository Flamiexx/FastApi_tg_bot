from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExpenseBase(BaseModel):
    amount_uah: float
    category: str
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    amount_usd: float
    usd_rate: float
    date: date

    class Config:
        orm_mode = True
