
from django.db import models
from accounts.models import Utilisateur
from django.contrib.auth.models import User

class profile_sente(models.Model):
    # Lien avec l'utilisateur (si authentifié)
    user = models.OneToOneField(
            Utilisateur, 
            on_delete=models.CASCADE,
            related_name='employer_profile_sente',
            limit_choices_to={'role': 'employe'}
)
    
    # Section 1 : Informations générales
    GOAL_CHOICES = [
        ('weight_loss', 'Perte de poids'),
        ('muscle_gain', 'Renforcement musculaire'),
        ('cardio', 'Amélioration cardio'),
        ('competition', 'Préparation à une compétition'),
        ('other', 'Autre'),
    ]
    sport_goal = models.CharField(
        max_length=50,
        choices=GOAL_CHOICES,
        verbose_name="Objectif sportif"
    )
    current_activity_level = models.CharField(
        max_length=50,
        verbose_name="Niveau d'activité actuel"
    )

    
    # Section 2 : Antécédents médicaux
    recent_injuries = models.TextField(
        blank=True,
        null=True,
        verbose_name="Blessures récentes"
    )
    chronic_diseases = models.TextField(
        blank=True,
        null=True,
        verbose_name="Maladies chroniques"
    )
    allergies = models.TextField(
        blank=True,
        null=True,
        verbose_name="Allergies"
    )
    
    # Section 3 : Données physiques
    weight = models.FloatField(
        verbose_name="Poids (kg)",
        blank=True,
        null=True
    )
    height = models.FloatField(
        verbose_name="Taille (cm)",
        blank=True,
        null=True
    )
    
    # Section 4 : Recommandations
    recommended_activities = models.TextField(
        blank=True,
        null=True,
        verbose_name="Activités conseillées"
    )
   
    needs_coaching = models.BooleanField(
        default=False,
        verbose_name="Besoin d'un encadrement"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return f"Profil Fitness de {self.user.username if self.user else 'Anonyme'}"