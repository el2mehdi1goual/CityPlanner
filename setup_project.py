"""
Script de configuration et de test initial pour AI Urban Design Planner
Exécutez: python setup_project.py
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from urban_design.models import ProjetUrbain, HistoriqueProjet


def print_header(text):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_requirements():
    """Vérifie les dépendances"""
    print_header("Vérification des dépendances")
    
    try:
        import django
        print("✓ Django installé")
    except ImportError:
        print("✗ Django non installé")
        return False
    
    try:
        import MySQLdb
        print("✓ MySQLdb installé")
    except ImportError:
        print("✗ MySQLdb non installé")
        return False
    
    return True


def run_migrations():
    """Exécute les migrations Django"""
    print_header("Exécution des migrations")
    
    try:
        call_command('migrate', verbosity=1)
        print("\n✓ Migrations appliquées avec succès")
        return True
    except Exception as e:
        print(f"\n✗ Erreur lors des migrations: {str(e)}")
        return False


def create_superuser():
    """Crée un superutilisateur de test"""
    print_header("Création d'un compte de test")
    
    if User.objects.filter(username='admin').exists():
        print("✓ Le compte admin existe déjà")
        return True
    
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✓ Superutilisateur créé")
        print("  Identifiants: admin / admin123")
        return True
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        return False


def create_sample_data():
    """Crée des données d'exemple"""
    print_header("Création de données d'exemple")
    
    try:
        admin = User.objects.get(username='admin')
        
        if ProjetUrbain.objects.filter(utilisateur=admin).exists():
            print("✓ Données d'exemple existent déjà")
            return True
        
        # Créer un projet d'exemple
        projet = ProjetUrbain.objects.create(
            utilisateur=admin,
            titre="Projet de Relogement - Zone A",
            description="Projet pilote de planification urbaine pour 500 familles",
            nombre_familles=500,
            taille_moyenne_famille=5,
            surface_terrain=75,
            niveau_budget='moyen',
            priorite='équilibré'
        )
        
        # Ajouter une entrée historique
        HistoriqueProjet.objects.create(
            projet=projet,
            action='creation',
            description=f'Projet "{projet.titre}" créé automatiquement'
        )
        
        print("✓ Données d'exemple créées")
        print(f"  Projet: {projet.titre}")
        print(f"  ID: {projet.pk}")
        return True
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        return False


def check_database():
    """Vérifie la connexion à la base de données"""
    print_header("Vérification de la base de données")
    
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✓ Connexion à la base de données établie")
        print(f"  Base de données: {connection.settings_dict['NAME']}")
        print(f"  Host: {connection.settings_dict['HOST']}")
        return True
    except Exception as e:
        print(f"✗ Erreur de connexion: {str(e)}")
        return False


def display_summary():
    """Affiche un résumé"""
    print_header("Configuration terminée ✓")
    
    print("Prochaines étapes:")
    print("\n1. Lancer le serveur:")
    print("   python manage.py runserver")
    print("\n2. Accéder à l'application:")
    print("   http://127.0.0.1:8000")
    print("\n3. Se connecter avec:")
    print("   Utilisateur: admin")
    print("   Mot de passe: admin123")
    print("\n4. Accéder à l'admin Django:")
    print("   http://127.0.0.1:8000/admin/")
    print("\n" + "="*60 + "\n")


def main():
    """Fonction principale"""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║     AI Urban Design Planner - Configuration Initiale     ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Vérifications
    if not check_requirements():
        print("\n✗ Veuillez installer les dépendances manquantes")
        sys.exit(1)
    
    if not check_database():
        print("\n✗ Impossible de se connecter à la base de données")
        print("  Vérifiez:")
        print("  - MySQL est lancé")
        print("  - La base de données ai_urban_design existe")
        print("  - Les paramètres dans config/settings.py")
        sys.exit(1)
    
    # Configuration
    if not run_migrations():
        print("\n✗ Erreur lors des migrations")
        sys.exit(1)
    
    if not create_superuser():
        print("\n⚠ Impossible de créer le superutilisateur")
    
    if not create_sample_data():
        print("\n⚠ Impossible de créer les données d'exemple")
    
    # Afficher le résumé
    display_summary()


if __name__ == '__main__':
    main()
