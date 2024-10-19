# from pydantic import BaseModel, EmailStr, validator, Field
# from enum import Enum
# from typing import List, Union

# class ExpenseMethod(str, Enum):
#     equal = "equal"
#     exact = "exact"
#     percentage = "percentage"

# class UserCreate(BaseModel):
#     """
#     Model for creating a new user.
#     """
#     email: EmailStr
#     name: str  # Standard string type
#     mobile_number: str  # Standard string type

#     @validator("mobile_number")
#     def validate_mobile_number(cls, value):
#         if not value.isdigit() or not (10 <= len(value) <= 15):
#             raise ValueError("Mobile number must contain only digits and be between 10 to 15 digits long.")
#         return value

# class User(UserCreate):
#     """
#     Model representing an existing user with an ID.
#     """
#     id: int

#     class Config:
#         orm_mode = True

# class ExpenseCreate(BaseModel):
#     """
#     Model for creating a new expense.
#     """
#     user_id: int
#     amount: float  # Using float instead of condecimal
#     method: ExpenseMethod
#     split_details: List[Union[float, int]]  # List of amounts or percentages for each participant

#     @validator("amount")
#     def validate_amount(cls, value):
#         if value <= 0:
#             raise ValueError("Amount must be greater than 0.")
#         return value

#     @validator("split_details")
#     def validate_split_details(cls, value, values):
#         if not value:
#             raise ValueError("Split details cannot be empty.")

#         method = values.get('method')
#         if method == ExpenseMethod.equal and len(value) < 2:
#             raise ValueError("For 'equal' method, at least two participants are required.")

#         if method == ExpenseMethod.exact:
#             total_exact = sum(value)
#             if total_exact != values['amount']:
#                 raise ValueError("The total of exact amounts must equal the total expense amount.")

#         if method == ExpenseMethod.percentage:
#             total_percentage = sum(value)
#             if total_percentage != 100:
#                 raise ValueError("Percentages must add up to 100%.")

#         return value

# class Expense(ExpenseCreate):
#     """
#     Model representing an existing expense with an ID.
#     """
#     id: int

#     class Config:
#         orm_mode = True


from pydantic import BaseModel, EmailStr, validator, root_validator
from enum import Enum
from typing import List, Union

class ExpenseMethod(str, Enum):
    equal = "equal"
    exact = "exact"
    percentage = "percentage"

class UserCreate(BaseModel):
    """
    Model for creating a new user.
    """
    email: EmailStr
    name: str  # Standard string type
    mobile_number: str  # Standard string type

    @validator("mobile_number")
    def validate_mobile_number(cls, value):
        if not value.isdigit() or not (10 <= len(value) <= 15):
            raise ValueError("Mobile number must contain only digits and be between 10 to 15 digits long.")
        return value

class User(UserCreate):
    """
    Model representing an existing user with an ID.
    """
    id: int

    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    """
    Model for creating a new expense.
    """
    user_id: int
    amount: float  # Using float instead of condecimal
    method: ExpenseMethod
    split_details: List[Union[float, int]]  # List of amounts or percentages for each participant

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0.")
        return value

    @root_validator(pre=False)
    def validate_split_details(cls, values):
        split_details = values.get('split_details')
        method = values.get('method')
        amount = values.get('amount')

        if not split_details:
            raise ValueError("Split details cannot be empty.")

        if method == ExpenseMethod.equal and len(split_details) < 2:
            raise ValueError("For 'equal' method, at least two participants are required.")

        if method == ExpenseMethod.exact:
            total_exact = sum(split_details)
            if total_exact != amount:
                raise ValueError("The total of exact amounts must equal the total expense amount.")

        if method == ExpenseMethod.percentage:
            total_percentage = sum(split_details)
            if total_percentage != 100:
                raise ValueError("Percentages must add up to 100%.")

        return values

class Expense(ExpenseCreate):
    """
    Model representing an existing expense with an ID.
    """
    id: int

    class Config:
        orm_mode = True
