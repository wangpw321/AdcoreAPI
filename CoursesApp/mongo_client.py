from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class MongoDBClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            logger.info("Initializing MongoDB client")
            cls._client = MongoClient(
                "mongodb+srv://wangpw321:szoau9miBiA8o7RN@cluster1.texblzu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1",
                authMechanism="SCRAM-SHA-1",
                maxPoolSize=50,
                minPoolSize=5,
                maxIdleTimeMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
            )
        return cls._client

    @classmethod
    def close_client(cls):
        if cls._client:
            logger.info("Closing MongoDB client")
            cls._client.close()
            cls._client = None
