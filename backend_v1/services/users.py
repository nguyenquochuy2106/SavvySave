from fastapi import APIRouter
from backend.config import supabase
from backend.utils import verify_token

users_router = APIRouter()

@users_router.put("/update")
async def update_user_info(token: str, name: str, email: str):
    user_id = verify_token(token)
    supabase.table("users").update({"name": name, "email": email}).eq("id", user_id).execute()
    return {"message": "Profile updated"}
