
from rest_framework import serializers
from .models import AdminGlobal, Coach, AdminEntreprise, Employer

class AdminGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminGlobal
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'


class AdminEntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminEntreprise
        fields = '__all__'


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
