from django.utils import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import authenticate
from .models import  Utilisateur
from .models import AdminGlobal, Coach, AdminEntreprise, Employer
from .serializers import (
    AdminGlobalSerializer, CoachSerializer, AdminEntrepriseSerializer, EmployerSerializer
)

import random
from django.core.mail import send_mail
from datetime import timedelta


def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()
    user.otp_code = otp
    user.otp_created_at = timezone.now()
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
        password = request.data.get('password')
        user = Utilisateur.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'Utilisateur non trouvé'}, status=404)
        elif not user.check_password(password):
            return Response({'detail': 'Password error'}, status=404)
        elif user.is_verified == True:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        send_otp_email(user)
        return Response({'detail': 'OTP envoyé'})

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user1 = Utilisateur.objects.filter(email=email).first()
        if user1 and user1.otp_code == otp:
            user1.is_verified = True
            user1.otp_code = None
            user1.save()
            # Créer un token (JWT ou DRF Token)
            token, created = Token.objects.get_or_create(user=user1)
            return Response({'token': token.key})
        return Response({'detail': 'OTP invalide'}, status=400)




class SendOTPReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Utilisateur.objects.get(email=email)
            send_otp_email(user)
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)
        except Utilisateur.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class ResetPasswordWithOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        try:
            user = Utilisateur.objects.get(email=email)

            # Validate OTP expiration (e.g., valid for 10 minutes)
            if user.otp_code != otp or timezone.now() > user.otp_created_at + timedelta(minutes=10):
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.otp = None
            user.otp_created_at = None
            user.save()

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)