from users.models import Profile
from .serializers import ProfileSerializer
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView


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


class ProfileByUsername(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        try:
            return Profile.objects.select_related("user").get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound(f"No profile found for username: {username}")


