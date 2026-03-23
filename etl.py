import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from datetime import datetime
from models import UserDimension, DateDimension, CategoryDimension, TransactionFact
from schemas import UserCreate, CategoryCreate, TransactionCreate # Import schemas
from crud import get_user_by_email, create_user, get_date, create_date, get_category_by_name, create_category, create_transaction

def process_csv_data(db: Session, user_email: str, csv_data: str):
    # 1. Extract
    df = pd.read_csv(StringIO(csv_data))

    # Basic data cleaning and standardization (Transform)
    # Assuming CSV has columns: 'Date', 'Description', 'Amount', 'Currency', 'Merchant'
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    # Ensure required columns exist
    required_columns = ['date', 'description', 'amount', 'currency', 'merchant']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV is missing required columns. Expected: {required_columns}, Found: {df.columns.tolist()}")

    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])

    # Deduplication (simple example: based on date, description, amount, merchant)
    df.drop_duplicates(subset=['date', 'description', 'amount', 'merchant'], inplace=True)

    # Get or create user
    user = get_user_by_email(db, user_email)
    if not user:
        user_create_data = UserCreate(username=user_email.split('@')[0], email=user_email)
        user = create_user(db, user_create_data)

    # Process each row
    transactions_to_create = []
    for index, row in df.iterrows():
        # Get or create date dimension
        date_obj = row['date'].to_pydatetime()
        db_date = get_date(db, date_obj)
        if not db_date:
            db_date = create_date(db, date_obj)

        # Placeholder for categorization (will be replaced by LLM)
        # For now, assign a default category or try to infer a simple one
        category_name = "Uncategorized"
        if "starbucks" in row['description'].lower():
            category_name = "Food & Drink"
        elif "rent" in row['description'].lower():
            category_name = "Housing"

        db_category = get_category_by_name(db, category_name)
        if not db_category:
            category_create_data = CategoryCreate(category_name=category_name)
            db_category = create_category(db, category_create_data)

        # Create transaction fact
        transaction_create_data = TransactionCreate(
            user_id=user.user_id,
            date_id=db_date.date_id,
            category_id=db_category.category_id,
            merchant_name=row['merchant'],
            amount=row['amount'],
            currency=row['currency'],
            description=row['description'],
            cleaned_description=row['description'], # For now, same as description
            llm_explanation=None,
            status='processed'
        )
        transactions_to_create.append(transaction_create_data)

    # Load transactions
    for t_data in transactions_to_create:
        create_transaction(db, t_data)

    db.commit()
    return len(transactions_to_create)
