from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, permissions
from .serializers import CustomTokenObtainPairSerializer, MemberSerializer
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