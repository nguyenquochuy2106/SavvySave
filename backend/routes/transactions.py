from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.transaction import Transaction
from database import get_db

router = APIRouter()

@router.post("/add_transaction")
async def add_transaction(user_id: int, amount: float, category: str, type: str, db: Session = Depends(get_db)):
    if type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    transaction = Transaction(user_id=user_id, amount=amount, category=category, type=type)
    db.add(transaction)
    await db.commit()
    return {"message": "Transaction Added"}

@router.get("/transactions/{user_id}")
async def list_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return transactions


