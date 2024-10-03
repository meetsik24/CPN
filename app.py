from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string
from fastapi.middleware.cors import CORSMiddleware

# Define the database URL
DATABASE_URL = 'mysql+pymysql://new_user:password@localhost/cpn_101'  # Update with your actual database credentials

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the Payment_Transactions model
class PaymentTransaction(Base):
    __tablename__ = 'Payment_Transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='Pending')  # Default value for status
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Adjust to your front-end server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to insert a transaction
@app.post("/insert-transaction/")
async def insert_transaction(user_id: int = Form(...), amount: float = Form(...)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be a positive number")

    session = Session()  # Create a new session
    transaction_id = session.query(PaymentTransaction).count() + 1  # Simple way to generate a transaction ID
    pcn = generate_pcn(transaction_id)  # Generate PCN
    
    try:
        new_transaction = PaymentTransaction(
            user_id=user_id,
            amount=amount,
            status='Pending',  # Set default status
            PCN=pcn
        )
        
        session.add(new_transaction)
        session.commit()
        
        # Prepare HTML response with results
        result_html = f"""
        <html>
            <head>
                <title>PCN Generated</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <h1 class="text-center">Payment Control Number Generated</h1>
                    <div class="alert alert-success text-center">
                        <p><strong>PCN:</strong> {pcn}</p>
                        <p><strong>Amount:</strong> {amount}</p>
                        <p><strong>User ID:</strong> {user_id}</p>
                        <a href="/" class="btn btn-primary">Generate Another PCN</a>
                    </div>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=result_html)
    
    except Exception as e:
        session.rollback()
        return HTMLResponse(content=f"<p>Error: {str(e)}</p>", status_code=500)
    
    finally:
        session.close()  # Close the session after the operation

# Endpoint to serve HTML form
@app.get("/", response_class=HTMLResponse)
async def read_form():
    html_content = """
    <html>
        <head>
            <title>Payment Control Number Generator</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="text-center">Generate Payment Control Number (CPN)</h1>
                <div class="row justify-content-center mt-4">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <form action="/insert-transaction/" method="post">
                                    <input type="number" name="user_id" placeholder="User ID" required>
                                    <input type="number" step="0.01" name="amount" placeholder="Amount" required>
                                    <button type="submit">Generate PCN</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Start the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)