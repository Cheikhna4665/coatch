from django.db import models

# Create your models here.
from django.db import models
from programme.models import ProgrammeSportif

class Commentaire(models.Model):
    programme = models.ForeignKey(ProgrammeSportif, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    commentaires = models.TextField()
    status = models.CharField(max_length=50)
    profilsante = models.FileField(upload_to='profils_sante/', null=True, blank=True)

    def __str__(self):
        return f"Commentaire pour {self.programme}"
