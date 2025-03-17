from fastapi import APIRouter, HTTPException, Depends
from ..config import supabase
from ..services.auth import get_current_user

router = APIRouter()

@router.post("/transactions")
def add_transaction(user: str = Depends(get_current_user), amount: float = 0.0, category: str = "", description: str = ""):
    """Add a new transaction."""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
    
    transaction = {
        "user": user,
        "amount": amount,
        "category": category,
        "description": description,
    }
    supabase.table("transactions").insert(transaction).execute()
    return {"message": "Transaction added successfully"}


@router.get("/transactions")
def get_transactions(user: str = Depends(get_current_user)):
    """Retrieve all transactions for the current user."""
    response = supabase.table("transactions").select("*").eq("user", user).execute()
    return response.data


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, user: str = Depends(get_current_user)):
    """Delete a transaction by ID."""
    response = supabase.table("transactions").delete().eq("id", transaction_id).eq("user", user).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}


@router.get("/transactions/stats")
def get_transaction_stats(user: str = Depends(get_current_user)):
    """Retrieve spending and savings statistics for the user."""
    transactions = supabase.table("transactions").select("amount, category").eq("user", user).execute()
    
    total_spent = sum(t["amount"] for t in transactions.data if t["amount"] < 0)
    total_savings = sum(t["amount"] for t in transactions.data if t["amount"] > 0)
    
    category_breakdown = {}
    for t in transactions.data:
        category = t["category"]
        category_breakdown[category] = category_breakdown.get(category, 0) + t["amount"]
    
    return {
        "total_spent": total_spent,
        "total_savings": total_savings,
        "category_breakdown": category_breakdown,
    }
