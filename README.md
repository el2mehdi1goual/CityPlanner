# AI Urban Design Planner

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Description

**AI Urban Design Planner** est une application web intelligente d'aide à la conception urbaine. Elle permet aux urbanistes et aux responsables de projets de développement de créer des plans d'aménagement complets pour les populations relogées, notamment les familles déplacées depuis des habitats informels ou précaires.

L'application génère automatiquement des propositions d'aménagement urbain intelligentes basées sur les paramètres saisis (nombre de familles, taille moyenne, budget, priorités), en respectant les standards internationaux de planification urbaine.

### Objectifs

- 🏘️ Faciliter la planification urbaine pour les projets de relogement
- 🤖 Générer automatiquement des propositions d'aménagement intelligentes
- 📊 Fournir des visualisations et des descriptions détaillées
- 🔒 Assurer la sécurité et la confidentialité des données utilisateurs
- ♿ Créer une interface inclusive et facile à utiliser

## Fonctionnalités principales

### 1. Authentification
- ✅ Inscription et connexion sécurisées
- ✅ Système d'authentification Django User
- ✅ Gestion des sessions utilisateurs
- ✅ Déconnexion

### 2. Tableau de bord
- 📊 Statistiques des projets
- 📈 Nombre total de propositions générées
- 📋 Affichage des derniers projets
- 🆕 Bouton pour créer un nouveau projet

### 3. Gestion des projets urbains
- ➕ Créer un nouveau projet
- ✏️ Modifier un projet
- 🗑️ Supprimer un projet
- 👁️ Consulter les détails complets
- 📋 Lister tous les projets de l'utilisateur

### 4. Génération intelligente de propositions
L'application génère automatiquement une proposition d'aménagement contenant:
- 🏠 Nombre de logements
- 🏫 Nombre d'écoles (1 par 500 habitants min.)
- 🏥 Centres de santé (1 par 1000 habitants min.)
- 🛒 Marchés (1 par 800 habitants min.)
- 🌳 Espaces verts (7-15% selon priorité)
- 🛣️ Routes et voiries (20% du terrain)
- 📝 Description détaillée

### 5. Génération de prompts d'images
- 🖼️ Génération automatique de prompts pour API d'IA
- 📸 Prompts prêts pour Midjourney, DALL-E, Stable Diffusion
- 💾 Historique des prompts générés

### 6. Historique des actions
- 📝 Suivi de toutes les modifications
- ⏱️ Dates et descriptions de chaque action
- 🔍 Historique complet du projet

## Technologies utilisées

- **Backend**: Python 3.8+, Django 4.2
- **Base de données**: MySQL 5.7+
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Framework CSS**: Bootstrap 5
- **Authentification**: Django Auth System
- **Architecture**: Django MVT (Model-View-Template)

## Structure du projet

```
CityPlanner/
├── config/                 # Configuration Django
│   ├── __init__.py
│   ├── settings.py        # Paramètres Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI configuration
├── urban_design/          # Application principale
│   ├── __init__.py
│   ├── admin.py           # Admin Django
│   ├── apps.py            # Configuration app
│   ├── forms.py           # Formulaires Django
│   ├── models.py          # Modèles de données
│   ├── urls.py            # URLs de l'app
│   ├── utils.py           # Utilitaires
│   └── views.py           # Vues
├── templates/             # Templates HTML
│   ├── base.html          # Template de base
│   └── urban_design/      # Templates de l'app
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── projet_list.html
│       ├── projet_form.html
│       ├── projet_detail.html
│       ├── confirm_delete.html
│       ├── 404.html
│       └── 500.html
├── static/                # Fichiers statiques
│   ├── css/
│   │   └── style.css      # Styles personnalisés
│   └── js/
│       └── main.js        # Scripts JavaScript
├── manage.py              # Django CLI
├── requirements.txt       # Dépendances Python
├── .gitignore            # Configuration Git
└── README.md             # Ce fichier
```

## Modèles de données

### ProjetUrbain
- `id`: Identifiant unique
- `utilisateur`: ForeignKey vers User (Django)
- `titre`: Titre du projet
- `description`: Description du projet
- `nombre_familles`: Nombre de familles
- `taille_moyenne_famille`: Taille moyenne des familles
- `surface_terrain`: Superficie du terrain (en hectares)
- `niveau_budget`: Choix (Faible, Moyen, Élevé)
- `priorite`: Choix (Logements, Espaces verts, Services publics, Équilibré)
- `date_creation`: Date de création (auto)
- `date_modification`: Date de modification (auto)

### PropositionAmenagement
- `id`: Identifiant unique
- `projet`: OneToOneField vers ProjetUrbain
- `nombre_logements`: Nombre de logements proposés
- `nombre_ecoles`: Nombre d'écoles
- `nombre_centres_sante`: Nombre de centres de santé
- `nombre_marches`: Nombre de marchés
- `surface_espaces_verts`: Surface des espaces verts
- `surface_routes`: Surface des routes
- `description`: Description détaillée
- `date_generation`: Date de génération
- `date_modification`: Dernière modification

### ImageGeneree
- `id`: Identifiant unique
- `projet`: ForeignKey vers ProjetUrbain
- `prompt`: Prompt pour API d'image
- `url_image`: URL de l'image (optionnel)
- `date_generation`: Date de génération

### HistoriqueProjet
- `id`: Identifiant unique
- `projet`: ForeignKey vers ProjetUrbain
- `action`: Type d'action
- `description`: Description de l'action
- `date_action`: Date de l'action

## Installation et configuration

### Prérequis
- Python 3.8 ou supérieur
- MySQL 5.7 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

### Étapes d'installation

#### 1. Cloner le projet
```bash
git clone <repository-url>
cd CityPlanner
```

