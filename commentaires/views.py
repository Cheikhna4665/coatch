from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Commentaire
from .serializers import CommentaireSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
