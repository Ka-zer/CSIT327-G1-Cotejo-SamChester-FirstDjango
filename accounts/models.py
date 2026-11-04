from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
   
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        ADMIN = "ADMIN", "Administrator"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"

   
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.STUDENT
    )
    course = models.CharField(max_length=100, blank=True)