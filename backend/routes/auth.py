from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from services.auth import hash_password, create_jwt_token
from services.face_recognition import extract_face_embedding
from database import get_db

router = APIRouter()

@router.post("/register_faceid")
async def register_faceid(email: str, password: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    hashed_pw = hash_password(password)

    # Save uploaded image
    image_path = f"uploads/{email}.jpg"
    with open(image_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Extract Face Embedding
    face_embedding = extract_face_embedding(image_path).tobytes()

    # Store user data in DB
    user = User(email=email, hashed_password=hashed_pw, face_embedding=face_embedding)
    db.add(user)
    await db.commit()
    
    return {"message": "FaceID Registered Successfully"}


import numpy as np

@router.post("/login_faceid")
async def login_faceid(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save uploaded image
    image_path = f"uploads/temp.jpg"
    with open(image_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Extract Face Embedding
    new_embedding = extract_face_embedding(image_path)

    # Retrieve all users & compare embeddings
    users = db.query(User).all()
    for user in users:
        stored_embedding = np.frombuffer(user.face_embedding, dtype=np.float32)
        similarity = np.dot(new_embedding, stored_embedding) / (np.linalg.norm(new_embedding) * np.linalg.norm(stored_embedding))
        
        if similarity > 0.9:  # Threshold for Face Match
            token = create_jwt_token({"sub": user.email})
            return {"message": "Login Successful", "access_token": token}
    
    raise HTTPException(status_code=401, detail="Face Not Recognized")
