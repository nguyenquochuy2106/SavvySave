from fastapi import APIRouter, HTTPException, File, UploadFile
from backend.facenet.recognize import verify_face
from backend.utils import generate_jwt_token
from backend.config import supabase

auth_router = APIRouter()

@auth_router.post("/faceid-login")
async def faceid_login(file: UploadFile = File(...)):
    face_verified, user_id = verify_face(file.file)
    if not face_verified:
        raise HTTPException(status_code=401, detail="Face not recognized")
    token = generate_jwt_token(user_id)
    return {"message": "Login successful", "token": token}
