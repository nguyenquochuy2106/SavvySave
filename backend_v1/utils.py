import numpy as np

def cosine_similarity(emb1, emb2):
    """Calculate cosine similarity between two embeddings"""
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

def store_user_face_embedding(user_id, image_path):
    """Extract and store face embedding in Supabase"""
    face = preprocess_image(image_path)
    if face is None:
        return False

    embedding = get_embedding(face).astype(np.float32).tobytes()  # Convert to bytes
    supabase.table("users").update({"face_embedding": embedding}).eq("id", user_id).execute()
    return True
