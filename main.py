from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Item Management API",
    description="A simple FastAPI service for managing items",
    version="1.0.0"
)

# Schema definitions using Pydantic
class ItemBase(BaseModel):
    name: str = Field(..., example="Wireless Mouse")
    description: Optional[str] = Field(None, example="Ergonomic optical mouse")
    price: float = Field(..., gt=0, example=29.99)
    in_stock: bool = Field(default=True, example=True)

class ItemResponse(ItemBase):
    id: int

# In-memory storage simulation
items_db: List[dict] = [
    {"id": 1, "name": "Mechanical Keyboard", "description": "RGB backlight", "price": 89.99, "in_stock": True},
    {"id": 2, "name": "USB-C Cable", "description": "Braided 6ft cable", "price": 14.99, "in_stock": True},
]

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "FastAPI service is running"}

@app.get("/items", response_model=List[ItemResponse], tags=["Items"])
def get_items(limit: int = 10, in_stock_only: bool = False):
    """Retrieve items with optional filtering by stock status."""
    results = items_db
    if in_stock_only:
        results = [item for item in results if item["in_stock"]]
    return results[:limit]

@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int):
    """Retrieve a single item by its ID."""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return item

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item: ItemBase):
    """Create a new item."""
    new_id = max((i["id"] for i in items_db), default=0) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items_db.append(new_item)
    return new_item