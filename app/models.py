from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    mobile_number = Column(String(15))
    hashed_password = Column(String)
    expenses = relationship("Expense", back_populates="owner")

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="expenses")
    details = relationship("ExpenseDetail", back_populates="expense")




class ExpenseDetail(Base):
    __tablename__ = "expense_details"
    
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    amount_owed = Column(DECIMAL(10, 2))
    percentage = Column(DECIMAL(5, 2))

    expense = relationship("Expense", back_populates="details")
    user = relationship("User")
