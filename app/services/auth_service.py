from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password
)
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email
)


def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    existing_user = get_user_by_email(
        db,
        email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role="user"
    )

    return create_user(db, user)


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = authenticate_user(
        db,
        email,
        password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token_data = {
        "sub": str(user.id),
        "role": user.role
        }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }