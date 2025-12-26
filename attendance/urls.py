from django.urls import path
from .views import GenerateQRView, ScanAndLogAttendanceView, MemberAttendanceHistoryView

urlpatterns = [
    # Admin Endpoint (QR Scan / Manual Log)
    path('admin/attendance/scan/', ScanAndLogAttendanceView.as_view(), name='admin-scan-log'),
    
    # Member Endpoint (QR Generation)
    path('member/attendance/generate_qr/<int:session_id>/', GenerateQRView.as_view(), name='member-generate-qr'),

    path('member/attendance/history/', MemberAttendanceHistoryView.as_view(), name='member-attendance-history'),
]