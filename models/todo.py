from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Base Model

class ToDo(BaseModel):
    title: str
    desc: Optional[str] = None
    done: bool = False
    created_at: datetime = datetime.now()


#Model for updating a task in ToDO

class Update(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    done: Optional[bool] = None