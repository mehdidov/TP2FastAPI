from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: int

class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
