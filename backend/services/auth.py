from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """
    Create a JWT token with an expiration time.
    :param data: Dictionary containing user data
    :param expires_delta: Token expiration time (default: 24 hours)
    :return: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str):
    """
    Decode and verify a JWT token.
    :param token: JWT token to decode
    :return: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
