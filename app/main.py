from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine

from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.api.users import router as User_router
from app.api.orders import router as orders_router
from app.api.product import router as product_router


app = FastAPI(title="AI Backend Platform")

Base.metadata.create_all(bind=engine)

app.include_router(User_router);
app.include_router(orders_router)

app.include_router(product_router)


@app.get("/health")
def health():
    return {'status': "ok"}

@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        return {"database" : result.scalar()}