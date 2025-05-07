from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import AdminGlobal, Coach, AdminEntreprise, Employer
from .serializers import (
    AdminGlobalSerializer, CoachSerializer, AdminEntrepriseSerializer, EmployerSerializer
)

class AdminGlobalViewSet(viewsets.ModelViewSet):
    queryset = AdminGlobal.objects.all()
    serializer_class = AdminGlobalSerializer

class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

class AdminEntrepriseViewSet(viewsets.ModelViewSet):
    queryset = AdminEntreprise.objects.all()
    serializer_class = AdminEntrepriseSerializer

class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
