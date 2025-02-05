from pydantic import BaseModel, EmailStr
from datetime import datetime

from sqlalchemy import FLOAT


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

# Authentication Logic Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Transaction Request Schema
class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: str

# Transaction Response Schema
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    description: str
    transaction_date: datetime

