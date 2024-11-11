from fastapi import APIRouter, Depends
from app.api.schemas.product import ProductReturn, ProductCreate

from app.db.product import get_product_query, create_product_query, update_product_query, delete_product_query


products_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@products_router.get("/get_product", response_model=ProductReturn)
async def get_product(product_uuid: str):
    content: ProductReturn = await get_product_query(product_uuid)
    return content

@products_router.post("/create_product", response_model=dict)
async def create_product(product: ProductCreate):
    print(product)
    product_uuid: str = await create_product_query(product)
    return {"message": "Product was successful create", "uuid": product_uuid}

@products_router.post("/update_product", response_model=dict)
async def update_product(product_uuid: str, product: ProductCreate):
    product_uuid: ProductReturn = await update_product_query(product_uuid, product)
    return {"message": "Product was successful update", "uuid": product_uuid}

@products_router.post("/delete_product", response_model=dict)
async def update_product(product_uuid: str):
    product_uuid: str = await delete_product_query(product_uuid)
    return {"message": "Product was successful delete", "uuid": product_uuid}