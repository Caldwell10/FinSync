from pydantic import BaseModel, EmailStr
from datetime import datetime

# User Registration Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

