from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from typing import List
import csv
from fastapi.responses import StreamingResponse
from io import StringIO
from decimal import Decimal

router = APIRouter()

@router.get("/balance_sheet/", response_model=List[schemas.BalanceSheetEntry])
def get_balance_sheet(db: Session = Depends(get_db)):
    # Fetch total expenses per user using a single query
    result = (
        db.query(models.User.id, models.User.name, func.sum(models.Expense.amount).label("total_expense"))
        .join(models.Expense, models.Expense.user_id == models.User.id)
        .group_by(models.User.id, models.User.name)
        .all()
    )

    balance_sheet_data = []

    for row in result:
        user_expenses = db.query(models.Expense).filter(models.Expense.user_id == row.id).all()
        balance_sheet_data.append(schemas.BalanceSheetEntry(
            user_id=row.id,
            user_name=row.name,
            total_expense=Decimal(str(row.total_expense)),  # Convert to Decimal
            individual_expenses=[schemas.ExpenseOut.from_orm(expense) for expense in user_expenses]
        ))

    return balance_sheet_data
@router.get("/download_balance_sheet/")
def download_balance_sheet(db: Session = Depends(get_db)):
    # Fetch all users and expenses
    users = crud.get_all_users(db)
    expenses = crud.get_all_expenses(db)

    # Prepare CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["User ID", "User Name", "Total Expense", "Expense ID", "Amount", "Method", "Description"])

    for user in users:
        user_expenses = [expense for expense in expenses if expense.user_id == user.id]
        user_total_expense = sum(expense.amount for expense in user_expenses)

        for expense in user_expenses:
            # Convert the method string to the corresponding Enum value
            expense_method = schemas.ExpenseMethod(expense.method)
            writer.writerow([
                user.id, 
                user.name, 
                user_total_expense, 
                expense.id, 
                expense.amount, 
                expense_method.value,  
                expense.description
            ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=balance_sheet.csv"})