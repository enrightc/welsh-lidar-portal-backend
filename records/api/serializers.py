from rest_framework import serializers
from records.models import Record
import json


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
    polygonCoordinate = serializers.JSONField(required=True, allow_null=False)

    def to_internal_value(self, data):
        """
        Normalise form inputs so that empty strings become None and ensure
        polygonCoordinate is a proper list-of-[lat,lng] pairs even if the
        client sent it as a JSON string (common with multipart/form-data).
        """
        if isinstance(data, dict):
            # 1) Convert empty strings to None across the payload
            data = {
                key: (None if isinstance(value, str) and value.strip() == "" else value)
                for key, value in data.items()
            }
            # 2) If polygonCoordinate is a JSON string, parse it
            pc = data.get("polygonCoordinate")
            if isinstance(pc, str):
                try:
                    data["polygonCoordinate"] = json.loads(pc)
                except Exception:
                    raise serializers.ValidationError({"polygonCoordinate": "Invalid JSON for polygonCoordinate"})
        return super().to_internal_value(data)

    def validate_polygonCoordinate(self, value):
        # Accept tuples but treat everything as list
        if value is None:
            raise serializers.ValidationError("polygonCoordinate is required.")
        if not isinstance(value, (list, tuple)):
            raise serializers.ValidationError("polygonCoordinate must be a list of [lat, lng] pairs.")
        value = list(value)
        if len(value) < 3:
            raise serializers.ValidationError("polygonCoordinate must contain at least three [lat, lng] points.")
        for pt in value:
            if not isinstance(pt, (list, tuple)) or len(pt) != 2:
                raise serializers.ValidationError("Each vertex must be a [lat, lng] pair.")
            try:
                float(pt[0]); float(pt[1])
            except Exception:
                raise serializers.ValidationError("Each vertex must contain two numbers: [lat, lng].")
        return value

    def to_representation(self, instance):
        # Start with the default representation
        rep = super().to_representation(instance)
        # Normalise polygonCoordinate: parse legacy strings into arrays
        val = getattr(instance, "polygonCoordinate", None)
        if isinstance(val, str):
            try:
                rep["polygonCoordinate"] = json.loads(val)
            except Exception:
                rep["polygonCoordinate"] = []
        return rep



    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ['recorded_by']
