from django.db import models
from django.contrib.auth.models import AbstractUser
# Custom user model to extend Django's default user model


class User(AbstractUser):
    """
    Custom user model that extends Django's default user model.
    This allows for future extensions, such as adding additional fields.
    """
    pass  # Inherit all fields from AbstractUser, which includes username, password, first_name, last_name, etc.
    # You can add additional fields here if needed
    email = models.EmailField(unique=True)  # Ensure email is unique
