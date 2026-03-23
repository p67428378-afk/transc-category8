from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DateBase(BaseModel):
    date: datetime
    year: int
    month: int
    day: int
    quarter: int

class DateCreate(DateBase):
    pass

class Date(DateBase):
    date_id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    category_name: str
    parent_category_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    user_id: int
    date_id: int
    category_id: int
    merchant_name: str
    amount: float
    currency: str
    description: str
    cleaned_description: str
    llm_explanation: Optional[str] = None
    status: str = "processed"

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
