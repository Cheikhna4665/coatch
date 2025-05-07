from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentaireViewSet

router = DefaultRouter()
router.register(r'', CommentaireViewSet)  # base: /commentaires/

urlpatterns = [
    path('', include(router.urls)),
]
