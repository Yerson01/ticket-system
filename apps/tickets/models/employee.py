from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    class Meta:
        default_related_name = 'employees'

    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.first_name
