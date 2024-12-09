import uuid

def generate_transaction_tx():
    try:
        transaction_id = str(uuid.uuid4())
        reference_id = str(uuid.uuid4())
        return transaction_id, reference_id
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")