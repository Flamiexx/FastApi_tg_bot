from sqlalchemy.orm import Session
from . import models, schemas
from .currency import get_usd_rate
from .unils import convert_to_usd


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    usd_rate = get_usd_rate()
    db_expense = models.Expense(
        amount_uah=expense.amount_uah,
        amount_usd=round(expense.amount_uah / usd_rate, 2),
        usd_rate=usd_rate,
        category=expense.category,
        description=expense.description,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, start_date=None, end_date=None):
    query = db.query(models.Expense)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    return query.order_by(models.Expense.date.desc()).all()


def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None
    db.delete(expense)
    db.commit()
    return expense


def update_expense(db: Session, expense_id: int, expense_data: schemas.ExpenseCreate):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None
    expense.amount_uah = expense_data.amount_uah
    usd_rate = get_usd_rate()
    expense.amount_usd = round(expense_data.amount_uah / usd_rate, 2)
    expense.usd_rate = usd_rate
    expense.category = expense_data.category
    expense.description = expense_data.description
    db.commit()
    db.refresh(expense)
    return expense
