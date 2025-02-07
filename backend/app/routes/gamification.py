from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.config.database import get_db
from backend.app.models.models import Gamification, User
from backend.schemas import GamificationResponse, GamificationUpdate
from backend.app.routes.auth import get_current_user

router = APIRouter(prefix= "/gamification", tags=["Gamification"])

# Get Gamification Data
@router.get("/", response_model=GamificationResponse)
def get_gamification(
        db: Session = Depends(get_db),
        user_email: str = Depends(get_current_user)
):
    user=db.query(User).filter(User.id==user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    gamification=db.query(Gamification).filter(Gamification.user_id==user.id).first()
    if not gamification:
        raise HTTPException(status_code=404, detail="Gamification not found")
    return gamification

# Update Gamification Data(e.g rewards)
@router.post("/", response_model=GamificationResponse)
def update_gamification(
        update: GamificationUpdate,
        db: Session = Depends(get_db),
        user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.id==user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    gamification = db.query(Gamification).filter(Gamification.user_id==user.id).first()
    if not gamification:
        gamification=Gamification(
            user_id = user.id,
            streak_days=0,
            achievements="",
            rewards_points=0
        )
    db.add(gamification)

    # Update streaks and rewards
    gamification.streak_days += update.streak_days
    gamification.achievements += update.achievements
    gamification.rewards_points += update.rewards_points

    db.commit()
    db.refresh(gamification)
    return gamification


