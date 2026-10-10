from datetime import datetime

from pydantic import BaseModel, Field
from typing import Literal


class ConversationCreate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: str
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    

class MessageCreate(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10_000)


class MessageResponse(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime    