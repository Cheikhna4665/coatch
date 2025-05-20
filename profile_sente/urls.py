from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileSenteViewSet

router = DefaultRouter()
router.register(r'', ProfileSenteViewSet)  # base: /commentaires/

urlpatterns = [
    path('', include(router.urls)),
]
