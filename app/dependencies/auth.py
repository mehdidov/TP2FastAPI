from dotenv import load_dotenv
import os
load_dotenv() # loads the environment variables that are in .env 
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User as UserModel

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY") # Confidential code used to guarantee the authenticity and integrity of a JWT token
if not SECRET_KEY:
    raise RuntimeError("il n y a pas de SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password hashing(bcrypt)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # The token is retrieved in the endpoint


# Open a connection to the database dedicated to each user 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Validates the correspondence between the password entered and its encrypted version in the database
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Password security through hashing upon registration
def get_password_hash(password):
    return pwd_context.hash(password)

# User authentication function
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Generate the JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Returns the logged-in user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception
    return user