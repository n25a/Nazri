# Django libs
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    """
    Custom user model manager where mobile_number is the unique identifiers
    for authentication.
    """

    def create_user(self, mobile_number, name, password, **extra_fields):
        """
        Create and save a User with the given name
        and mobile_number and password.
        """
        if not name:
            raise ValueError(_('The name must be set'))

        if not mobile_number:
            raise ValueError(_('The Mobile Number must be set'))

        user = self.model(
            name=name, mobile_number=mobile_number, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given mobile number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mobile_number, password, **extra_fields)
