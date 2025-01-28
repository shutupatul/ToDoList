from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") 

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in environment variables!")

ALGORITHM = "HS256"

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": username, "exp": expire}
    print(f"SECRET_KEY: {SECRET_KEY}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
