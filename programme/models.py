from django.db import models

# Create your models here.
from django.db import models
from accounts.models import Coach, Employer

class ProgrammeSportif(models.Model):
    titre = models.CharField(max_length=200)
    objectif = models.TextField()
    description = models.TextField()
    duree = models.DateTimeField()

    frequence = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    employe = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre
