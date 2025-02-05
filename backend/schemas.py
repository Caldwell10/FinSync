from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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


# Budget Schema
class BudgetCreate(BaseModel):
    category: str
    limit_amount: float
    alert_threshold: float

class BudgetResponse(BudgetCreate):
    id:int
    user_id:int

    class Config:
        orm_mode = True

class GamificationResponse(BaseModel):
    id: int
    user_id: int
    streak_days: int
    achievements: Optional[str]
    rewards_points: int

    class Config:
        orm_mode = True

class GamificationUpdate(BaseModel):
    streak_days: int
    achievements: Optional[str]
    rewards_points: int





