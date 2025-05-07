from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AdminGlobal, Coach, AdminEntreprise, Employer

@admin.register(AdminGlobal)
class AdminGlobalAdmin(admin.ModelAdmin):
    list_display = ('id', 'dateCreation')
    search_fields = ('id',)

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'certification', 'experience')
    search_fields = ('certification',)

@admin.register(AdminEntreprise)
class AdminEntrepriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'poste', 'telephone', 'dateEmbauche')
    search_fields = ('poste', 'telephone')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'poste', 'dateNaissance', 'dateEmbauche')
    search_fields = ('poste',)

