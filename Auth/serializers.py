from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        token['role'] = user.role
        token['committee'] = user.committee
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        data['committee'] = self.user.committee

        return data
    

class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'committee']
        read_only_fields = fields