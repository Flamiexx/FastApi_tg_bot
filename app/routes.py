from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from . import crud, schemas
from .database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@router.get("/expenses/", response_model=list[schemas.Expense])
def get_expenses(
    start_date: date = Query(None, description="From: (YYYY-MM-DD)"),
    end_date: date = Query(None, description="To: (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    return crud.get_expenses(db, start_date, end_date)


@router.delete("/expenses/{expense_id}", response_model=schemas.Expense)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted_expense = crud.delete_expense(db, expense_id)
    if not deleted_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted_expense


@router.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense_update: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    updated_expense = crud.update_expense(db, expense_id, expense_update)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense


