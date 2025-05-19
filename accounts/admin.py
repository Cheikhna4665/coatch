from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminGlobal, Coach, AdminEntreprise, Employer, Utilisateur

class CustomUserAdmin(UserAdmin):
    # Use fields from your Utilisateur model
    list_display = ('email', 'nom', 'prenom', 'role', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('role', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('-date_creation',)
    readonly_fields = ('date_creation', 'date_modification')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('nom', 'prenom', 'role')}),
        
        ('Important dates', {'fields': ('date_creation', 'date_modification')}),
        ('Authentication', {'fields': ('otp_code',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register your models here
admin.site.register(Utilisateur, CustomUserAdmin)

@admin.register(AdminGlobal)
class AdminGlobalAdmin(admin.ModelAdmin):
    list_display = ('user_id',)
    raw_id_fields = ('user_id',)  # Better for performance with OneToOne relationships

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'certification', 'experience')
    raw_id_fields = ('user_id',)

@admin.register(AdminEntreprise)
class AdminEntrepriseAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'poste', 'entreprise')
    raw_id_fields = ('user_id', 'entreprise')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'poste', 'entreprise')
    raw_id_fields = ('user_id', 'entreprise')