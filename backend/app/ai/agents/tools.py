from langchain_core.tools import tool
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.database.models.product import Product
from app.ai.rag.vector_store import ChromaDBManager

@tool
def product_search(query: str) -> str:
    """Use this tool when a customer asks about specific products, stock status, or prices."""
    db: Session = SessionLocal()
    try:
        # Simple text matching against product names/descriptions for the catalog tool
        products = db.query(Product).filter(
            (Product.name.ilike(f"%{query}%")) | 
            (Product.description.ilike(f"%{query}%"))
        ).limit(3).all()
        
        if not products:
            return "No matching products found in the catalog."
            
        return "\n".join([
            f"- {p.name}: ${p.price} | Stock: {p.stock_quantity} | Organic: {p.is_organic}\n  Desc: {p.description}"
            for p in products
        ])
    finally:
        db.close()

@tool
def policy_and_recipe_search(query: str) -> str:
    """Use this tool when a customer asks about shipping, refunds, recipes, or spice guides."""
    vector_store = ChromaDBManager()
    results = vector_store.similarity_search(query, top_k=3)
    
    if not results:
        return "No relevant company documents or recipes found."
        
    return "\n\n".join([
        f"[Source Doc ID {res['metadata'].get('source_doc_id')}]: {res['content']}"
        for res in results
    ])