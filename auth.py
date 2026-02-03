from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt # Using the library directly for maximum stability
import os

SECRET_KEY = os.getenv("SECRET_KEY", "temporary-dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """
    Encrypts a plain text password into a secure hash.
    """
    # 1. Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # 2. Generate a 'salt' (extra randomness)
    salt = bcrypt.gensalt()
    # 3. Hash it!
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # 4. Return as a string so it can be stored in our fake_db
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a login attempt to the stored hash.
    """
    try:
        # Convert both to bytes for the comparison
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # This returns True if they match, False if they don't
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)