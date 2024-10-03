import random
import string
from datetime import datetime

def generate_pcn(transaction_id):
    # System identifier
    system_identifier = "INV"
    
    # Current date in YYYYMMDD format
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Generate a random string (4 characters long)
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # Combine all parts to form the PCN
    pcn = f"{system_identifier}-{transaction_id}-{date_str}-{random_string}"
    
    return pcn

# Example usage
transaction_id = 1001
pcn = generate_pcn(transaction_id)
print(f"Generated PCN: {pcn}")