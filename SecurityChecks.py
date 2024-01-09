from flask import session
import hashlib
import secrets

# Function to generate a random recovery key
def generate_recovery_key() -> str:
    ''' Generates a random URL-safe recovery key'''
    return secrets.token_urlsafe(20)  # Generate a random URL-safe recovery key

# Function to hash data
def hash_data(data:str) -> str:
    ''' Hashes data in a way which is designed to be deterministic'''
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data

# Function to check if the user is logged in
def check_logged_in() -> bool:
    ''' Checks if the user is currently logged in '''
    return 'logged_in' in session