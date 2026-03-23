from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from io import StringIO

from database import SessionLocal, engine, Base, get_db
from models import UserDimension, DateDimension, CategoryDimension, TransactionFact
from schemas import User, UserCreate, Transaction
from crud import create_user, get_user_by_email, get_transactions_by_user
from etl import process_csv_data

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Create database tables on startup (for development purposes)
    Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already registered")
    return create_user(db=db, user=user)

@app.post("/upload-transactions/{user_email}")
def upload_transactions(user_email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        csv_contents = StringIO(file.file.read().decode("utf-8"))
        processed_count = process_csv_data(db, user_email, csv_contents.read())
        return {"message": f"Successfully processed {processed_count} transactions for {user_email}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {e}")

@app.get("/transactions/{user_id}", response_model=List[Transaction])
def get_user_transactions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = get_transactions_by_user(db, user_id, skip=skip, limit=limit)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")
    return transactions
