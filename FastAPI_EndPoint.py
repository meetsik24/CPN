from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
import string

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your function to generate a CPN
def generate_pcn(transaction_id):
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SIK-CPN-{timestamp}-{random_string}-{transaction_id}"

@app.post("/generate-cpn/")
async def generate_cpn(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    if not user_id or not amount:
        return {"status": "error", "message": "Invalid data. User ID and amount are required."}

    # Simulate creating a transaction and generating a PCN
    transaction_id = random.randint(1000, 9999)  # Example of how you could generate a unique transaction ID
    pcn = generate_pcn(transaction_id)

    # Return the generated PCN
    return {
        "status": "success",
        "PCN": pcn
    }