from sqlalchemy.orm import Session
from app.models import Expense as ExpenseModel
from app.schemas import ExpenseCreate, ExpenseMethod
from typing import List
from datetime import datetime


def create_expense(db: Session, expense: ExpenseCreate) -> ExpenseModel:
    if expense.method == ExpenseMethod.equal:
        total_amount = expense.amount
        number_of_participants = len(expense.details)
        equal_share = total_amount / number_of_participants

        for detail in expense.details:
            detail.amount_owed = equal_share  # Set the equal share for each participant

    elif expense.method == ExpenseMethod.exact:
        total_split = sum(detail.amount_owed for detail in expense.details if detail.amount_owed is not None)
        if total_split != expense.amount:
            raise ValueError("The total of exact amounts must equal the total expense amount.")

    elif expense.method == ExpenseMethod.percentage:
        total_percentage = sum(detail.percentage for detail in expense.details if detail.percentage is not None)
        if total_percentage != 100:
            raise ValueError("Percentages must add up to 100%.")

        for detail in expense.details:
            if detail.percentage is not None:
                detail.amount_owed = expense.amount * (detail.percentage / 100)

    db_expense = ExpenseModel(
        user_id=expense.user_id,
        amount=expense.amount,
        method=expense.method,
        description=expense.description,
         date=datetime.utcnow()
        
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_user_expenses(db: Session, user_id: int) -> List[ExpenseModel]:
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == user_id).all()

def get_all_expenses(db: Session) -> List[ExpenseModel]:
    return db.query(ExpenseModel).all()
