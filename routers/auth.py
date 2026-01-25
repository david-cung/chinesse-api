import os
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database.database import get_db
from models.user import User
from schemas.schemas import UserCreate, UserResponse, Token, TokenWithUser, GoogleAuthRequest
from utils.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Google Auth
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    print("Warning: google-auth not installed. Run: pip install google-auth")

router = APIRouter(prefix="/auth", tags=["auth"])

# Google Client ID from environment
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")


def generate_unique_username(base_name: str, db: Session) -> str:
    """Generate a unique username from base name"""
    # Clean and normalize the base name
    username = base_name.lower().replace(" ", "_").replace(".", "_")[:20]
    
    # Check if username exists
    if not db.query(User).filter(User.username == username).first():
        return username
    
    # Add random suffix if username exists
    for _ in range(10):
        suffix = secrets.token_hex(3)
        new_username = f"{username}_{suffix}"
        if not db.query(User).filter(User.username == new_username).first():
            return new_username
    
    # Fallback: use random string
    return f"user_{secrets.token_hex(6)}"


# ==================== Email/Password Authentication ====================

@router.post("/register", response_model=TokenWithUser)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.
    
    Returns access token and user data on success.
    """
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        auth_provider="email",
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


@router.post("/login", response_model=TokenWithUser)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    Note: Uses OAuth2PasswordRequestForm, so send as form data:
    - username: email address
    - password: user password
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user registered with OAuth (no password)
    if user.auth_provider != "email" or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This account uses {user.auth_provider} login. Please login with {user.auth_provider}.",
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# ==================== Google OAuth Authentication ====================

@router.post("/google", response_model=TokenWithUser)
def google_auth(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Login or register with Google OAuth.
    
    The client should use Google Sign-In SDK to get the ID token,
    then send it to this endpoint.
    
    Flow:
    1. Client gets ID token from Google Sign-In
    2. Client sends ID token to this endpoint
    3. Server verifies token and extracts user info
    4. Server creates new user or logs in existing user
    5. Server returns JWT access token
    
    Request body:
    - id_token: The ID token from Google Sign-In
    """
    if not GOOGLE_AUTH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google authentication is not configured on the server"
        )
    
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Client ID is not configured"
        )
    
    try:
        # Verify the Google ID token
        idinfo = id_token.verify_oauth2_token(
            request.id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        
        # Verify the issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token issuer"
            )
        
        # Extract user info from the verified token
        google_id = idinfo['sub']
        email = idinfo.get('email')
        email_verified = idinfo.get('email_verified', False)
        full_name = idinfo.get('name', '')
        picture = idinfo.get('picture')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    
    # Check if user exists by Google ID
    user = db.query(User).filter(User.google_id == google_id).first()
    
    if user:
        # User exists, login
        pass
    else:
        # Check if user exists by email (may have registered with email first)
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # Link Google account to existing user
            if user.auth_provider == "email":
                # User registered with email, now linking Google
                user.google_id = google_id
                user.auth_provider = "google"  # Switch to Google as primary
                if not user.avatar and picture:
                    user.avatar = picture
                if not user.full_name and full_name:
                    user.full_name = full_name
                if email_verified:
                    user.is_verified = True
                db.commit()
                db.refresh(user)
        else:
            # Create new user
            username = generate_unique_username(full_name or email.split('@')[0], db)
            
            user = User(
                username=username,
                email=email,
                google_id=google_id,
                auth_provider="google",
                full_name=full_name,
                avatar=picture,
                is_verified=email_verified,
                hashed_password=None  # No password for OAuth users
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


# ==================== Helper Endpoints ====================

from utils.auth import get_current_user as get_current_user_dep

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user_dep)):
    """Get current logged in user's information"""
    return current_user