from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.config.database import get_db
from backend.app.models.models import Transaction, User
from backend.schemas import TransactionCreate, TransactionResponse
from backend.app.routes.auth import get_current_user  # Import JWT authentication

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ✅ Create a new transaction
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_transaction = Transaction(
        user_id=user.id,
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        transaction_date=datetime.utcnow()
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# ✅ Get all transactions for the authenticated user
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    return transactions

# ✅ Get a single transaction by ID
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

# ✅ Update a transaction
@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    updated_transaction: TransactionCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update fields
    transaction.amount = updated_transaction.amount
    transaction.category = updated_transaction.category
    transaction.description = updated_transaction.description

    db.commit()
    db.refresh(transaction)
    return transaction

# ✅ Delete a transaction
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
