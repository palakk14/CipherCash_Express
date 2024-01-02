# backend/utils.py
import random

def generate_random_key():
    # Generate a random encryption key
    return str(random.randint(10000000, 99999999))
