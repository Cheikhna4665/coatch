from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminGlobalViewSet, CoachViewSet, AdminEntrepriseViewSet, EmployerViewSet, LoginWithOTPView, VerifyOTPView
)

router = DefaultRouter()
router.register(r'admins-global', AdminGlobalViewSet)
router.register(r'coachs', CoachViewSet)
router.register(r'admins-entreprise', AdminEntrepriseViewSet)
router.register(r'employes', EmployerViewSet)

urlpatterns = [
    path('', include(router.urls)),
       path('auth/login-otp/', LoginWithOTPView.as_view()),
    path('auth/verify-otp/', VerifyOTPView.as_view()),
]
