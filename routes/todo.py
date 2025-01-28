from fastapi import APIRouter, HTTPException, Depends
from models.todo import ToDo, Update
from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext
from typing import List
from auth.jwt_handler import create_access_token, decode_token
from auth.auth_bearer import JWTBearer
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

# Initializing MongoDB client and db
client = MongoClient(MONGODB_URI)
db = client.ToDoList
collection = db.tdl_db

router = APIRouter()

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to get ObjectId
def str_to_object(id: str) -> ObjectId:
    return ObjectId(id)

# Create new task ("C"RUD) (Protected)
@router.post("/tasks/", dependencies=[Depends(JWTBearer())], response_model=ToDo)
async def create_task(task: ToDo):
    task_dict = task.dict()
    result = collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    return task_dict

# Get all tasks (C"R"UD) (Protected)
@router.get("/tasks/", dependencies=[Depends(JWTBearer())], response_model=List[ToDo])
async def get_all():
    tasks = collection.find()
    return [ToDo(**task) for task in tasks]

# Get individual task by ID (C"R"UD) (Protected)
@router.get("/tasks/{task_id}", dependencies=[Depends(JWTBearer())], response_model=ToDo)
async def get_task(task_id: str):
    task = collection.find_one({"_id": str_to_object(task_id)})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task by ID (CR"U"D) (Protected)
@router.put("/tasks/{task_id}", dependencies=[Depends(JWTBearer())], response_model=ToDo)
async def update_task(task_id: str, task: Update):
    updated_task = {key: value for key, value in task.dict(exclude_unset=True).items()}
    if updated_task:
        result = collection.update_one({"_id": str_to_object(task_id)}, {"$set": updated_task})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Todo not found or nothing to update")
        updated_todo = collection.find_one({"_id": str_to_object(task_id)})
        return updated_todo
    raise HTTPException(status_code=400, detail="No valid fields to update")

# Delete a task by ID (CRU"D") (Protected)
@router.delete("/tasks/{task_id}", dependencies=[Depends(JWTBearer())], response_model=ToDo)
async def delete_task(task_id: str):
    task = collection.find_one({"_id": str_to_object(task_id)})
    if task is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    collection.delete_one({"_id": str_to_object(task_id)})
    return task
