import csv
import os
from utils import generate_random_key

class Database:
    def __init__(self, accounts_csv='accounts.csv', transactions_csv='transactions.csv'):
        # Initialize or load data from the CSV files
        self.accounts = {}
        self.account_numbers = set()
        self.transactions = []
        self.accounts_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), accounts_csv)
        self.transactions_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), transactions_csv)
        self.load_data()

    def get_user_by_username(self, account_name):
        for account_number, user_data in self.accounts.items():
            if user_data.get('account_name') == account_name:
                return {
                    'account_name': user_data['account_name'],
                    'account_number': account_number,
                    'phone_number': user_data.get('phone_number'),
                    'password': user_data.get('password')
                }

        return None   

    def load_data(self):
        # Load account data
        with open(self.accounts_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                account_number = row['account_number']
                self.accounts[account_number] = {
                    'account_name': row['account_name'],
                    'balance': float(row['balance']),
                    'phone_number': row['phone_number'],
                    'encryption_key': generate_random_key(),
                    'password': row.get('password')  # Add this line to include the password
                }
                self.account_numbers.add(account_number)
                print(f"Loaded user data: {self.accounts[account_number]}")

        # Load transaction data
        with open(self.transactions_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.transactions.append({
                    'id': int(row['id']),
                    'sender_account': row['sender_account'],
                    'recipient_account': row['recipient_account'],
                    'amount': float(row['amount']),
                    'encrypted_data': row['encrypted_data'],
                    'transaction_key': row['transaction_key']
                })

    def save_transaction(self, transaction):
        # Save transaction details to the transactions CSV file
        with open(self.transactions_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                transaction['id'],
                transaction['sender_account'],
                transaction['recipient_account'],
                transaction['amount'],
                transaction['encrypted_data'],
                transaction['transaction_key']
            ])

    def get_transaction_by_id(self, transaction_id):
        # Retrieve a transaction by its ID
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                return transaction
        return None

    def generate_transaction_key(self):
        # Generate a new random key for each transaction
        return generate_random_key()

    def update_balance_by_account_number(self, account_number, amount):
        # Update balance based on the account number
        if account_number in self.accounts:
            self.accounts[account_number]['balance'] += amount
            self.save_accounts_to_csv() 

    def add_transaction_by_account_number(self, sender_account_number, recipient_account_number, amount, encrypted_data):
        # Add transaction details to the database
        transaction_id = len(self.transactions) + 1
        transaction_key = self.generate_transaction_key()

        transaction = {
            'id': transaction_id,
            'sender_account': sender_account_number,
            'recipient_account': recipient_account_number,
            'amount': amount,
            'encrypted_data': encrypted_data,
            'transaction_key': transaction_key
        }

        self.transactions.append(transaction)
        return transaction_id
        
    def save_accounts_to_csv(self):
        # Save account details to the accounts CSV file
        with open(self.accounts_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['account_number', 'account_name', 'balance', 'phone_number', 'encryption_key', 'password'])
            for account_number, user_data in self.accounts.items():
                writer.writerow([
                    account_number,
                    user_data['account_name'],
                    user_data['balance'],
                    user_data['phone_number'],
                    user_data['encryption_key'],
                    user_data['password']
                ])    

    def get_balance_by_account_number(self, account_number):
        # Retrieve balance by account number
        if account_number in self.accounts:
            return self.accounts[account_number]['balance']
        return 0

    def get_phone_number_by_account_number(self, account_number):
        # Retrieve phone number by account number
        if account_number in self.accounts:
            return self.accounts[account_number]['phone_number']
        return None

db = Database()
