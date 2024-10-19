from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from app.auth.auth import get_current_user
from typing import List  # Import List from typing

router = APIRouter()

@router.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.add_expense(db=db, expense=expense)

@router.get("/expenses/user/{user_id}", response_model=List[schemas.Expense])
def read_expenses_by_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)  # Ensure user is logged in
):
    # Check if current_user has permission to access user_id's expenses
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user's expenses."
        )

    # Fetch and return the expenses for the specified user
    return crud.get_user_expenses(db=db, user_id=user_id)

@router.get("/expenses/", response_model=List[schemas.Expense])
async def read_user_expenses(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)  # Ensure user is logged in
):
    return crud.get_user_expenses(db=db, user_id=current_user.id)  # Retrieve expenses for the current user

@router.get("/expenses/", response_model=List[schemas.Expense])
def read_all_expenses(db: Session = Depends(get_db)):
    return crud.get_all_expenses(db=db)



