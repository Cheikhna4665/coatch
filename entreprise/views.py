from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Entreprise
from .serializers import Entrepriseserializers

class EntrepriseViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.all()
    serializer_class = Entrepriseserializers
