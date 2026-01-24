from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import CustomTokenObtainPairView, CommitteeMemberViewSet, ChangePasswordView


router = DefaultRouter()
router.register(r'members', CommitteeMemberViewSet, basename='committee-members')


urlpatterns = [

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    path('admin/', include(router.urls)), 
]