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


class Profile(models.Model):
    """
    Profile model to store additional user information.
    This can be linked to the User model via a OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(
            blank=True,
            max_length=500
        )  # Optional biography field
    location = models.CharField(
            max_length=100,
            blank=True,
            null=True
        )  # Optional location field
    expertise_level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("enthusiast", "Enthusiast"),
            ("researcher", "Researcher"),
            ("professional", "Professional"),
        ],
        default="beginner"
    )  # Optional expertise level field
    organisation = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Social media links
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    bluesky = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    joined_date = models.DateTimeField(auto_now_add=True)  # When the profile was created
    last_active = models.DateTimeField(
            auto_now=True
        )  # Updates every time the profile is saved

    def __str__(self):
        return f"{self.user.username}'s Profile"
