from datetime import datetime, timezone
import re


from bson import ObjectId

from app.db.mongodb import conversations_collection


class ConversationRepository:

    @staticmethod
    def create(user_id: int, title: str):
        now = datetime.now(timezone.utc)

        document = {
            "user_id": user_id,
            "title": title,
            "messages": [],
            "created_at": now,
            "updated_at": now,
        }

        result = conversations_collection.insert_one(document)
        document["_id"] = result.inserted_id

        return ConversationRepository.serialize_conversation(document)

    @staticmethod
    def get_by_id(conversation_id: str):
        document = conversations_collection.find_one(
            {"_id": ObjectId(conversation_id)}
        )

        return ConversationRepository.serialize_conversation(document)

    @staticmethod
    def list_by_user(
        user_id: int,
        limit: int = 20,
        offset: int = 0,
    ):
        cursor = (
            conversations_collection
            .find({"user_id": user_id}, {"messages": 0})
            .sort([("updated_at", -1), ("_id", -1)])
            .skip(offset)
            .limit(limit)
        )

        return [
            ConversationRepository.serialize_conversation(document)
            for document in cursor
        ]

    @staticmethod
    def update_title(
        conversation_id: str,
        title: str
    ):
        result = conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$set": {
                    "title": title,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

        return result

    @staticmethod
    def delete(conversation_id: str):
        return conversations_collection.delete_one(
            {"_id": ObjectId(conversation_id)}
        )

    @staticmethod
    def add_message(
        conversation_id: str,
        role: str,
        content: str,
    ):
        now = datetime.now(timezone.utc)

        return conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$push": {
                    "messages": {
                        "role": role,
                        "content": content,
                        "created_at": now,
                    }
                },
                "$set": {
                    "updated_at": now,
                },
            },
        )

    @staticmethod
    def search_by_user(
        user_id: int,
        title: str | None = None,
    ):
        query = {"user_id": user_id}

        if title:
            query["title"] = {
                "$regex": re.escape(title),
                "$options": "i",
            }

        return list(
            conversations_collection.find(query)
        ) 
    
    @staticmethod
    def serialize_conversation(document: dict | None):
        if document is None:
            return None

        document["_id"] = str(document["_id"])
        return document   
    
    @staticmethod
    def list_messages(conversation_id: str):
        document = conversations_collection.find_one(
            {"_id": ObjectId(conversation_id)},
            {"messages": 1},
        )

        if document is None:
            return None

        return document.get("messages", [])   
    
    @staticmethod
    def get_message_counts_by_role(user_id: int):
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$unwind": "$messages"},
            {
                "$group": {
                    "_id": "$messages.role",
                    "message_count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "role": "$_id",
                    "message_count": 1,
                }
            },
            {"$sort": {"message_count": -1}},
        ]

        return list(
            conversations_collection.aggregate(pipeline)
        )         