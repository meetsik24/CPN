# app.py

from fastapi import FastAPI, HTTPException
from db_sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string

# Database URL configuration
#DATABASE_URL = "postgresql+asyncpg://username:password@localhost/mydatabase"  # For PostgreSQL
DATABASE_URL = "mysql+aiomysql://username:password@localhost/cpn_101"  # For MySQL

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define the Payment_Transactions model
class PaymentTransaction(Base):
    __tablename__ = "Payment_Transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    PCN = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create the table
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Updated PCN generation function
def generate_pcn(transaction_id):
    system_identifier = "SIK-CPN"  # Updated identifier
    date_str = datetime.now().strftime("%Y%m%d")
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    pcn = f"{system_identifier}-{transaction_id}-{date_str}-{random_string}"
    return pcn

# Function to insert a transaction
async def insert_transaction(user_id: int, amount: float, status: str):
    transaction_id = session.query(PaymentTransaction).count() + 1  # Simple way to generate a transaction ID
    pcn = generate_pcn(transaction_id)
    
    new_transaction = PaymentTransaction(
        user_id=user_id,
        amount=amount,
        status=status,
        PCN=pcn
    )

    session.add(new_transaction)
    session.commit()
    return pcn

@app.post("/api/payments/")
async def create_payment(user_id: int, amount: float):
    if not user_id or amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid input data.")
    
    status = "Pending"
    pcn = await insert_transaction(user_id, amount, status)  # Call the insert function
    return {"message": "Payment created successfully", "PCN": pcn}

# Function to start the session
def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Start the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)