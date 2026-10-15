from sqlalchemy.orm import Session

import redis,logging
from fastapi import HTTPException
from pydantic import ValidationError , TypeAdapter

from app.db.redis import redis_client
from app.schemas.products import ProductResponse

from app.models.product import Product
from app.schemas.products import ProductUpdate

from app.repositories import product_repository



def create_product(
    db: Session,
    name: str,
    price: float,
    stock: int,
) -> Product:
    product = Product(
        name=name,
        price=price,
        stock=stock,
    )

    created = product_repository.create_product(db, product)

    try:
        redis_client.delete("ai-backend:products:all")
    except redis.RedisError:
        pass

    return created

def get_products(db: Session):
    cache_key = "ai-backend:products:all"

    # 1. Try Redis.
    try:
        cached = redis_client.get(cache_key)

        if cached is not None:
            try:
                return TypeAdapter(
                    list[ProductResponse]
                ).validate_json(cached)
            except (ValidationError, ValueError):
                redis_client.delete(cache_key)

    except redis.RedisError:
        pass

    # 2. Cache miss: query PostgreSQL.
    products = product_repository.get_products(db)

    # 3. Convert ORM objects into response models.
    result = [
        ProductResponse.model_validate(product)
        for product in products
    ]

    # 4. Populate Redis for five minutes.
    try:
        redis_client.set(
            cache_key,
            TypeAdapter(list[ProductResponse]).dump_json(result).decode(),
            ex=300,
        )
    except redis.RedisError:
        pass

    return result

def get_product_by_id(
    db: Session,
    product_id: int,
) -> ProductResponse:
    cache_key = f"ai-backend:product:{product_id}"

    # 1. Try Redis first.
    try:
        cached_product = redis_client.get(cache_key)

        if cached_product is not None:
            try:
                return ProductResponse.model_validate_json(
                    cached_product
                )
            except (ValidationError, ValueError):
                # Malformed/stale cache entry: discard it.
                redis_client.delete(cache_key)

    except redis.RedisError:
        # Redis failure should not prevent a database read.
        pass

    # 2. Cache miss: query PostgreSQL.
    product = product_repository.get_product_by_id(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # 3. Convert the ORM object into a validated response.
    response = ProductResponse.model_validate(product)

    # 4. Populate Redis for five minutes.
    try:
        redis_client.set(
            cache_key,
            response.model_dump_json(),
            ex=300,
        )
    except redis.RedisError:
        # The request can still succeed without caching.
        pass

    return response


logger = logging.getLogger(__name__)


def invalidate_product_cache(product_id: int) -> None:
    try:
        redis_client.delete(
            f"ai-backend:product:{product_id}",
            "ai-backend:products:all",
        )
    except redis.RedisError:
        logger.warning(
            "Failed to invalidate Redis cache for product %s",
            product_id,
            exc_info=True,
        )


def update_product(db, product_id: int, product_data: ProductUpdate):
    update_data = product_data.model_dump(exclude_unset=True)

    if not update_data:
        raise ValueError("At least one field must be provided")

    product = product_repository.update_product(
        db, product_id, update_data
    )

    if product is None:
        return None

    invalidate_product_cache(product_id)
    return product


def delete_product(db, product_id: int):
    deleted = product_repository.delete_product(db, product_id)

    if not deleted:
        return False

    invalidate_product_cache(product_id)
    return True

