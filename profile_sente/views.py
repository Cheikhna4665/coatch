from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import profile_sente
from .serializers import ProfileSenteSerializer

class ProfileSenteViewSet(viewsets.ModelViewSet):
    queryset = profile_sente.objects.all()
    serializer_class = ProfileSenteSerializer
