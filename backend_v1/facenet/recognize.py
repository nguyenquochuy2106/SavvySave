import cv2
import numpy as np
import tensorflow as tf
import torch
from mtcnn import MTCNN
from backend.config import supabase
from backend.utils import cosine_similarity

# Load FaceNet model (TensorFlow)
facenet_model = tf.keras.models.load_model("backend/facenet/facenet_keras.h5")

# Load MTCNN detector (PyTorch)
detector = MTCNN()

def preprocess_image(image_path):
    """Detect face and preprocess for FaceNet"""
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(img_rgb)

    if not faces:
        return None  # No face detected

    x, y, w, h = faces[0]['box']
    face = img_rgb[y:y+h, x:x+w]
    face = cv2.resize(face, (160, 160))  # FaceNet input size
    face = np.expand_dims(face.astype("float32") / 255.0, axis=0)
    return face

def get_embedding(face_pixels):
    """Generate FaceNet embedding"""
    return facenet_model.predict(face_pixels)[0]

def verify_face(image_path):
    """Compare FaceNet embedding with stored embeddings in Supabase"""
    face = preprocess_image(image_path)
    if face is None:
        return False, None  # No face found

    input_embedding = get_embedding(face)

    # Fetch all user embeddings from Supabase
    users_data = supabase.table("users").select("id, face_embedding").execute().data

    for user in users_data:
        stored_embedding = np.frombuffer(user["face_embedding"], dtype=np.float32)
        similarity = cosine_similarity(input_embedding, stored_embedding)

        if similarity > 0.8:  # Match threshold
            return True, user["id"]

    return False, None
