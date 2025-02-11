from fastapi import FastAPI
from routes.todo import router as todo_router
from routes.auth import router as auth_router 
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the ToDoList!"}
