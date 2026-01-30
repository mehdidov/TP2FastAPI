from pydantic import BaseModel
from typing import Optional

# Product fields
class ProductBase(BaseModel):
    name: str
    price: int

# Schema used to create a product 
class ProductCreate(ProductBase):
    pass

# Schema used to update a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

# Schema used for API responses
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
