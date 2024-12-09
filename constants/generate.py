import random

def generate_tx_id(username):
    # Get the first 4 characters of the username
    prefix = username[:4]
    
    # Generate a random 6-digit number
    random_number = random.randint(100000, 999999)
    
    # Create the tx_id
    tx_id = f"{prefix}#{random_number}"
    
    return tx_id
