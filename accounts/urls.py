from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminGlobalViewSet, CoachViewSet, AdminEntrepriseViewSet, EmployerViewSet, LoginWithOTPView,
      VerifyOTPView,SendOTPReset,ResetPasswordWithOTPView
)

router = DefaultRouter()
router.register(r'admins-global', AdminGlobalViewSet)
router.register(r'coachs', CoachViewSet)
router.register(r'admins-entreprise', AdminEntrepriseViewSet)
router.register(r'employes', EmployerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login-otp/', LoginWithOTPView.as_view(), name='login-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/sand-otp/', SendOTPReset.as_view(), name='sand-otp'),
    path('auth/ResetPassword-otp/', ResetPasswordWithOTPView.as_view(), name='ResetPassword-otp'),

]
