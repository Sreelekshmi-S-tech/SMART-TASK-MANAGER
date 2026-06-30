from pydantic import BaseModel
from typing import Optional


# ---------------------------
# USER SCHEMAS (KEEP IF YOU ALREADY HAVE LOGIN/REGISTER)
# ---------------------------

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# ---------------------------
# TOKEN SCHEMA (JWT)
# ---------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------------------
# TASK SCHEMAS
# ---------------------------

# CREATE TASK
class TaskCreate(BaseModel):
    title: str
    description: str


# UPDATE TASK (EDIT FEATURE)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# OPTIONAL (IF YOU USE RESPONSE MODELS)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int

    class Config:
        from_attributes = True