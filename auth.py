import csv
import hashlib
from database import Database

db = Database()

def get_user_by_account_number(account_number):
    for user_account_number, user_data in db.accounts.items():
        if user_account_number == account_number:
            return {
                'account_name': user_data.get('account_name'),
                'account_number': user_account_number,
                'phone_number': user_data.get('phone_number'),
                'password': user_data.get('password')
            }

    return None

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def authenticate_user(account_name, account_number, phone_number, entered_password, request):
    user = get_user_by_account_number(account_number)

    if user and user['phone_number'] == phone_number:
        stored_password = user['password']

        entered_password_hashed = hash_password(entered_password)

        print(f"Stored Password: {stored_password}")
        print(f"Entered Password (Hashed): {entered_password_hashed}")

        if (stored_password== entered_password_hashed):
            return {'status': 'success', 'message': 'Authentication successful'}
        else:
            return {'status': 'error', 'message': 'Invalid password'}
    else:
        return {'status': 'error', 'message': 'User not present or invalid account number/phone number'}

if __name__ == "__main__":
    username = 'example_username'
    account_number = 'example_account_number'
    phone_number = 'example_phone_number'
    entered_password = 'example_password'

    authentication_result = authenticate_user(username, account_number, phone_number, entered_password, None)
    print(authentication_result)
