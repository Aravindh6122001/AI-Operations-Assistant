from fastapi import HTTPException
from bson.errors import InvalidId

from app.repositories.coversation_repository import (
    ConversationRepository
)


class ConversationService:

    @staticmethod
    def create_conversation(
        user_id: int,
        title: str
    ):
        return ConversationRepository.create(
            user_id=user_id,
            title=title,
        )

    @staticmethod
    def get_conversation(
        user_id: int,
        conversation_id: str
    ):
        conversation = ConversationRepository.get_by_id(
            conversation_id
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        # Authorization / ownership check
        if conversation["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return conversation

    @staticmethod
    def list_conversations(user_id: int):
        return ConversationRepository.list_by_user(
            user_id
        )

    @staticmethod
    def update_conversation(
        user_id: int,
        conversation_id: str,
        title: str,
    ):
        conversation = ConversationService.get_conversation(
            user_id,
            conversation_id,
        )

        ConversationRepository.update_title(
            conversation_id,
            title,
        )

        return {
            **conversation,
            "title": title,
        }

    @staticmethod
    def delete_conversation(
        user_id: int,
        conversation_id: str,
    ):
        ConversationService.get_conversation(
            user_id,
            conversation_id,
        )

        result = ConversationRepository.delete(
            conversation_id
        )

        return result.deleted_count > 0
    
    @staticmethod
    def add_message(
        user_id: int,
        conversation_id: str,
        role: str,
        content: str,
    ):
        try:
            conversation = ConversationRepository.get_by_id(
                conversation_id
            )
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail="Invalid conversation ID",
            )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        if conversation["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        result = ConversationRepository.add_message(
            conversation_id,
            role,
            content,
        )

        return {
            "success": result.modified_count == 1,
            "conversation_id": conversation_id,
        }

    @staticmethod
    def list_conversations(
        user_id: int,
        limit: int = 20,
        offset: int = 0,
    ):
        if not 1 <= limit <= 100:
            raise HTTPException(
                status_code=400,
                detail="limit must be between 1 and 100",
            )

        if offset < 0:
            raise HTTPException(
                status_code=400,
                detail="offset cannot be negative",
            )

        return ConversationRepository.list_by_user(
            user_id,
            limit,
            offset,
        )
        
    @staticmethod
    def get_messages(user_id: int, conversation_id: str):
        try:
            conversation = ConversationRepository.get_by_id(
                conversation_id
            )
        except Exception as exc:
            from bson.errors import InvalidId

            if isinstance(exc, InvalidId):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid conversation ID",
                )
            raise

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        if conversation["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return ConversationRepository.list_messages(
            conversation_id
        )
        
        
    @staticmethod
    def get_message_counts_by_role(user_id: int):
        return ConversationRepository.get_message_counts_by_role(
            user_id=user_id
        )    