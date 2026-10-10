from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# database
from sqlalchemy import text
# from app.db.database import Base, engine

# Models must be imported before create_all()
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

# Routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.orders import router as orders_router
from app.api.product import router as products_router
from app.api.conversations import router as conversations_router

from app.db.mongodb import ensure_mongodb_indexes
from app.db.database import engine



app = FastAPI(
    title="AI Backend Platform"
)


# Temporary until Alembic is introduced in Phase 3
# Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(users_router, prefix="/api/v1")
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(conversations_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/db-health")
def db_health():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        return {
            "database": result.scalar()
        }
  
@app.on_event("startup")
def initialize_mongodb():
    ensure_mongodb_indexes()

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    print(f"ERROR: {type(exc).__name__}: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )    