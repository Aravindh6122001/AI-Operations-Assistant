from pymongo import MongoClient

from app.core.config import settings


client = MongoClient(settings.MONGODB_URL)

mongo_db = client[settings.MONGODB_DATABASE]

conversations_collection = mongo_db["conversations"]


# for index demonstration purpose
def ensure_mongodb_indexes():
    conversations_collection.create_index(
        [
            ("user_id", 1),
            ("updated_at", -1),
            ("_id", -1),
        ],
        name="ix_conversations_user_updated",
    )