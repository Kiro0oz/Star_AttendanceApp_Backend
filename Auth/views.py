from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, permissions
from .serializers import CustomTokenObtainPairSerializer, MemberSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import User
from .permissions import IsCommitteeAdmin

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


class CommitteeMemberViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommitteeAdmin]

    def get_queryset(self):
        user = self.request.user
        

        if user.is_authenticated and user.role == 'admin' and user.committee:
        
            return User.objects.filter(committee=user.committee).order_by('username')
        
        return User.objects.none()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            return Response({
                "message": "Password reset token generated",
                "uid": uid,
                "token": token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
