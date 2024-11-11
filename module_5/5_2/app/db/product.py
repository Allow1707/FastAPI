import logging
import uuid
from fastapi import HTTPException
from app.api.schemas.product import ProductCreate, ProductReturn
from databases import Database
from app.core.config import load_config, Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


DATABASE_URL = "postgresql://postgres:7793@localhost:5433/fast_api"

database = Database(DATABASE_URL)

async def get_product_query(product_uuid: str) -> ProductReturn:
    query: str = "SELECT * FROM public.products WHERE uuid = :product_uuid"
    values: dict = {"product_uuid": product_uuid}
    logger.info(f"get_product_query: {query}")
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product from database: {e}")
    if result:
        logger.info(f"get_product_query select content: {result}")
        content = ProductReturn.model_validate(result)
        return content
    else:
        raise HTTPException(status_code=404, detail="Product not found")


async def create_product_query(product: ProductCreate) -> str:
    query: str = """
        INSERT INTO public.products(uuid, name, price) 
        VALUES (:uuid, :name, :price)
        RETURNING uuid; 
    """
    product_uuid: str = str(uuid.uuid4())
    values: dict = {"uuid": product_uuid, "name": product.name, "price": product.price}
    logger.info(f"create_product_query: {query}")
    try:
        product_uuid: str = await database.execute(query=query, values=values)
        return product_uuid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {e}")


async def update_product_query(product_uuid: str, product: ProductCreate) -> uuid:
    print(product_uuid, product)
    query: str = """
        UPDATE public.products
        SET name = :name, price = :price
        WHERE uuid = :uuid
        RETURNING uuid
    """
    values: dict = {"uuid": product_uuid, "name": product.name, "price": product.price}
    logger.info(f"update_product_query: {query}")
    try:
        result = await database.execute(query=query, values=values)
        print(result, type(result))
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {e}")

async def delete_product_query(product_uuid: str) -> str:
    query = """
        DELETE FROM public.products
        WHERE uuid = :uuid 
        RETURNING uuid
    """
    values: dict = {"uuid": product_uuid}
    logger.info(f"delete_product_query: {query}")
    try:
        product_uuid: str = await database.execute(query=query, values=values)
        return product_uuid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {e}")
