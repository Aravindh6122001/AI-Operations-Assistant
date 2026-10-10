from fastapi import APIRouter,Query

from app.schemas.conversation import (
    ConversationCreate,
)
from app.services.conversation_service import (
    ConversationService,
)


router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["Conversations"],
)


@router.post("/")
def create_conversation(
    data: ConversationCreate,
):
    return ConversationService.create_conversation(
        user_id=4,
        title=data.title,
    )


@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: str,
):
    return ConversationService.get_conversation(
        user_id=4,
        conversation_id=conversation_id,
    )



@router.patch("/{conversation_id}")
def update_conversation(
    conversation_id: str,
    data: ConversationCreate,
):
    return ConversationService.update_conversation(
        user_id=4,
        conversation_id=conversation_id,
        title=data.title,
    )


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
):
    return ConversationService.delete_conversation(
        user_id=4,
        conversation_id=conversation_id,
    )
    

from app.schemas.conversation import MessageCreate
from app.services.conversation_service import ConversationService


@router.get("/")
def list_conversations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    # Temporary user ID; replace with the existing JWT dependency.
    return ConversationService.list_conversations(
        user_id=4,
        limit=limit,
        offset=offset,
    )


@router.post("/{conversation_id}/messages")
def add_message(
    conversation_id: str,
    data: MessageCreate,
):
    # Temporary user ID; replace with the existing JWT dependency.
    return ConversationService.add_message(
        user_id=4,
        conversation_id=conversation_id,
        role=data.role,
        content=data.content,
    )  
    
@router.get("/{conversation_id}/messages")
def get_messages(conversation_id: str):
    # Temporary user ID; replace with your JWT dependency.
    return ConversationService.get_messages(
        user_id=4,
        conversation_id=conversation_id,
    )   
    
@router.get("/stats/messages-by-role")
def get_message_counts_by_role():
    return ConversationService.get_message_counts_by_role(
        user_id=4
    )       