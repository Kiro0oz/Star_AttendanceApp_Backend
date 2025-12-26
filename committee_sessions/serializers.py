from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'committee', 'name', 'start_time', 'end_time', 'location', 'instructor', 'manual_code']
        read_only_fields = ['committee']

class MemberSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'start_time', 'end_time', 'location', 'instructor']
        read_only_fields = fields

