from users.models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics


class ProfileDetail(generics.RetrieveAPIView):
    """
    API view to retrieve a specific user profile by its primary key (pk).
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    API view to retrieve a list of all profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileUpdate(generics.UpdateAPIView):
    """
    API view to update a profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
