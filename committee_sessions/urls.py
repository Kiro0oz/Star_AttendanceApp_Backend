from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AdminSessionViewSet, MemberSessionListView, MemberAllSessionsListView

router = DefaultRouter()
router.register(r'sessions', AdminSessionViewSet, basename='admin-sessions')


urlpatterns = [
    path('member/sessions/', MemberSessionListView.as_view(), name='member-active-sessions'),
    path('member/sessions/all/', MemberAllSessionsListView.as_view(), name='member-all-sessions'),
    path('admin/', include(router.urls)), 
]