from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from supabase import create_client
from ..config import SUPABASE_URL, SUPABASE_KEY
from ..facenet.recognize import verify_face
import os

# Setup Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(username: str, image: bytes):
    # Check if user exists
    existing_user = supabase.table("users").select("id").eq("username", username).single().execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Generate Face Embedding
    face_embedding = verify_face(image)
    if face_embedding is None:
        raise HTTPException(status_code=400, detail="Face verification failed")
    
    # Save user to database
    new_user = {"username": username, "face_embedding": face_embedding}
    supabase.table("users").insert(new_user).execute()
    
    return {"message": "User registered successfully"}


@router.post("/login")
def login(username: str, image: bytes):
    # Verify Face
    user = supabase.table("users").select("id, face_embedding").eq("username", username).single().execute()
    if not user.data:
        raise HTTPException(status_code=400, detail="User not found")
    
    stored_embedding = user.data["face_embedding"]
    if not verify_face(image, stored_embedding):
        raise HTTPException(status_code=401, detail="Face verification failed")
    
    # Generate Token
    access_token = create_access_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
def logout():
    return {"message": "Successfully logged out"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
