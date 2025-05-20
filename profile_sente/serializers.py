from rest_framework import serializers
from .models import profile_sente

class ProfileSenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile_sente
        fields = '__all__'
