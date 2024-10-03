Here’s the `README.md` file in one block for easy copying:

```markdown
# Payment Control Number System with FastAPI and Zenopay Integration

This project demonstrates the implementation of a **Payment Control Number (PCN) System** using **FastAPI** and integrates with the **Zenopay payment gateway** for processing payments.

## Features
- **FastAPI backend** with database support (MySQL or PostgreSQL).
- **Payment Control Number (PCN)** generation for each transaction.
- Integration with **Zenopay** for handling payments.
- Webhook handling for payment confirmation.

## Prerequisites
- Python 3.8+
- MySQL or PostgreSQL database
- Zenopay API credentials (API Key and Secret Key)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/control-number-system.git
cd control-number-system
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root of your project to store sensitive information like the database URL and Zenopay API credentials.
```bash
DATABASE_URL=mysql+pymysql://username:password@localhost/cpn_101
ZENOPAY_API_KEY=your_zenopay_api_key
ZENOPAY_SECRET_KEY=your_zenopay_secret_key
```

### 5. Set Up the Database
Make sure your database is running (MySQL or PostgreSQL). Create a database called `cpn_101` (or modify the `DATABASE_URL` to match your setup).

You can create the tables by running:
```bash
python db_setup.py
```

### 6. Running the Application
Start the FastAPI app using Uvicorn:
```bash
uvicorn app:app --reload
```
The app will now be running on `http://127.0.0.1:8000/`.

### 7. Zenopay Integration
You can create a payment request via the `/create-zenopay-payment/` endpoint.

**Example Request:**
```bash
POST /create-zenopay-payment/
{
  "amount": 5000,
  "currency": "TZS",
  "customer_email": "customer@example.com"
}
```

The Zenopay webhook is handled at `/zenopay-webhook/`.

## Folder Structure
```
.
├── app.py                    # Main FastAPI application
├── db_setup.py               # Database setup and PCN generation
├── zenopay_integration.py     # Zenopay integration logic
├── requirements.txt           # Python dependencies
├── README.md                  # Project README
└── .env                       # Environment variables (not included in repo)
```

## Dependencies
- **FastAPI**: Web framework for building APIs.
- **SQLAlchemy**: ORM for handling database interactions.
- **Zenopay**: Payment gateway for processing payments.
- **Uvicorn**: ASGI server for running the FastAPI app.
- **Requests**: HTTP library for sending requests to Zenopay API.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Feel free to fork this repository and contribute via pull requests. Make sure to add unit tests for any new features.

## Contact
For any inquiries or issues, please contact [your_email@example.com](mailto:your_email@example.com).
```

This single block includes everything in a well-structured format for your GitHub repository.
