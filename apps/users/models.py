from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    status = models.CharField(max_length=30, choices=Status.choices)
    USERNAME_FIELD = ['email']
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'status']

    def __str__(self):
        return self.first_name
