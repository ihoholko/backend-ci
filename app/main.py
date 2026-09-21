from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Sample FastAPI Backend", version="1.0.0")


class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: str | None = None


items_db: List[dict] = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "Gaming laptop"},
    {"id": 2, "name": "Mouse", "price": 29.99, "description": "Wireless mouse"},
]


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the FastAPI backend", "version": app.version}


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.get("/items")
async def get_items() -> List[dict]:
    return items_db


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict:
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> dict:
    if any(existing["id"] == item.id for existing in items_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with id {item.id} already exists",
        )

    items_db.append(item.model_dump())
    return item.model_dump()
