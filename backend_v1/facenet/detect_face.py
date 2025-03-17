import numpy as np
import cv2
import tensorflow as tf
from scipy.spatial.distance import cosine
from mtcnn import MTCNN

# Load pre-trained FaceNet model
facenet_model = tf.keras.models.load_model("path_to_facenet_model")
detector = MTCNN()

def detect_face(image: bytes) -> np.ndarray:
    """Detect face in the image and return the cropped face."""
    image_array = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    faces = detector.detect_faces(img)
    if not faces:
        return None
    
    x, y, width, height = faces[0]['box']
    face = img[y:y+height, x:x+width]
    return face


def get_embedding(image: bytes) -> np.ndarray:
    """Generate FaceNet embedding for a given face image."""
    face = detect_face(image)
    if face is None:
        return None
    
    face = cv2.resize(face, (160, 160))  # Resize to model input size
    face = (face - 127.5) / 127.5  # Normalize
    face = np.expand_dims(face, axis=0)
    return facenet_model.predict(face)[0]


def verify_face(image: bytes, stored_embedding: np.ndarray, threshold: float = 0.5) -> bool:
    """Verify if the face in the image matches the stored embedding."""
    new_embedding = get_embedding(image)
    if new_embedding is None:
        return False
    
    distance = cosine(new_embedding, stored_embedding)
    return distance < threshold
