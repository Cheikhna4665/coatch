from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgrammeSportifViewSet

router = DefaultRouter()
router.register(r'', ProgrammeSportifViewSet)  # base: /programmes-sportifs/

urlpatterns = [
    path('', include(router.urls)),
]
