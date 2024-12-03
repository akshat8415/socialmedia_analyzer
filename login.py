import os
from dotenv import load_dotenv
from instagrapi import Client

# Load environment variables from .env file
load_dotenv()

# Access the username and password
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')

def login(cl: Client):
    try:
        cl.login(username, password)
        print("Login successful!")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

# Testing the login function
if __name__ == "__main__":
    cl = Client()
    if login(cl):
        print("Logged in and ready to proceed!")
    else:
        print("Failed to authenticate.")
