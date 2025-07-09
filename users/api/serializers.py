from rest_framework import serializers
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    This serializer handles the conversion of Profile instances to and from JSON format.
    """
    
    class Meta:
        model = Profile
        fields = '__all__'  # Include all fields from the Profile model
        read_only_fields = ['user']  # Make the user field read-only, as it is set automatically