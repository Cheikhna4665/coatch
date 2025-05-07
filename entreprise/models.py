from django.db import models

# Create your models here.
from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    theme = models.CharField(max_length=100)
    budgetTotal = models.IntegerField()

    def __str__(self):
        return self.nom

