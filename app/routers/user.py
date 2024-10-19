from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  # Make sure to import List
from .. import crud, models, schemas
from ..database import get_db
from app.crud import get_user  # Implement this function to fetch user from DB
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.config.security import create_access_token, verify_password


router = APIRouter()

@router.post("/users/", response_model=schemas.User)  # Ensure response_model is defined
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return await crud.create_user(db=db, user=user)  # Use await here
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=form_data.username)
    if user:
        print(f"User found: {user.email}")
        if verify_password(form_data.password, user.hashed_password):
            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
    
    print("Invalid credentials")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
