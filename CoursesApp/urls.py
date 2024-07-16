from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/", views.courseApi, name="courseApi"),
    path("course/<int:id>/", views.courseApi, name="courseApi"),
]
