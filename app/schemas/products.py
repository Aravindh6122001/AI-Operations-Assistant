from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    model_config = {
        "from_attributes": True
    }