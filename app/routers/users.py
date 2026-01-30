from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.schemas.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserUpdate
from app.dependencies.auth import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Read all users
@router.get("/", response_model=list[User])
def get_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(UserModel).all()

# Read the current user
@router.get("/me", response_model = User)
def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


# Read one user with id
@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="pas d'utilisateur")
    return user


# DELETE USER
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="pas d'utilisateur")

    db.delete(user)
    db.commit()
    return {"message": "Suppression de l'utilisateur"}

@router.patch("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail="pas d'utilisateur")

    if user_in.username is not None:
        user.username = user_in.username

    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)

    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model = User)
def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


