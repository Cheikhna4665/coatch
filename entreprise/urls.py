from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrepriseViewSet

router = DefaultRouter()
router.register(r'', EntrepriseViewSet)  # base: /entreprises/

urlpatterns = [
    path('', include(router.urls)),
]
