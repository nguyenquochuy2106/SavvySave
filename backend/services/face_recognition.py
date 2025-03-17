import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load FaceNet Model
facenet_model = load_model("models/facenet_keras.h5")

def preprocess_image(image_path):
    """Preprocess image before feeding into FaceNet."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (160, 160))
    img = np.expand_dims(img, axis=0)
    return img / 255.0

def extract_face_embedding(image_path):
    """Extract Face Embedding using FaceNet."""
    preprocessed_img = preprocess_image(image_path)
    embedding = facenet_model.predict(preprocessed_img)[0]
    return embedding
