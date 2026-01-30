from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

# Model representing a product stored in a database
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
