# Automated Transaction Categorization System

This project implements an automated system to categorize bank transactions using an LLM-based engine, an ETL pipeline, a FastAPI backend, and a PostgreSQL database.

## Features

- **Transaction Data Upload:** Upload raw bank transaction data in CSV format.
- **LLM-based Categorization:** Automatic categorization of transactions using a Large Language Model.
- **ETL Pipeline:** Data cleaning, standardization, deduplication, and loading into an optimized SQL schema.
- **Backend API:** RESTful API for data ingestion and reporting.
- **Star Schema Database:** Optimized PostgreSQL database for analytical queries.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/transc-category8.git
    cd transc-category8
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Database Setup:**
    -   Ensure you have a PostgreSQL database running.
    -   Set the `DATABASE_URL` environment variable. Example:
        ```
        export DATABASE_URL="postgresql://user:password@localhost/transaction_db"
        ```
        (You can also create a `.env` file in the project root with this variable).

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

    The API documentation will be available at `http://127.0.0.1:8000/docs`.

## Project Structure

```
.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── etl.py
├── llm_categorizer.py
├── requirements.txt
└── README.md
```

## API Endpoints

-   `POST /users/`: Register a new user.
-   `POST /upload-transactions/{user_email}`: Upload a CSV file with transaction data for a specific user.
-   `GET /transactions/{user_id}`: Retrieve categorized transactions for a user.

## Next Steps

-   Implement actual LLM integration in `llm_categorizer.py`.
-   Develop the frontend dashboard.
-   Add comprehensive testing.
-   Implement authentication and authorization.
