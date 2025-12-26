from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from django.db import models

from .utils import generate_encrypted_qr_data, decrypt_and_validate_qr_data
from .models import AttendanceRecord
from Auth.permissions import IsCommitteeAdmin
from committee_sessions.models import Session
from Auth.models import User
from rest_framework import generics
from .serializers import AttendanceHistorySerializer


class GenerateQRView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        user = request.user
        
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.committee != session.committee:
            return Response({"detail": "User is not authorized for this session's committee."}, status=status.HTTP_403_FORBIDDEN)

        now = timezone.now()
        
        if now < session.start_time:
            return Response({"detail": "Cannot generate QR: Session has not started yet."}, status=status.HTTP_400_BAD_REQUEST)
        if now > session.end_time:
            return Response({"detail": "Cannot generate QR: Session has already ended."}, status=status.HTTP_400_BAD_REQUEST)

        encrypted_data = generate_encrypted_qr_data(
            user_id=user.id, 
            session_id=session.id, 
            committee_id=user.committee
        )
        
        return Response({
            "encrypted_qr_data": encrypted_data,
            "qr_lifetime_seconds": 90, 
            "session_manual_code": session.manual_code 
        })
    

class ScanAndLogAttendanceView(views.APIView):

    permission_classes = [permissions.IsAuthenticated, IsCommitteeAdmin]

    def post(self, request):
        admin = request.user
        encrypted_data = request.data.get('encrypted_data')
        manual_code = request.data.get('manual_code') 
        session_id = request.data.get('session_id') 

        if not session_id:
             return Response({"detail": "Current session ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            current_session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
             return Response({"detail": "Invalid current session ID."}, status=status.HTTP_404_NOT_FOUND)

        if admin.committee != current_session.committee:
             return Response({"detail": "Admin not authorized for this session."}, status=status.HTTP_403_FORBIDDEN)

        member_id_to_log = None

        if encrypted_data:
            validation_result = decrypt_and_validate_qr_data(encrypted_data)

            if not validation_result['valid']:
                return Response({"detail": f"QR validation failed: {validation_result['reason']}"}, status=status.HTTP_400_BAD_REQUEST)

            data = validation_result['data']
            member_id_to_log = data['user_id']
            qr_session_id = data['session_id']
            
            if qr_session_id != current_session.id:
                return Response({"detail": "QR code belongs to a different session."}, status=status.HTTP_400_BAD_REQUEST)
        
        elif manual_code and 'member_identifier' in request.data:
            if manual_code != current_session.manual_code:
                return Response({"detail": "Invalid session manual code."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                identifier = request.data['member_identifier']
                member_user = User.objects.get(
                    models.Q(username=identifier) | models.Q(phone_number=identifier)
                )
                member_id_to_log = member_user.id
            except User.DoesNotExist:
                return Response({"detail": "Member identifier (username/phone) not found."}, status=status.HTTP_404_NOT_FOUND)
        
        else:
             return Response({"detail": "Encrypted data or manual entry details are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member_user = User.objects.get(pk=member_id_to_log)

            if member_user.committee != current_session.committee:
                 return Response({"detail": "Member does not belong to this session's committee."}, status=status.HTTP_403_FORBIDDEN)

            status_check = 'present'
            time_difference = timezone.now() - current_session.start_time
            if time_difference > timedelta(minutes=30): 
                 status_check = 'late'
            
            record, created = AttendanceRecord.objects.update_or_create(
                user=member_user, 
                session=current_session,
                defaults={'status': status_check, 'check_in_time': timezone.now()}
            )
            

            response_data = {
                "member_name": member_user.get_full_name() or member_user.username,
                "member_committee": member_user.get_committee_display(),
                "member_phone": member_user.phone_number,
                "session_name": current_session.name,
                "attendance_status": status_check,
                "logged_time": record.check_in_time,
                "message": "Attendance recorded successfully."
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
             return Response({"detail": "Attendance already logged for this session."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An error occurred during logging: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MemberAttendanceHistoryView(generics.ListAPIView):
    serializer_class = AttendanceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AttendanceRecord.objects.filter(user=user).order_by('-check_in_time')
        return AttendanceRecord.objects.none()