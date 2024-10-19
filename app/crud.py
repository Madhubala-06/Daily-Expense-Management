from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas, models  # Ensure these imports are correct
from app.models import Expense, ExpenseDetail
from app.config.security import hash_password, verify_password  
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas import ExpenseCreate, ExpenseMethod

async def create_user(db: Session, user: schemas.UserCreate):
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    # Proceed to create a new user
    hashed_password = hash_password(user.password)  # Hash the password using your hashing function
    db_user = models.User(
        email=user.email,
        name=user.name,
        mobile_number=user.mobile_number,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    
    try:
        db.commit()  # Commit the new user to the database
        db.refresh(db_user)  # Refresh the instance to get the generated state
        return db_user  # Return the newly created user
    except IntegrityError as e:
        db.rollback()  # Rollback the session on error
        # Check if the error is related to unique constraints
        if 'UNIQUE constraint failed' in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user. Email might already exist."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user due to an unexpected error."
            )
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()  # Fetch by email


def add_expense(db: Session, expense: ExpenseCreate):
    # Validate the expense method using the enum
    if expense.method not in ExpenseMethod:
        raise ValueError("Invalid expense splitting method")

    # Create the expense entry
    db_expense = Expense(
        user_id=expense.user_id,
        amount=expense.amount,
        method=expense.method.value,
        description=expense.description
    )

    db.add(db_expense)

    try:
        db.commit()  # Commit the expense first
        db.refresh(db_expense)  # Refresh to get the generated ID

        # Handling different methods of expense splitting
        if expense.method == ExpenseMethod.equal:
            # Split equally among all participants
            num_participants = len(expense.details)
            if num_participants == 0:
                raise ValueError("At least one participant is required for equal splitting.")

            split_amount = expense.amount / num_participants

            for detail in expense.details:
                db_detail = ExpenseDetail(
                    expense_id=db_expense.id,
                    user_id=detail.user_id,
                    amount_owed=split_amount,
                    percentage=(100 / num_participants)  # Each participant owes equal percentage
                )
                db.add(db_detail)

        elif expense.method == ExpenseMethod.exact:
            # Exact amounts specified for each participant
            for detail in expense.details:
                if detail.amount_owed is None:
                    raise ValueError(f"Amount owed must be specified for user {detail.user_id}")

                db_detail = ExpenseDetail(
                    expense_id=db_expense.id,
                    user_id=detail.user_id,
                    amount_owed=detail.amount_owed,
                    percentage=(detail.amount_owed / expense.amount) * 100  # Calculate the percentage
                )
                db.add(db_detail)

        elif expense.method == ExpenseMethod.percentage:
            total_percentage = sum(detail.percentage for detail in expense.details)
            if total_percentage != 100:
                raise ValueError("Percentages must sum up to 100.")

            for detail in expense.details:
                if detail.percentage is None:
                    raise ValueError(f"Percentage owed must be specified for user {detail.user_id}")

                amount_owed = (detail.percentage / 100) * expense.amount

                db_detail = ExpenseDetail(
                    expense_id=db_expense.id,
                    user_id=detail.user_id,
                    amount_owed=amount_owed,
                    percentage=detail.percentage,
                )
                db.add(db_detail)

        db.commit()  # Commit all details after processing
    except ValueError as e:
        db.rollback()  # Rollback on error
        raise e  # Reraise the exception for handling upstream
    except Exception as e:
        db.rollback()  # Rollback on any unexpected error
        raise ValueError("An unexpected error occurred while adding expense details.") from e

    return db_expense


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_expenses(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()


def get_all_expenses(db: Session):
    return db.query(models.Expense).all()
