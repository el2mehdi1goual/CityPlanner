from django.contrib import admin
from .models import ProjetUrbain, PropositionAmenagement, ImageGeneree, HistoriqueProjet

@admin.register(ProjetUrbain)
class ProjetUrbainAdmin(admin.ModelAdmin):
    list_display = ('titre', 'utilisateur', 'nombre_familles', 'niveau_budget', 'date_creation')
    list_filter = ('niveau_budget', 'priorite', 'date_creation')
    search_fields = ('titre', 'utilisateur__username')
    readonly_fields = ('date_creation', 'date_modification')

@admin.register(PropositionAmenagement)
class PropositionAmenagementAdmin(admin.ModelAdmin):
    list_display = ('projet', 'nombre_logements', 'nombre_ecoles', 'date_generation')
    list_filter = ('date_generation',)
    search_fields = ('projet__titre',)
    readonly_fields = ('date_generation', 'date_modification')

@admin.register(ImageGeneree)
class ImageGenereeAdmin(admin.ModelAdmin):
    list_display = ('projet', 'date_generation')
    list_filter = ('date_generation',)
    search_fields = ('projet__titre',)
    readonly_fields = ('date_generation',)

@admin.register(HistoriqueProjet)
class HistoriqueProjetAdmin(admin.ModelAdmin):
    list_display = ('projet', 'action', 'date_action')
    list_filter = ('action', 'date_action')
    search_fields = ('projet__titre',)
    readonly_fields = ('date_action',)
