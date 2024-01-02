# main.py
from flask import Flask, render_template, request, redirect, url_for, jsonify

from auth import authenticate_user
from consistency_checks import perform_consistency_checks
from database import Database  
from encryption import encrypt_data

app = Flask(__name__)
db = Database() 

# Route for the home page where the user enters their information
@app.route('/', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        sender_account_name = request.form.get('sender_account_name')
        sender_account_number = request.form.get('sender_account_number')
        sender_phone_number = request.form.get('sender_phone_number')
        password = request.form.get('password')

        print(f"Received form data - Account Name: {sender_account_name}, Account Number: {sender_account_number}, Phone Number: {sender_phone_number}")

        # Authenticate the user
        authentication_result = authenticate_user(sender_account_name, sender_account_number, sender_phone_number, password, request)

        if authentication_result['status'] == 'success':
            # User authenticated successfully, redirect to the transfer form
            return redirect(url_for('transfer_form'))
        else:
            # Authentication failed, show error message
            return render_template('index.html', error_message=authentication_result['message'])

    # Render the home page
    return render_template('index.html')

# Route for the transfer form where the user enters recipient information
@app.route('/transfer_form', methods=['GET', 'POST'])
def transfer_form():
    if request.method == 'POST':
        recipient_account_number = request.form.get('recipient_account')

        # Check if the recipient account exists
        if recipient_account_number not in db.account_numbers:
            return render_template('transfer_form.html', error_message='Recipient account does not exist')

        # Render the page for entering the transfer amount
        return render_template('transfer_amount.html', recipient_account=recipient_account_number)

    # Render the fund transfer form
    return render_template('transfer_form.html')

# Route for handling the actual fund transfer
@app.route('/transfer', methods=['POST'])
def transfer():
    if request.method == 'POST':
        sender_account_number = request.form.get('sender_account_number')
        recipient_account_number = request.form.get('recipient_account_number')
        amount = float(request.form.get('amount'))
        phone_number = request.form.get('phone_number')

        # Validate accounts and amount
        
        if amount <= 0 or amount > db.get_balance_by_account_number(sender_account_number):
            return jsonify({'status': 'error', 'message': 'Invalid amount or insufficient funds'})

        # Validate provided phone number against the associated account
        

        # Use DES encryption on sensitive data
        sensitive_data = f"{sender_account_number}-{recipient_account_number}-{amount}"
        encryption_key = db.generate_transaction_key()  # Use transaction-specific key
        encrypted_data = encrypt_data(sensitive_data, encryption_key) 

        # Consistency checks
        sender_account_balance = db.get_balance_by_account_number(sender_account_number)
        transaction = {
            'id': db.generate_transaction_key(),  # Generate a unique transaction ID
            'sender_account': sender_account_number,
            'recipient_account': recipient_account_number,
            'amount': amount
            # Add other transaction details if needed
        }
        consistency_checks_result = perform_consistency_checks(transaction, db.transactions, sender_account_balance)

        if consistency_checks_result['status'] == 'error':
            return jsonify({'status': 'error', 'message': consistency_checks_result['message']})

        # If consistency checks pass, proceed with the fund transfer logic
        # Update balances and record the transaction
        print(f"Before balance update - Sender's Balance: {db.get_balance_by_account_number(sender_account_number)}")
        print(f"Before balance update - Recipient's Balance: {db.get_balance_by_account_number(recipient_account_number)}")
        db.update_balance_by_account_number(sender_account_number, -amount)
        db.update_balance_by_account_number(recipient_account_number, amount)
        print(f"After balance update - Sender's Balance: {db.get_balance_by_account_number(sender_account_number)}")
        print(f"After balance update - Recipient's Balance: {db.get_balance_by_account_number(recipient_account_number)}")

        transaction_id = db.add_transaction_by_account_number(sender_account_number, recipient_account_number, amount, encrypted_data)

        # Save the transaction to the transactions CSV file
        transaction = db.get_transaction_by_id(transaction_id)
        if transaction:
            db.save_transaction(transaction)

        # Return transaction ID in the response
        return jsonify({'status': 'success', 'message': 'Transfer successful!', 'transaction_id': transaction_id})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request'})

if __name__ == "__main__":
    app.run(debug=True)
