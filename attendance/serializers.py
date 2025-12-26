# attendance/serializers.py
from rest_framework import serializers
from .models import AttendanceRecord
from committee_sessions.serializers import MemberSessionSerializer 

class AttendanceHistorySerializer(serializers.ModelSerializer):
    session = MemberSessionSerializer(read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = ['session', 'check_in_time', 'status']