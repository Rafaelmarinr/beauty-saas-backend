from fastapi import APIRouter, Depends

from sqlmodel import Session, select

from core.security import get_current_user
from db.database import get_session

from models.payment import Payment
from models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

# ---------------- TOTAL REVENUE ----------------
@router.get("/revenue")
def get_total_revenue(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    payments = session.exec(
        select(Payment)
    ).all()

    total_revenue = sum(
        payment.amount
        for payment in payments
    )
    
    return {
        "total_revenue": total_revenue
    }