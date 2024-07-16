from django.utils.deprecation import MiddlewareMixin
from .mongo_client import MongoDBClient
import logging

logger = logging.getLogger(__name__)


class MongoDBMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            mongo_client = MongoDBClient.get_client()
            mongo_client.admin.command("ping")
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            MongoDBClient._client = None
            MongoDBClient.get_client()
        return None
