from django.utils import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from .models import  Utilisateur
from .models import AdminGlobal, Coach, AdminEntreprise, Employer
from .serializers import (
    AdminGlobalSerializer, CoachSerializer, AdminEntrepriseSerializer, EmployerSerializer
)

import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()
    user.otp_code = otp
    user.save()

    send_mail(
        subject='Votre code OTP',
        message=f'Bonjour {user.prenom},\n\nVotre code OTP est : {otp}',
        from_email='noreply@corporatecoach.local',
        recipient_list=[user.email],
        fail_silently=False,
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




class LoginWithOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = Utilisateur.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'Utilisateur non trouvé'}, status=404)
        send_otp_email(user)
        return Response({'detail': 'OTP envoyé'})

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user1 = Utilisateur.objects.filter(email=email).first()
        if user1 and user1.otp_code == otp:
            user1.is_verified = True
            user1.save()
            # Créer un token (JWT ou DRF Token)
            token, created = Token.objects.get_or_create(user=user1)
            return Response({'token': token.key})
        return Response({'detail': 'OTP invalide'}, status=400)
