from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.models.product import Product
from app.database.session import get_db

router = APIRouter()


@router.get("")
def list_products(
    search: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(Product.name.ilike(term), Product.description.ilike(term), Product.category.ilike(term))
        )
    products = query.order_by(Product.name.asc()).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "slug": item.slug,
            "description": item.description,
            "category": item.category,
            "price": item.price,
            "stock_quantity": item.stock_quantity,
            "is_organic": item.is_organic,
            "image_url": item.image_url,
        }
        for item in products
    ]
