# src/api/auth.py

def authenticate_user(user_id: str, token: str) -> bool:
    # Dummy hardcoded users for testing
    valid_users = {
        "farmer1": "token123",
        "farmer2": "token456"
    }
    return valid_users.get(user_id) == token
