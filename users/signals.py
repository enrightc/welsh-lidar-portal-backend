
from django.contrib.auth import get_user_model
user = get_user_model()
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=user)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the user profile when the user is saved.
    """
    instance.profile.save()