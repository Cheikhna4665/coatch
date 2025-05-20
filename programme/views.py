from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ProgrammeSportif
from .serializers import ProgrammeSportifSerializer

class ProgrammeSportifViewSet(viewsets.ModelViewSet):
    queryset = ProgrammeSportif.objects.all()
    
    serializer_class = ProgrammeSportifSerializer
