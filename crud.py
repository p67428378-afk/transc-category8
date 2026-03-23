from sqlalchemy.orm import Session
from datetime import datetime
from models import UserDimension, DateDimension, CategoryDimension, TransactionFact
from schemas import UserCreate, CategoryCreate, TransactionCreate

def get_user(db: Session, user_id: int):
    return db.query(UserDimension).filter(UserDimension.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserDimension).filter(UserDimension.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = UserDimension(username=user.username, email=user.email, created_at=datetime.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_date(db: Session, date: datetime):
    return db.query(DateDimension).filter(DateDimension.date == date).first()

def create_date(db: Session, date: datetime):
    db_date = DateDimension(date=date, year=date.year, month=date.month, day=date.day, quarter=(date.month - 1) // 3 + 1)
    db.add(db_date)
    db.commit()
    db.refresh(db_date)
    return db_date

def get_category(db: Session, category_id: int):
    return db.query(CategoryDimension).filter(CategoryDimension.category_id == category_id).first()

def get_category_by_name(db: Session, category_name: str):
    return db.query(CategoryDimension).filter(CategoryDimension.category_name == category_name).first()

def create_category(db: Session, category: CategoryCreate):
    db_category = CategoryDimension(category_name=category.category_name, parent_category_id=category.parent_category_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_transaction(db: Session, transaction_id: int):
    return db.query(TransactionFact).filter(TransactionFact.transaction_id == transaction_id).first()

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = TransactionFact(
        user_id=transaction.user_id,
        date_id=transaction.date_id,
        category_id=transaction.category_id,
        merchant_name=transaction.merchant_name,
        amount=transaction.amount,
        currency=transaction.currency,
        description=transaction.description,
        cleaned_description=transaction.cleaned_description,
        llm_explanation=transaction.llm_explanation,
        status=transaction.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(TransactionFact).filter(TransactionFact.user_id == user_id).offset(skip).limit(limit).all()
