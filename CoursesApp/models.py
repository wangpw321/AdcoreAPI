from django.db import models

# Create your models here.


class Courses(models.Model):
    CourseId = models.AutoField(primary_key=True)
    University = models.CharField(max_length=100)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    CourseName = models.CharField(max_length=50)
    CourseDescription = models.CharField(max_length=500)
    StartDate = models.DateField()
    EndDate = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Currency = models.CharField(max_length=10)

    class Meta:
        db_table = "coursesapp_courses"
        
    class Meta:
        db_table = 'normalized_data'
