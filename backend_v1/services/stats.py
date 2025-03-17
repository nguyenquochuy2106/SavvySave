from fastapi import APIRouter
from backend.config import supabase
from backend.utils import verify_token

stats_router = APIRouter()

@stats_router.get("/summary")
async def get_summary(token: str):
    user_id = verify_token(token)
    transactions = supabase.table("transactions").select("*").eq("user_id", user_id).execute().data
    total_spent = sum(t["amount"] for t in transactions if t["amount"] < 0)
    total_saved = sum(t["amount"] for t in transactions if t["amount"] > 0)
    return {"total_spent": total_spent, "total_saved": total_saved}
