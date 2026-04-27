"""
Tests unitaires pour l'application urban_design
Exécuter avec: python manage.py test
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ProjetUrbain, PropositionAmenagement, ImageGeneree, HistoriqueProjet
from .utils import generer_proposition_amenagement


class UserAuthenticationTest(TestCase):
    """Tests pour l'authentification des utilisateurs"""
    
    def setUp(self):
        """Configuration de base pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_page(self):
        """Test de la page d'inscription"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'urban_design/register.html')
    
    def test_login_page(self):
        """Test de la page de connexion"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'urban_design/login.html')
    
    def test_user_login(self):
        """Test de connexion d'un utilisateur"""
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)
    
    def test_user_logout(self):
        """Test de déconnexion"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class ProjetUrbainTest(TestCase):
    """Tests pour les modèles de projets"""
    
    def setUp(self):
        """Configuration de base"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        self.projet = ProjetUrbain.objects.create(
            utilisateur=self.user,
            titre='Projet Test',
            nombre_familles=100,
            taille_moyenne_famille=5,
            surface_terrain=50,
            niveau_budget='moyen',
            priorite='équilibré'
        )
    
    def test_create_projet(self):
        """Test de création d'un projet"""
        self.assertEqual(self.projet.titre, 'Projet Test')
        self.assertEqual(self.projet.utilisateur, self.user)
        self.assertEqual(self.projet.nombre_familles, 100)
    
    def test_projet_population(self):
        """Test du calcul de la population"""
        self.assertEqual(self.projet.population_totale, 500)
    
    def test_projet_list_view(self):
        """Test de la vue liste des projets"""
        response = self.client.get(reverse('projet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.projet, response.context['projets'])
    
    def test_projet_detail_view(self):
        """Test de la vue détails d'un projet"""
        response = self.client.get(reverse('projet_detail', args=[self.projet.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['projet'], self.projet)


class PropositionAmenagementTest(TestCase):
    """Tests pour la génération de propositions"""
    
    def setUp(self):
        """Configuration de base"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.projet = ProjetUrbain.objects.create(
            utilisateur=self.user,
            titre='Projet Test',
            nombre_familles=1000,
            taille_moyenne_famille=5,
            surface_terrain=100,
            niveau_budget='moyen',
            priorite='équilibré'
        )
    
    def test_generer_proposition(self):
        """Test de génération d'une proposition"""
        donnees = generer_proposition_amenagement(self.projet)
        
        self.assertEqual(donnees['nombre_logements'], 1000)
        self.assertEqual(donnees['nombre_ecoles'], 10)  # 5000/500 = 10
        self.assertEqual(donnees['nombre_centres_sante'], 5)  # 5000/1000 = 5
        self.assertEqual(donnees['nombre_marches'], 7)  # ceil(5000/800) = 7
        self.assertEqual(donnees['surface_espaces_verts'], 10.0)  # 100 * 0.10
        self.assertEqual(donnees['surface_routes'], 20.0)  # 100 * 0.20
    
    def test_proposition_avec_priorite_espaces_verts(self):
        """Test des espaces verts selon priorité"""
        self.projet.priorite = 'espaces_verts'
        donnees = generer_proposition_amenagement(self.projet)
        self.assertEqual(donnees['surface_espaces_verts'], 15.0)  # 15%
    
    def test_proposition_avec_priorite_logements(self):
        """Test des espaces verts selon priorité logements"""
        self.projet.priorite = 'logements'
        donnees = generer_proposition_amenagement(self.projet)
        self.assertEqual(donnees['surface_espaces_verts'], 7.0)  # 7%
    
    def test_create_proposition_in_database(self):
        """Test de création d'une proposition en base"""
        donnees = generer_proposition_amenagement(self.projet)
        proposition = PropositionAmenagement.objects.create(
            projet=self.projet,
            **donnees
        )
        
        self.assertEqual(proposition.nombre_logements, 1000)
        self.assertEqual(proposition.projet, self.projet)


class HistoriqueProjetTest(TestCase):
    """Tests pour l'historique des projets"""
    
    def setUp(self):
        """Configuration de base"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.projet = ProjetUrbain.objects.create(
            utilisateur=self.user,
            titre='Projet Test',
            nombre_familles=100,
            taille_moyenne_famille=5,
            surface_terrain=50,
            niveau_budget='moyen',
            priorite='équilibré'
        )
    
    def test_create_historique_entry(self):
        """Test de création d'une entrée historique"""
        historique = HistoriqueProjet.objects.create(
            projet=self.projet,
            action='creation',
            description='Projet créé'
        )
        
        self.assertEqual(historique.projet, self.projet)
        self.assertEqual(historique.action, 'creation')
    
    def test_historique_ordering(self):
        """Test du tri du l'historique"""
        h1 = HistoriqueProjet.objects.create(
            projet=self.projet,
            action='creation',
            description='Projet créé'
        )
        h2 = HistoriqueProjet.objects.create(
            projet=self.projet,
            action='modification',
            description='Projet modifié'
        )
        
        historique = HistoriqueProjet.objects.filter(projet=self.projet)
        self.assertEqual(historique[0], h2)  # Plus récent d'abord


class SecurityTest(TestCase):
    """Tests de sécurité"""
    
    def setUp(self):
        """Configuration de base"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        self.projet1 = ProjetUrbain.objects.create(
            utilisateur=self.user1,
            titre='Projet User1',
            nombre_familles=100,
            taille_moyenne_famille=5,
            surface_terrain=50,
            niveau_budget='moyen',
            priorite='équilibré'
        )
    
    def test_login_required(self):
        """Test que les pages protégées nécessitent une connexion"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_user_can_only_see_own_projects(self):
        """Test qu'un utilisateur ne peut voir que ses propres projets"""
        self.client.login(username='user2', password='pass2')
        response = self.client.get(reverse('projet_list'))
        self.assertNotIn(self.projet1, response.context['projets'])


if __name__ == '__main__':
    import unittest
    unittest.main()
