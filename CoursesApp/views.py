import time
import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from CoursesApp.models import Courses
from CoursesApp.serializers import CoursesSerializer
from pymongo.errors import PyMongoError
from .mongo_client import MongoDBClient

# Configure logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Home Page")


def check_connection():
    mongo_client = MongoDBClient.get_client()
    try:
        mongo_client.admin.command("ping")
        return mongo_client
    except (PyMongoError, Exception) as e:
        logger.error(f"MongoDB connection error: {e}")
        MongoDBClient._client = None
        return MongoDBClient.get_client()


@csrf_exempt
def courseApi(request, id=0):
    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        try:
            mongo_client = check_connection()

            if request.method == "GET":
                courses = Courses.objects.all()
                courses_serializer = CoursesSerializer(courses, many=True)
                return JsonResponse(courses_serializer.data, safe=False)
            elif request.method == "POST":
                logger.info("POST request received")
                course_data = JSONParser().parse(request)
                logger.info(f"Received data: {course_data}")
                courses_serializer = CoursesSerializer(data=course_data)
                if courses_serializer.is_valid():
                    courses_serializer.save()
                    logger.info("Saved successfully")
                    return JsonResponse("Added Successfully", safe=False)
                logger.error(
                    f"POST request validation failed: {courses_serializer.errors}"
                )
                return JsonResponse("Failed to Add", safe=False)
            elif request.method == "PUT":
                course_data = JSONParser().parse(request)
                course = Courses.objects.get(CourseId=course_data["CourseId"])
                courses_serializer = CoursesSerializer(course, data=course_data)
                if courses_serializer.is_valid():
                    courses_serializer.save()
                    return JsonResponse("Updated Successfully", safe=False)
                logger.error(
                    f"PUT request validation failed: {courses_serializer.errors}"
                )
                return JsonResponse("Failed to Update")
            elif request.method == "DELETE":
                course = Courses.objects.get(CourseId=id)
                course.delete()
                return JsonResponse("Deleted Successfully", safe=False)
        except PyMongoError as e:
            logger.exception("PyMongoError occurred in courseApi")
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)  # Wait for a second before retrying
                continue
            return JsonResponse(f"Database Error: {str(e)}", safe=False)
        except Exception as e:
            logger.exception("Exception occurred in courseApi")
            return JsonResponse(f"Error: {str(e)}", safe=False)
        break
    return JsonResponse("Failed after retries", safe=False)
