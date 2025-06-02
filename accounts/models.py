from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from entreprise.models import Entreprise

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', False)
        extra_fields.setdefault('role', 'admin_global')

        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser):
    ROLE_CHOICES = [
        ('admin_global', 'Admin Global'),
        ('admin_entreprise', 'Admin Entreprise'),
        ('coach', 'Coach'),
        ('employe', 'Employé'),
    ]

    # Personal Info
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    # Auth Fields
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Timestamps
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    # Additional Info

    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='utilisateur_set',
        related_query_name='utilisateur'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='utilisateur_set',
        related_query_name='utilisateur'
    ) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']

    objects = UtilisateurManager()
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new user being created
        super().save(*args, **kwargs)  # Save the user first
        
        if created:  # Only create profile for new users
            self.create_related_profile()
    
    def create_related_profile(self):
        """Create the appropriate profile based on the user's role"""
        if self.role == 'admin_global' and not hasattr(self, 'Admin_global_profile'):
            AdminGlobal.objects.create(user_id=self)
        elif self.role == 'admin_entreprise' and not hasattr(self, 'admin_entreprise_profile'):
            AdminEntreprise.objects.create(user_id=self)
        elif self.role == 'coach' and not hasattr(self, 'coach_profile'):
            Coach.objects.create(user_id=self, certification="", experience="")
        elif self.role == 'employe' and not hasattr(self, 'employe_profile'):
            Employer.objects.create(user_id=self, poste="", date_embauche="2000-01-01", date_naissance="2000-01-01")
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Utilisateur Global"
        verbose_name_plural = "Utilisateurs Globaux"
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    @property
    def profile(self):
        """Returns the specific profile based on the user's role"""
        if hasattr(self, 'Admin_global_profile'):
            return self.Admin_global_profile
        elif hasattr(self, 'admin_entreprise_profile'):
            return self.admin_entreprise_profile
        elif hasattr(self, 'coach_profile'):
            return self.coach_profile
        elif hasattr(self, 'employe_profile'):
            return self.employe_profile
        return None
    
class AdminGlobal(models.Model):
    user_id = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='Admin_global_profile',
        limit_choices_to={'role': 'admin_global'}
)

    def __str__(self):
        return f"AdminGlobal {self.user_id}"
    
class Coach(models.Model):
    user_id = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE, 
        related_name='coach_profile',
        limit_choices_to={'role': 'coach'}
)
    certification = models.FileField(upload_to='certifications/', null=True, blank=True)
    experience = models.TextField()
    specialites = models.TextField(blank=True)


    def __str__(self):
        return f"Coach {self.user_id}"

class AdminEntreprise(models.Model):
    user_id = models.OneToOneField(
            Utilisateur, 
            on_delete=models.CASCADE,
            related_name='admin_entreprise_profile',
            limit_choices_to={'role': 'admin_entreprise'}
)
    poste = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_embauche = models.DateField(null=True, blank=True)

    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, related_name='admins_entreprise')

    def __str__(self):
        return f"Admin {self.user_id} - {self.entreprise}"

class Employer(models.Model):
    user_id = models.OneToOneField(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='employe_profile',
        limit_choices_to={'role': 'employe'}
)
    date_embauche = models.DateField()
    date_naissance = models.DateField()
    poste = models.CharField(max_length=100)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, related_name='employes')
    
    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employers'
    )
    def __str__(self):
        return f"Employé {self.user_id} - {self.poste}"                                                 