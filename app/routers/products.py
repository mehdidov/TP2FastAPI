from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.products import Product as ProductModel
from app.schemas.products import Product, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Read all product
@router.get("/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


# Create a product
@router.post("/", response_model=Product)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductModel(**product_in.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Update the product with the id
@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produit non trouvé")

    if product_in.name is not None:
        product.name = product_in.name
    if product_in.price is not None:
        product.price = product_in.price

    db.commit()
    db.refresh(product)
    return product


# Delete product with the id
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produit non trouvé")

    db.delete(product)
    db.commit()
    return {"message": "produit supprimé"}
