from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Entreprise

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'theme', 'budgetTotal')
    search_fields = ('nom', 'theme')
