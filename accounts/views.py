from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import authenticate
from .models import  Utilisateur
from .models import AdminGlobal, Coach, AdminEntreprise, Employer
from .serializers import (
    AdminGlobalSerializer, CoachSerializer, AdminEntrepriseSerializer, EmployerSerializer, MyTokenObtainPairSerializer
)

import random
from django.core.mail import send_mail

from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

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
            return Response({'detail': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        elif not user.check_password(password):
            return Response({'detail': 'Mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_verified:
            refresh = MyTokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),  # This will now contain your claims
            })
        
        send_otp_email(user)
        return Response({'detail': 'OTP envoyé à votre email'}, status=status.HTTP_200_OK)
    
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = Utilisateur.objects.filter(email=email).first()
        
        if user and user.otp_code == otp and user.otp_code != None:
            user.is_verified = True
            user.otp_code = None
            user.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({'detail': 'OTP invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)

class SendOTPReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Utilisateur.objects.get(email=email)
            send_otp_email(user)
            return Response({'message': 'OTP envoyé à votre email'}, status=status.HTTP_200_OK)
        except Utilisateur.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordWithOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        try:
            user = Utilisateur.objects.get(email=email)

            # Validate OTP expiration (e.g., valid for 10 minutes)
            if (user.otp_code != otp or 
                timezone.now() > user.otp_created_at + timedelta(minutes=10)):
                return Response({'error': 'OTP invalide ou expiré'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.otp_code = None
            user.otp_created_at = None
            user.save()

            # Optionally return new tokens after password reset
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Mot de passe réinitialisé avec succès',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except Utilisateur.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, 
                          status=status.HTTP_404_NOT_FOUND)
        