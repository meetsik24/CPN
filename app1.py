from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware

# Other imports remain the same...

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500/index.html"],  # Specify your allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define your endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate-cpn/")
async def generate_cpn(user_id: int = Form(...), amount: float = Form(...), status: str = Form(...)):
    # Your code to generate PCN and save to database
    # Assuming generate_pcn and insert_transaction are defined correctly
    transaction_id = ...  # Logic to get transaction ID
    pcn = generate_pcn(transaction_id)  # Generate PCN
    insert_transaction(user_id, amount, status)  # Insert into database
    return {"status": "success", "PCN": pcn, "amount": amount}


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