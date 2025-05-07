from rest_framework import serializers
from .models import Entreprise

class Entrepriseserializers(serializers.ModelSerializer):
    class Meta:
        model=Entreprise
        fields ='__all__'