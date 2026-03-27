from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base # Import Base from database.py

class UserDimension(Base):
    __tablename__ = "user_dimension"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)

    transactions = relationship("TransactionFact", back_populates="user")

class DateDimension(Base):
    __tablename__ = "date_dimension"
    date_id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    quarter = Column(Integer)

    transactions = relationship("TransactionFact", back_populates="date")

class CategoryDimension(Base):
    __tablename__ = "category_dimension"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, index=True)
    parent_category_id = Column(Integer, ForeignKey("category_dimension.category_id"), nullable=True)

    parent_category = relationship("CategoryDimension", remote_side=[category_id])
    transactions = relationship("TransactionFact", back_populates="category")

class TransactionFact(Base):
    __tablename__ = "transactions_fact"
    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_dimension.user_id"))
    date_id = Column(Integer, ForeignKey("date_dimension.date_id"))
    category_id = Column(Integer, ForeignKey("category_dimension.category_id"))
    merchant_name = Column(String)
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    cleaned_description = Column(String)
    llm_explanation = Column(String, nullable=True)
    status = Column(String, default="processed")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("UserDimension", back_populates="transactions")
    date = relationship("DateDimension", back_populates="transactions")
    category = relationship("CategoryDimension", back_populates="transactions")