#### 2. Créer un environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Configurer MySQL
```sql
-- Créer la base de données
CREATE DATABASE ai_urban_design CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer un utilisateur Django (optionnel)
-- Utiliser root par défaut dans settings.py
```

**Note**: Assurez-vous que MySQL est lancé et accessible à `localhost:3306`

#### 5. Configurer Django
Modifiez `config/settings.py` si nécessaire:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ai_urban_design',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 6. Créer les tables (Migrations)
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Créer un superutilisateur (Admin)
```bash
python manage.py createsuperuser
# Suivez les instructions pour créer votre compte admin
```

#### 8. Lancer le serveur
```bash
python manage.py runserver
```

L'application sera accessible à `http://127.0.0.1:8000`

## Utilisation

### Premier lancement

1. **Créer un compte** : Allez sur `/register/` pour vous inscrire
2. **Se connecter** : Utilisez vos identifiants sur `/login/`
3. **Accéder au dashboard** : Après connexion, vous arrivez sur le tableau de bord
4. **Créer un projet** : Cliquez sur "Nouveau projet"
5. **Générer une proposition** : Une fois le projet créé, générez une proposition d'aménagement
6. **Générer une image** : Généralisez un prompt prêt pour une API d'IA

### Routes principales

| Route | Description |
|-------|-------------|
| `/register/` | Page d'inscription |
| `/login/` | Page de connexion |
| `/logout/` | Déconnexion |
| `/dashboard/` | Tableau de bord |
| `/projets/` | Liste des projets |
| `/projets/ajouter/` | Créer un nouveau projet |
| `/projets/<id>/` | Détails d'un projet |
| `/projets/<id>/modifier/` | Modifier un projet |
| `/projets/<id>/supprimer/` | Supprimer un projet |
| `/projets/<id>/generer-proposition/` | Générer une proposition |
| `/projets/<id>/generer-image-prompt/` | Générer un prompt image |
| `/admin/` | Panneau d'administration |

## Algorithme de génération

La génération de propositions suit les règles suivantes:

```
Nombre de logements = Nombre de familles

Population totale = Nombre de familles × Taille moyenne des familles

Nombre d'écoles = MAX(1, CEIL(Population / 500))
Nombre de centres de santé = MAX(1, CEIL(Population / 1000))
Nombre de marchés = MAX(1, CEIL(Population / 800))

Espaces verts:
- Si priorité = "Espaces verts": 15% du terrain
- Si priorité = "Équilibré": 10% du terrain
- Si priorité = "Logements" ou "Services publics": 7% du terrain

Routes = 20% du terrain
```

## Sécurité

### Authentification
- ✅ Authentification Django User
- ✅ Chiffrement des mots de passe (PBKDF2)
- ✅ Protection CSRF avec tokens
- ✅ Sessions sécurisées

### Autorisations
- ✅ Décorateur `@login_required` sur toutes les vues protégées
- ✅ Vérification de propriété (utilisateur) sur chaque requête
- ✅ Un utilisateur ne peut voir que ses propres projets
- ✅ Un utilisateur ne peut modifier/supprimer que ses propres projets

### Données
- ✅ Validation de tous les inputs
- ✅ Utilisation de l'ORM Django (protection contre les injections SQL)
- ✅ Sanitization des données affichées
- ✅ HTTPS recommandé en production

## Admin Django

Accédez au panneau d'admin à `/admin/`:
- Gestion des utilisateurs
- Gestion des projets
- Gestion des propositions
- Visualisation de l'historique

## Commandes utiles

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver

# Lancer sur un port spécifique
python manage.py runserver 0.0.0.0:8080

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer un app Django
python manage.py startapp app_name

# Shell Django interactif
python manage.py shell

# Vider la base de données
python manage.py flush

# Créer des données de test
python manage.py loaddata fixture.json
```

## Développement

### Ajouter des fonctionnalités

1. **Ajouter un modèle**: Modifiez `urban_design/models.py`
2. **Ajouter une vue**: Modifiez `urban_design/views.py`
3. **Ajouter une URL**: Modifiez `urban_design/urls.py`
4. **Ajouter un template**: Créez un fichier dans `templates/urban_design/`
5. **Faire les migrations**: `python manage.py makemigrations && python manage.py migrate`

### Style de code

- ✅ Suivre PEP 8 pour Python
- ✅ Utiliser des noms de variables explicites
- ✅ Commenter le code complexe
- ✅ Tester avant de pusher

## Amélioration futures

- 🔄 Intégration avec une vraie API IA pour la génération d'images
- 📊 Tableaux et graphiques avancés
- 🌍 Géolocalisation et cartes interactives
- 📄 Export PDF des propositions
- 🔔 Notifications et alertes
- 👥 Gestion des équipes et partage de projets
- 📱 Application mobile
- 🤖 Machine Learning pour les recommandations
- 💾 Sauvegarde automatique dans le cloud

## Dépannage

### Erreur de connexion MySQL
```
Error connecting to database
```
**Solution**: Vérifiez que MySQL est lancé et accessible

### Erreur de migrations
```
django.db.utils.IntegrityError
```
**Solution**: Exécutez `python manage.py migrate` pour appliquer les migrations

### Erreur 404 sur les static files
```
Static files not found
```
**Solution**: Exécutez `python manage.py collectstatic`

## Support et contribution

Pour des questions ou des problèmes, merci de créer une issue sur le dépôt GitHub.

Les contributions sont bienvenues! Veuillez faire un fork du projet et soumettre une pull request.

## Licence

Ce projet est sous la licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Auteur

Créé en 2026 pour la planification urbaine inclusive et durable.

---

**Dernier mise à jour**: Avril 2026
**Version**: 1.0.0
**Statut**: Production