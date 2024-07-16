from datetime import datetime, timedelta
from django.apps import AppConfig
from .mongo_client import MongoDBClient
from django.core.management import call_command


class CoursesAppConfig(AppConfig):
    name = "CoursesApp"

    def ready(self):
        # Initialize the MongoDB client when Django starts
        MongoDBClient.get_client()


# class YourAppConfig(AppConfig):
#     name = "your_app"

#     def ready(self):
#         from django_cron import CronJobManager
#         from your_app.cron import UpdateDataCronJob  # type: ignore

#         manager = CronJobManager()
#         manager.register(UpdateDataCronJob)


class YourAppConfig(AppConfig):
    name = "your_app"

    def ready(self):
        self.check_and_update_data()

    def check_and_update_data(self):
        client = MongoDBClient(
            "mongodb+srv://wangpw321:szoau9miBiA8o7RN@cluster1.texblzu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
        )
        db = client.your_database_name

        # Check if data exists and is valid
        current_time = datetime.utcnow()
        ten_minutes_ago = current_time - timedelta(minutes=10)
        count = db.normalized_data.count_documents(
            {"timestamp": {"$gt": ten_minutes_ago}}
        )

        if count == 0:
            # If no valid data, run the management command to update data
            call_command("update_data")
