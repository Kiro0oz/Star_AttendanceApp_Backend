from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
from .models import Session
from .serializers import SessionSerializer, MemberSessionSerializer
from Auth.permissions import IsCommitteeAdmin, IsAdminOfTargetCommittee


class AdminSessionViewSet(viewsets.ModelViewSet):

    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommitteeAdmin, IsAdminOfTargetCommittee]
    
    def get_queryset(self):
        # Admins can view all sessions related to their own committee.
        user = self.request.user
        if user.is_authenticated and user.committee:
            return Session.objects.filter(committee=user.committee).order_by('-start_time')
        return Session.objects.none()

    def perform_create(self, serializer):
        admin_committee = self.request.user.committee
        serializer.save(committee=admin_committee)

    @action(detail=False, methods=['get'])
    def active_sessions(self, request):
        now = timezone.now()
        # self.get_queryset() already filters by the admin's committee
        queryset = self.get_queryset().filter(start_time__lte=now, end_time__gte=now)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance_count(self, request, pk=None):
        """
        Returns the number of verified attendees (present or late) for a specific session.
        """
        session = self.get_object()
        # Count only present or late records as "attended"
        count = session.attendances.filter(status__in=['present', 'late']).count()
        
        return Response({
            "session_id": session.id,
            "session_name": session.name,
            "attendance_count": count,
            "is_ended": session.end_time < timezone.now()
        })


class MemberSessionListView(generics.ListAPIView):

    serializer_class = MemberSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        if user.is_authenticated and user.committee:
            queryset = Session.objects.filter(committee=user.committee)
            
            # (Session Visibility Control)
            # Session is active if now >= start_time AND now <= end_time.
            queryset = queryset.filter(start_time__lte=now, end_time__gte=now).order_by('start_time')
            
            # For Sessions was ended for today also:
            # sessions = Session.objects.filter(start_time__date=now.date(), committee=user.committee)
            
            return queryset
        
        return Session.objects.none()
    

class MemberAllSessionsListView(generics.ListAPIView):
    serializer_class = MemberSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_authenticated and user.committee:
            return Session.objects.filter(committee=user.committee).order_by('-start_time')
        
        return Session.objects.none()


class CommitteeSessionsListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        committee_name = self.kwargs['committee_name']
        return Session.objects.filter(committee=committee_name).order_by('-start_time')
