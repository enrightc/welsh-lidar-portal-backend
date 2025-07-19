from rest_framework import serializers
from users.models import Profile
from records.models import Record
from records.api.serializers import RecordSerializer
from datetime import datetime

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    This serializer handles the conversion of Profile instances to and from JSON format.
    """
    user_records = serializers.SerializerMethodField()
    record_count = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)

    joined_date = serializers.SerializerMethodField()
    last_active = serializers.SerializerMethodField()

    def get_joined_date(self, obj):
        if obj.joined_date:
            return obj.joined_date.strftime('%d/%m/%Y')
        return None

    def get_last_active(self, obj):
        if obj.last_active:
            return obj.last_active.strftime('%d/%m/%Y')
        return None

    def get_user_records(self, obj):
        """
        Returns a list of records associated with the user.
        """
        query = Record.objects.filter(recorded_by=obj.user)
        records_serialized = RecordSerializer(query, many=True)
        return records_serialized.data
    
    def get_record_count(self, obj):
        '''
        Returns the count of records associated with the user.
        '''
        return Record.objects.filter(recorded_by=obj.user).count()

    class Meta:
        model = Profile
        fields = [field.name for field in Profile._meta.fields] + [
            'user_records',
            'record_count',
            'user_username',
            'joined_date',
            'last_active',
        ]
        read_only_fields = ['user']