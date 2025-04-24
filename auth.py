import pandas as pd
import os
import hashlib

USER_DATA = "data/users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_exists(username):
    if os.path.exists(USER_DATA) and os.path.getsize(USER_DATA) > 0:
        df = pd.read_csv(USER_DATA)
        return username in df["username"].values
    return False

def signup_user(username, password):
    os.makedirs("data", exist_ok=True)
    password_hash = hash_password(password)
    user = pd.DataFrame([[username, password_hash]], columns=["username", "password"])
    if os.path.exists(USER_DATA) and os.path.getsize(USER_DATA) > 0:
        user.to_csv(USER_DATA, mode='a', header=False, index=False)
    else:
        user.to_csv(USER_DATA, index=False)  # writes headers if file doesn't exist or is empty

def login_user(username, password):
    if os.path.exists(USER_DATA) and os.path.getsize(USER_DATA) > 0:
        df = pd.read_csv(USER_DATA)
        password_hash = hash_password(password)
        user = df[(df["username"] == username) & (df["password"] == password_hash)]
        return not user.empty
    return False
