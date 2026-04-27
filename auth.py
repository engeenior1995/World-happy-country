import pandas as pd
import hashlib
import os
from datetime import datetime
import streamlit as st

USERS_FILE = 'users.csv'

def _init_users_file():
    """Initializes the users CSV if it doesn't exist."""
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=['username', 'password', 'signup_date'])
        df.to_csv(USERS_FILE, index=False)

def _hash_password(password):
    """Simple SHA256 hash for passwords."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def login_user(username, password):
    """
    Verifies user credentials.
    Returns True if valid, False otherwise.
    """
    _init_users_file()
    try:
        df = pd.read_csv(USERS_FILE)
    except pd.errors.EmptyDataError:
        return False
        
    hashed_pw = _hash_password(password)
    
    user_row = df[df['username'] == username]
    
    if not user_row.empty:
        if user_row.iloc[0]['password'] == hashed_pw:
            return True
    return False

def register_user(username, password):
    """
    Registers a new user.
    Returns:
        (True, "Success Message")
        (False, "Error Message")
    """
    _init_users_file()
    df = pd.read_csv(USERS_FILE)
    
    if username in df['username'].values:
        return False, "Username already exists."
        
    hashed_pw = _hash_password(password)
    new_user = pd.DataFrame({
        'username': [username], 
        'password': [hashed_pw],
        'signup_date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    new_user.to_csv(USERS_FILE, mode='a', header=False, index=False)
    return True, "User created successfully. Please login."

def check_auth():
    """Checks session state for authentication."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    return st.session_state['authenticated']
