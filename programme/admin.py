from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ProgrammeSportif

@admin.register(ProgrammeSportif)
class ProgrammeSportifAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'objectif', 'frequence', 'coach', 'employe')
    search_fields = ('titre', 'objectif')
    list_filter = ('frequence',)
