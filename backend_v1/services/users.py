from fastapi import APIRouter, HTTPException, Depends
from ..config import supabase
from ..services.auth import get_current_user

router = APIRouter()

@router.get("/users/me")
def get_user_profile(user: str = Depends(get_current_user)):
    """Retrieve user profile information."""
    response = supabase.table("users").select("id, name, email, avatar").eq("id", user).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data


@router.put("/users/me")
def update_user_profile(user: str = Depends(get_current_user), name: str = "", email: str = "", avatar: str = ""):
    """Update user profile information."""
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if avatar:
        update_data["avatar"] = avatar
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    response = supabase.table("users").update(update_data).eq("id", user).execute()
    return {"message": "Profile updated successfully"}
