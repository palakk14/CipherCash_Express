# backend/verification.py
from encryption import decrypt_data
from database import Database

db = Database()  # Assuming you have a Database instance

def verify_transfer_request(transaction_id, sender_account, recipient_account, amount, encrypted_data, transaction_key):
    # Retrieve the transaction from the database
    transaction = db.get_transaction_by_id(transaction_id)

    if not transaction:
        return False, 'Transaction not found'

    # Verify sender and recipient accounts
    if transaction['sender_account'] != sender_account or transaction['recipient_account'] != recipient_account:
        return False, 'Invalid sender or recipient account'

    # Verify the transaction amount
    if transaction['amount'] != amount:
        return False, 'Invalid transaction amount'

    # If all verifications pass, return True
    return True, 'Verification successful'
