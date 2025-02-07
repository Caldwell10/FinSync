from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.config.database import Base

# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships with other tables
    transactions = relationship("Transaction", back_populates="user")  # One-to-Many
    gamification = relationship("Gamification", back_populates="user")  # One-to-One
    budgets = relationship("Budget", back_populates="user")  # One-to-Many

# Transactions Table
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # ✅ Fixed column definition
    description = Column(String, nullable=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")  # Links back to User

# Gamification Table
class Gamification(Base):
    __tablename__ = "gamification"  # ✅ Fixed typo

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    streak_days = Column(Integer, default=0)  # Tracks streaks for budgeting habits
    achievements = Column(String, nullable=True)
    rewards_points = Column(Integer, default=0)

    user = relationship("User", back_populates="gamification")  # Links back to User

# Budgets Table
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)  # ✅ Removed redundant "nullable=False"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ Must always have a user
    category = Column(String, nullable=False)  # Example: "Food", "Transport"
    limit_amount = Column(Float, nullable=False)  # Budget limit
    alert_threshold = Column(Float, default=0.8)  # Alert at 80% usage
    user = relationship("User", back_populates="budgets")

class NewsArticle(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    content = Column(String, unique =True, nullable=False)
    published_date=Column(DateTime, default=datetime.utcnow)



