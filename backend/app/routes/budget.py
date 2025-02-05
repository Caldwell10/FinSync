from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.config.database import get_db
from backend.app.models.models import Budget, User
from backend.schemas import BudgetCreate, BudgetResponse
from backend.app.routes.auth import get_current_user

router = APIRouter(prefix="/budget", tags=["Budget"])

# Create a Budget
@router.get("/", response_model=BudgetResponse)
def create_budget(
        budget: BudgetCreate,
        db: Session = Depends(get_db),
        user_email: str = Depends(get_current_user),
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_budget = Budget(
        user_id = user.id,
        category=budget.category,
        limit_amount=budget.limit_amount,
        alert_threshold=budget.alert_threshold
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

# Get All Budgets for Current User
@router.get("/", response_model=list[BudgetResponse])
def get_budgets(
        db:Session = Depends(get_db),
        user_email: str = Depends(get_current_user),

):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Budget).filter(Budget.user_id == user.id).all()

# Update a Budget
@router.get("/{budget_id}", response_model=BudgetResponse)
def update_budget(
        budget_id: int,
        budget: BudgetCreate,
        db: Session = Depends(get_db),
        user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user.id).first()
    if not existing_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    existing_budget.category = budget.category
    existing_budget.limit_amount = budget.limit_amount
    existing_budget.alert_threshold = budget.alert_threshold

    db.commit()
    db.refresh(existing_budget)
    return existing_budget

@router.delete("/{budget_id}")
def delete_budget(
        budget_id: int,
        db: Session = Depends(get_db),
        user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    budget=db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}
