from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base

# Importing models
from app.models.user import User
from app.models.products import Product

# Creating tables 
Base.metadata.create_all(bind=engine)

from app.routers import auth, products, ai, users

app = FastAPI(title="TP2 FastAPI")

# Includes the different routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(ai.router)
app.include_router(users.router)

# API root
@app.get("/")
def root():
    return {
        "message": "APIFastAPI OK",
        "docs": "/docs"
    }


