# encryption.py
from Crypto.Cipher import DES
import base64

def encrypt_data(data, key):
    # Make sure the data length is a multiple of 8 (DES block size)
    data += ' ' * (8 - len(data) % 8)

    # Encode the key as bytes
    key = key.encode('utf-8')

    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted_data).decode('utf-8')
