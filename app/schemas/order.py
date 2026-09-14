from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }


class OrderResponse(BaseModel):
    id: int
    status: str
    user_id: int
    items: list[OrderItemResponse]

    model_config = {
        "from_attributes": True
    }