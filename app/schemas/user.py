from pydantic import BaseModel
from typing import Optional

# Schema used during the inscription
class UserCreate(BaseModel):
    username: str
    password: str

# Schema used during the connection
class UserLogin(BaseModel):
    username: str
    password: str

# Schema used to return a user
class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Schema used for user updates
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None