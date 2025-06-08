from rest_framework import serializers
from records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the Record model.
    This serializer handles the conversion of Record instances to and from JSON format.
    """
    recorded_by = serializers.CharField(source="recorded_by.username", read_only=True)

    class Meta:
        model = Record
        fields = '__all__'  # Include all fields from the Record model