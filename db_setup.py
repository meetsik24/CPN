from db_sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
import string

# Define the database URL
#DATABASE_URL = 'postgresql://username:password@localhost:5432/mydatabase'  # For PostgreSQL#
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

# Define the Payment_Transactions model
class PaymentTransaction(Base):
    __tablename__ = 'Payment_Transactions'
    __table_args__ = {'extend_existing': True} 
    
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

# Function to insert a transaction
def insert_transaction(user_id, amount, status):
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
        print(f"Transaction inserted: PCN = {pcn}, Amount = {amount}")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()  # Close the session after the operation

# Example usage
insert_transaction(user_id=123, amount=5000.00, status='Pending')