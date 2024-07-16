from io import BytesIO
import logging
import requests
import pandas as pd
from pymongo import MongoClient, ASCENDING
from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    help = "Download, normalize, and save data to MongoDB"

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("Starting data update process...")
        self.update_data(logger)

    def update_data(self, logger):
        # Step 1: Download the delimited file
        url = "https://api.mockaroo.com/api/501b2790?count=1000&key=8683a1c0"  # Replace with your URL
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Failed to download file")
            return

        # Step 2: Normalize the data using Pandas
        # Convert bytes to a file-like object
        file_like_object = BytesIO(response.content)
        data = pd.read_csv(file_like_object)

        # Perform normalization operations as needed
        # For example, you might clean data, drop duplicates, etc.

        # Step 3: Save the data into MongoDB
        client = MongoClient(
            "mongodb+srv://wangpw321:szoau9miBiA8o7RN@cluster1.texblzu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
        )
        db = client.coursesdb

        # Ensure the collection is a time-series collection with a 10-minute expiration
        try:
            db.create_collection(
                "normalized_data",
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "metadata",
                    "granularity": "minutes",
                },
                expireAfterSeconds=600,  # 10 minutes
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise

        # Step 4: Insert normalized data into MongoDB
        data_dict = data.to_dict("records")
        for record in data_dict:
            record["timestamp"] = datetime.utcnow()  # Add current timestamp
            record["metadata"] = {}  # Add any metadata if necessary

        db.normalized_data.insert_many(data_dict)

        # Ensure TTL index is created
        db.normalized_data.create_index(
            [("timestamp", ASCENDING)], expireAfterSeconds=600
        )

        logger.info("Data update process completed successfully")
