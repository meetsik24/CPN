import requests
from fastapi import HTTPException

ZENOPAY_API_KEY = "your_zenopay_api_key"
ZENOPAY_SECRET_KEY = "your_zenopay_secret_key"
ZENOPAY_BASE_URL = "https://api.zenopay.com"  # Adjust this to Zenopay’s actual API URL

# Function to create a Zenopay payment
def create_zenopay_payment(amount: float, currency: str = "TZS", customer_email: str = "user@example.com"):
    try:
        url = f"{ZENOPAY_BASE_URL}/create-payment"
        headers = {
            "Authorization": f"Bearer {ZENOPAY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "currency": currency,
            "customer_email": customer_email,
            "redirect_url": "https://your-website.com/callback",  # Your callback URL
            "payment_method": "card"  # Adjust as needed
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Payment request failed")

        return {"payment_link": response_data.get("payment_link", "https://zenopay.com/fallback")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to handle Zenopay webhook
async def zenopay_webhook(payload: dict):
    try:
        event_type = payload.get("event")
        if event_type == "payment.success":
            payment_data = payload.get("data", {})
            print(f"Payment succeeded for: {payment_data['amount']}")
            # Update your database or transaction record here

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")