from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    user: User
) -> User:

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int
) -> User | None:

    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_users(
    db: Session
) -> list[User]:

    return db.query(User).all()


def delete_user(
    db: Session,
    user: User
) -> None:

    db.delete(user)
    db.commit()


def update_user(
    db: Session,
    user: User
) -> User:

    db.commit()
    db.refresh(user)

    return user