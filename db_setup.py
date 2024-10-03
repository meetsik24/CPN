from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string

# Define the database URL
DATABASE_URL = 'mysql+pymysql://new_user:password@localhost/cpn_101'  # For MySQL

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Payment_Transactions model
class PaymentTransaction(Base):
    __tablename__ = 'Payment_Transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    PCN = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)

# Function to generate PCN
def generate_pcn(transaction_id):
    system_identifier = "SIK-CPN"
    date_str = datetime.now().strftime("%Y%m%d")
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    pcn = f"{system_identifier}-{transaction_id}-{date_str}-{random_string}"
    return pcn

# Create the FastAPI app
app = FastAPI()

# Endpoint to insert a transaction
@app.post("/insert-transaction/")
async def insert_transaction(user_id: int = Form(...), amount: float = Form(...), status: str = Form(...)):
    session = Session()  # Create a new session
    transaction_id = session.query(PaymentTransaction).count() + 1  # Simple way to generate a transaction ID
    pcn = generate_pcn(transaction_id)  # Generate PCN
    
    try:
        new_transaction = PaymentTransaction(
            user_id=user_id,
            amount=amount,
            status=status,
            PCN=pcn
        )
        
        session.add(new_transaction)
        session.commit()
        return {"status": "success", "PCN": pcn, "amount": amount}
    except Exception as e:
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()  # Close the session after the operation

# Endpoint to serve HTML form
@app.get("/", response_class=HTMLResponse)
async def read_form():
    html_content = """
    <html>
        <head>
            <title>Payment Control Number Generator</title>
        </head>
        <body>
            <h1>Generate Payment Control Number</h1>
            <form action="/insert-transaction/" method="post">
                <label for="user_id">User ID:</label>
                <input type="number" name="user_id" required><br>
                <label for="amount">Amount:</label>
                <input type="text" name="amount" required><br>
                <label for="status">Status:</label>
                <input type="text" name="status" required><br>
                <button type="submit">Generate PCN</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)