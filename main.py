from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="K8s Demo API", version="1.0.0")

# ---- Data model ----
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

# ---- In-memory database ----
items_db: Dict[int, Item] = {
    1: Item(id=1, name="Laptop", description="Fast laptop", price=999.99),
    2: Item(id=2, name="Phone", description="Smartphone", price=599.50)
}

# ---- Endpoints ----

@app.get("/", tags=["root"])
def root():
    return {"message": "Hello from Kubernetes FastAPI service!"}


@app.get("/items", response_model=List[Item], tags=["items"])
def list_items():
    """List all items."""
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int):
    """Get single item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", response_model=Item, tags=["items"])
def create_item(item: Item):
    """Create a new item."""
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    items_db[item.id] = item
    return item


@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, updated: Item):
    """Update existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = updated
    return updated


@app.delete("/items/{item_id}", tags=["items"])
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully."}

# ----------------------------------------------------------
#                HEAD & OPTIONS ENDPOINTS
# ----------------------------------------------------------

# ---- HEAD for collection ----
@app.head("/items", tags=["HEAD/OPTIONS"])
def head_items(response: Response):
    response.headers["X-Total-Count"] = str(len(items_db))
    return Response(status_code=200)

# ---- HEAD for specific item ----
@app.head("/items/{item_id}", tags=["HEAD/OPTIONS"])
def head_item(item_id: int, response: Response):
    if item_id not in items_db:
        return Response(status_code=404)
    response.headers["X-Item-Exists"] = "true"
    return Response(status_code=200)

# ---- OPTIONS for collection ----
@app.options("/items", tags=["HEAD/OPTIONS"])
def options_items():
    return {
        "allowed_methods": ["GET", "POST", "HEAD", "OPTIONS"]
    }

# ---- OPTIONS for specific item ----
@app.options("/items/{item_id}", tags=["HEAD/OPTIONS"])
def options_item():
    return {
        "allowed_methods": ["GET", "PUT", "DELETE", "HEAD", "OPTIONS"]
    }
