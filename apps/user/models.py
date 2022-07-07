from django.db import models
from django.contrib.auth.models import AbstractUser

from repositories.user_managers import CustomUserManager

ROLE_CHOICES = (
    (1, 'user'),
    (2, 'Admin'),
)


class CustomUser(AbstractUser):
    username = None

    name = models.CharField(max_length=50, blank=False)

    mobile_number = models.CharField(max_length=11, blank=False, unique=True)

    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return self.name + self.mobile_number
