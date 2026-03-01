from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", input_formats=["%Y-%m-%d %I:%M %p", "iso-8601"])
    end_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", input_formats=["%Y-%m-%d %I:%M %p", "iso-8601"])

    class Meta:
        model = Session
        fields = ['id', 'committee', 'name', 'level', 'start_time', 'end_time', 'location', 'instructor', 'manual_code']
        read_only_fields = ['committee']
        extra_kwargs = {
            'location': {'required': True, 'allow_null': False, 'allow_blank': False},
            'instructor': {'required': True, 'allow_null': False, 'allow_blank': False},
            'manual_code': {'required': True, 'allow_null': False, 'allow_blank': False},
        }

class MemberSessionSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", input_formats=["%Y-%m-%d %I:%M %p", "iso-8601"])
    end_time = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", input_formats=["%Y-%m-%d %I:%M %p", "iso-8601"])

    class Meta:
        model = Session
        fields = ['id', 'name', 'level', 'start_time', 'end_time', 'location', 'instructor']
        read_only_fields = ['id', 'name', 'level', 'start_time', 'end_time', 'location', 'instructor']

