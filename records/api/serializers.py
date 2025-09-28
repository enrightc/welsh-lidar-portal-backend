from rest_framework import serializers
from records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the Record model.
    This serializer handles the conversion
    of Record instances to and from JSON format.
    """
    recorded_by = serializers.CharField(
        source="recorded_by.username",
        read_only=True
    )
    recorded_by_user_id = serializers.IntegerField(source='recorded_by.id', read_only=True)

    # PRN is optional; accept "" (empty string) or null and normalise later
    prn = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    site_type_display = serializers.CharField(source='get_site_type_display', read_only=True)
    monument_type_display = serializers.CharField(source='get_monument_type_display', read_only=True)
    period_display = serializers.CharField(source='get_period_display', read_only=True)
    date_recorded = serializers.DateField(format='%d/%m/%Y', read_only=True)

    def to_internal_value(self, data):
        """
        Normalise form inputs so that empty strings become None. This prevents
        crashes when optional fields (e.g., PRN) are sent as "" by the browser.
        Applies to all incoming string fields in the payload.
        """
        if isinstance(data, dict):
            data = {
                key: (None if isinstance(value, str) and value.strip() == "" else value)
                for key, value in data.items()
            }
        return super().to_internal_value(data)


    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ['recorded_by']
