# utils/auth.py
import hashlib
import os
import base64
from typing import Optional
from datetime import datetime, timedelta

# Try to import JWT libraries
try:
    from jose import JWTError, jwt
except ImportError:
    print("Warning: python-jose not installed. Run: pip install python-jose[cryptography]")
    jwt = None

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "tiantian-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def get_password_hash(password: str) -> str:
    """Hash password using PBKDF2-SHA256"""
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return base64.b64encode(salt + pwdhash).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        decoded = base64.b64decode(hashed_password.encode('utf-8'))
        salt = decoded[:32]
        stored_hash = decoded[32:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return pwdhash == stored_hash
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if jwt is None:
        raise ImportError("python-jose is required. Install: pip install python-jose[cryptography]")
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token (alias for decode_access_token)"""
    return decode_access_token(token)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify JWT access token"""
    if jwt is None:
        return None
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"Token decode error: {e}")
        return None


def authenticate_user(db, email: str, password: str):
    """Authenticate user by email and password"""
    from models.user import User
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
        
    if not verify_password(password, user.hashed_password):
        return None
        
    return user
