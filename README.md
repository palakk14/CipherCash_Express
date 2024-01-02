# CipherCash Express

## Overview

The CipherCash Express is a Python-based web application designed for secure fund transfers between users. It incorporates authentication, encryption, and consistency checks to ensure the security and integrity of transactions.

## Table of Contents

1. [Installation]
2. [Usage]
3. [File Structure]
4. [Dependencies]
5. [Configuration]
6. [Authentication]
7. [Encryption]
8. [Consistency Checks]
9. [Database]
10. [Verification]
11. [Web Interface]

## 1. Installation

- Install dependencies: pip install -r requirements.txt

## 2. Usage

- Run the application: python main.py
- Access the application in a web browser at http://localhost:5000

## 3. File Structure

  CipherCash Express
├── _init_.py
├── _pycache_
│   ├── _init_.cpython-311.pyc
│   ├── auth.cpython-311.pyc
│   ├── consistency_checks.cpython-311.pyc
│   ├── database.cpython-311.pyc
│   ├── encryption.cpython-311.pyc
│   ├── main.cpython-311.pyc
│   ├── user_interface.cpython-311.pyc
│   └── utils.cpython-311.pyc
├── accounts.csv
├── auth.py
├── consistency_checks.py
├── database.py
├── encryption.py
├── main.py
├── readme.md
├── requirements.txt
├── templates
│   ├── index.html
│   ├── transfer_amount.html
│   └── transfer_form.html
├── transactions.csv
├── utils.py
└── verification.py

## 4. Dependencies

- Flask
- Crypto (pycryptodome)

Install dependencies using: pip install -r requirements.txt

## 5. Configuration

- Update configurations in the respective files if needed.

## 6. Authentication

- The auth.py module handles user authentication using username, account number, phone number, and password.
- User authentication is done through the Flask web interface (main.py).
- The password is same as phone number.

## 7. Encryption

- Encryption of sensitive data is implemented in the encryption.py module using the DES algorithm.
- Keys are generated dynamically for each transaction.

## 8. Consistency Checks

- Consistency checks are performed in the consistency_checks.py module.
- Checks include verifying unique transaction IDs, different sender and recipient accounts, and sufficient funds.

## 9. Database

- The database.py module manages user accounts and transactions.
- It loads and saves data to CSV files (accounts.csv and transactions.csv).

## 10. Verification

- The verification.py module is responsible for verifying transfer requests.
- It checks the validity of the sender and recipient accounts, transaction amount, and other details.

## 11. Web Interface

- The web interface is implemented using Flask in main.py.
- HTML templates are stored in the templates directory.
