
from pydantic import BaseModel, Field
from typing import Optional


# Request schema for creating a product
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str


# Request schema for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None


# Response schema
class ProductResponse(ProductCreate):
    id: int
