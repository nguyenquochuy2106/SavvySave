from fastapi import APIRouter, Depends
from backend.config import supabase
from backend.utils import verify_token

transactions_router = APIRouter()

@transactions_router.post("/add")
async def add_transaction(token: str, amount: float, category: str, description: str):
    user_id = verify_token(token)
    data = {"user_id": user_id, "amount": amount, "category": category, "description": description}
    response = supabase.table("transactions").insert(data).execute()
    return {"message": "Transaction added", "data": response.data}

@transactions_router.delete("/delete/{transaction_id}")
async def delete_transaction(transaction_id: str, token: str):
    user_id = verify_token(token)
    supabase.table("transactions").delete().eq("id", transaction_id).eq("user_id", user_id).execute()
    return {"message": "Transaction deleted"}

@transactions_router.get("/search")
async def search_transaction(token: str, category: str = None):
    user_id = verify_token(token)
    query = supabase.table("transactions").select("*").eq("user_id", user_id)
    if category:
        query = query.eq("category", category)
    response = query.execute()
    return {"transactions": response.data}
