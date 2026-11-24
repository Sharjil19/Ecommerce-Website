
from fastapi import APIRouter, HTTPException
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Temporary in-memory product storage
products = []
product_id_counter = 1


# 1. Create Product
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):

    global product_id_counter

    new_product = {
        "id": product_id_counter,
        **product.model_dump()
    }

    products.append(new_product)
    product_id_counter += 1

    return new_product


# 2. Get All Products
@router.get("/", response_model=list[ProductResponse])
def get_products():
    return products


# 3. Get Product by ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# 4. Update Product
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_data: ProductUpdate):

    for product in products:
        if product["id"] == product_id:

            changes = updated_data.model_dump(exclude_unset=True)

            product.update(changes)

            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# 5. Delete Product
@router.delete("/{product_id}")
def delete_product(product_id: int):

    for index, product in enumerate(products):
        if product["id"] == product_id:

            products.pop(index)

            return {
                "message": "Product deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
