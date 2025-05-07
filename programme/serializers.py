from rest_framework import serializers
from .models import ProgrammeSportif

class ProgrammeSportifSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgrammeSportif
        fields = '__all__'
