from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repository


def create_user(db: Session, name: str, email: str) -> User:
    user = User(
        name=name,
        email=email
    )

    return user_repository.create_user(db, user)


def get_users(db: Session) -> list[User]:
    return user_repository.get_users(db)


def get_user(db: Session, user_id: int) -> User | None:
    return user_repository.get_user_by_id(db, user_id)


def delete_user(db: Session, user_id: int) -> User | None:
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        return None

    user_repository.delete_user(db, user)

    return user

def update_user(db: Session,user_id:int, name: str | None , email: EmailStr | None) -> User | None:
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        return None
    
    if name is not None:
        user.name = name
                
    if email is not None:
        user.email = email   

    return  user_repository.update_user(db, user)