from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.users import UserResponse, UserUpdate
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return user_service.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete(
    "/{user_id}",
    response_model=UserResponse
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.delete(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_input: UserUpdate,
    db: Session = Depends(get_db)
):
    user = user_service.update_user(
        db,
        user_id,
        user_input.name,
        user_input.email
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user