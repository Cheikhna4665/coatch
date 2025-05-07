from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Commentaire

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'programme', 'date', 'status', 'profilsante')
    search_fields = ('status', 'profilsite')
    list_filter = ('status',)

