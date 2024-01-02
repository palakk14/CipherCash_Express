# backend/consistency_checks.py

def is_transaction_id_used_before(transaction_id, previous_transactions):
    # Check if the transaction ID has been used before
    return any(transaction['id'] == transaction_id for transaction in previous_transactions)

def has_sufficient_funds(sender_account_balance, transaction_amount):
    # Check if the sender has sufficient funds for the transaction
    return sender_account_balance >= transaction_amount

def perform_consistency_checks(transaction, previous_transactions, sender_account_balance):
    # Consistency checks result
    consistency_checks_result = {'status': 'success', 'message': ''}

    #Verify that the transaction ID is unique
    if is_transaction_id_used_before(transaction['id'], previous_transactions):
        consistency_checks_result['status'] = 'error'
        consistency_checks_result['message'] = 'Duplicate transaction ID'

    # Verify that the sender and recipient accounts are different
    if transaction['sender_account'] == transaction['recipient_account']:
        consistency_checks_result['status'] = 'error'
        consistency_checks_result['message'] = 'Sender and recipient accounts are the same'

    # Check for sufficient funds in the sender's account
    if not has_sufficient_funds(sender_account_balance, transaction['amount']):
        consistency_checks_result['status'] = 'error'
        consistency_checks_result['message'] = 'Insufficient funds in the sender\'s account'

    

    return consistency_checks_result

