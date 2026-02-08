from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import Dict
from datetime import timedelta
from database import get_async_session
from models.user import User, UserCreate, UserLogin, UserResponse, hash_password, verify_password
from utils.auth import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: Session = Depends(get_async_session)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = await session.execute(
        select(User).where(User.email == user.email)
    )
    if existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create the new user
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )

    session.add(db_user)
    try:
        await session.commit()
        await session.refresh(db_user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return db_user


@router.post("/login")
async def login(user_credentials: UserLogin, session: Session = Depends(get_async_session)) -> Dict[str, str]:
    """
    Authenticate user and return access token
    """
    # Find the user by email
    stmt = select(User).where(User.email == user_credentials.email)
    result = await session.execute(stmt)
    
    # Use scalar to get the first result directly
    user = result.scalar()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),  # Convert to string to match return type
        "email": user.email
    }