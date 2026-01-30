from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.schemas.user import UserCreate
from app.dependencies.auth import authenticate_user, create_access_token, get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Authentication router
router = APIRouter(prefix="/auth", tags=["Auth"])

# Open access to the database and automatically closes it once processing is complete
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# New user with a hashed password.
@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="utilisateur déjà existant")
    new_user = UserModel(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "utilisateur créé"}

# Allows to create a user with a secure password
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="erreur d'identifiants")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}