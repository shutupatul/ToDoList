from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token
from pymongo import MongoClient
import os

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.ToDoList
user_collection = db.users  # Collection for users

# Password context (for hashing)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/auth/login")
async def login(request: LoginRequest):

    user = user_collection.find_one({"username": request.username})
    
    if not user or not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(request.username)
    return {"access_token": access_token, "token_type": "bearer"}

# Register a new user
@router.post("/auth/register")
async def register(request: UserCreate):

    if user_collection.find_one({"username": request.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    

    hashed_password = hash_password(request.password)

    # Create a new user
    user_collection.insert_one({
        "username": request.username,
        "password": hashed_password
    })
    return {"message": "User registered successfully"}
