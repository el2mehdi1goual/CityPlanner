from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class ProjetUrbain(models.Model):
    """
    Modèle représentant un projet urbain de planification
    """
    BUDGET_CHOICES = [
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('élevé', 'Élevé'),
    ]
    
    PRIORITE_CHOICES = [
        ('logements', 'Logements'),
        ('espaces_verts', 'Espaces verts'),
        ('services_publics', 'Services publics'),
        ('équilibré', 'Équilibré'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    nombre_familles = models.IntegerField(validators=[MinValueValidator(1)])
    taille_moyenne_famille = models.IntegerField(validators=[MinValueValidator(1)])
    surface_terrain = models.FloatField(validators=[MinValueValidator(1)])  # en hectares
    niveau_budget = models.CharField(max_length=10, choices=BUDGET_CHOICES)
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Projet Urbain'
        verbose_name_plural = 'Projets Urbains'
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"
    
    @property
    def population_totale(self):
        """Calcule la population totale estimée"""
        return self.nombre_familles * self.taille_moyenne_famille


class PropositionAmenagement(models.Model):
    """
    Modèle représentant une proposition d'aménagement urbain générée
    """
    projet = models.OneToOneField(ProjetUrbain, on_delete=models.CASCADE, related_name='proposition')
    nombre_logements = models.IntegerField()
    nombre_ecoles = models.IntegerField()
    nombre_centres_sante = models.IntegerField()
    nombre_marches = models.IntegerField()
    surface_espaces_verts = models.FloatField()  # en hectares
    surface_routes = models.FloatField()  # en hectares
    description = models.TextField()
    date_generation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Proposition d\'aménagement'
        verbose_name_plural = 'Propositions d\'aménagement'
    
    def __str__(self):
        return f"Proposition pour {self.projet.titre}"


class ImageGeneree(models.Model):
    """
    Modèle représentant les prompts d'images générées pour un projet
    """
    projet = models.ForeignKey(ProjetUrbain, on_delete=models.CASCADE, related_name='images_generees')
    prompt = models.TextField()
    url_image = models.URLField(blank=True, null=True)
    date_generation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_generation']
        verbose_name = 'Image générée'
        verbose_name_plural = 'Images générées'
    
    def __str__(self):
        return f"Image pour {self.projet.titre}"


class HistoriqueProjet(models.Model):
    """
    Modèle représentant l'historique des actions sur un projet
    """
    ACTION_CHOICES = [
        ('creation', 'Création du projet'),
        ('modification', 'Modification du projet'),
        ('suppression', 'Suppression du projet'),
        ('proposition_generee', 'Proposition générée'),
        ('proposition_regeneree', 'Proposition regénérée'),
        ('prompt_genere', 'Prompt image généré'),
    ]
    
    projet = models.ForeignKey(ProjetUrbain, on_delete=models.CASCADE, related_name='historique')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    description = models.TextField()
    date_action = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_action']
        verbose_name = 'Historique du projet'
        verbose_name_plural = 'Historiques des projets'
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.projet.titre} ({self.date_action})"
