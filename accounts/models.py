from django.db import models

# Create your models here.
from entreprise.models import Entreprise

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    competences = models.TextField(blank=True)

    class Meta:
        abstract = True  # Ne crée pas de table pour Utilisateur

class AdminGlobal(Utilisateur):
    dateCreation = models.DateTimeField(auto_now_add=True)

class Coach(Utilisateur):
    certification = models.TextField()
    experience = models.TextField()

    def __str__(self):
        return f"{self.nom}"

class AdminEntreprise(Utilisateur):
    poste = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    dateEmbauche = models.DateField()
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)

class Employer(Utilisateur):
    dateEmbauche = models.DateField()
    dateNaissance = models.DateField()
    poste = models.CharField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.nom}"
