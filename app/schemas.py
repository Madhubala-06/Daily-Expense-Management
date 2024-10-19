from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from decimal import Decimal

class UserCreate(BaseModel):
    email: str
    name: str
    mobile_number: str
    password: str 

class User(BaseModel):
    id: int
    email: str
    name: str
    mobile_number: str

    class Config:
        from_attributes = True

class ExpenseMethod(str, Enum):
    equal = "equal"
    exact = "exact"
    percentage = "percentage"

class ExpenseDetailCreate(BaseModel):
    user_id: int
    amount_owed: Optional[Decimal] = None  
    percentage: Optional[float] = None    

class ExpenseCreate(BaseModel):
    user_id: int
    amount: Decimal 
    method: ExpenseMethod
    description: str
    details: List[ExpenseDetailCreate]  

class Expense(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    method: ExpenseMethod
    description: str  

    class Config:
        orm_mode = True 

class ExpenseOut(BaseModel):
    id: int
    amount: Decimal
    method: ExpenseMethod
    description: str

    class Config:
        from_attributes = True

class BalanceSheetEntry(BaseModel):
    user_id: int
    user_name: str
    total_expense: Decimal
    individual_expenses: List[ExpenseOut]

    class Config:
        from_attributes = True  
