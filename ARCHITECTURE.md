# Architecture et Structure du Code

## 📁 Organisation des fichiers

```
CityPlanner/
├── 📁 config/                      # Configuration Django principale
│   ├── settings.py                # Paramètres Django
│   ├── urls.py                    # URLs racines
│   ├── wsgi.py                    # Configuration WSGI
│   └── __init__.py
│
├── 📁 urban_design/               # Application principale Django
│   ├── models.py                  # Modèles de données (ORM)
│   ├── views.py                   # Vues (logique métier)
│   ├── forms.py                   # Formulaires Django
│   ├── urls.py                    # URLs de l'application
│   ├── admin.py                   # Configuration Admin Django
│   ├── apps.py                    # Configuration de l'app
│   ├── utils.py                   # Utilitaires (génération)
│   ├── tests.py                   # Tests unitaires
│   └── __init__.py
│
├── 📁 templates/                  # Templates HTML
│   ├── base.html                  # Template de base (navbar, footer)
│   └── 📁 urban_design/           # Templates de l'application
│       ├── login.html             # Authentification
│       ├── register.html
│       ├── dashboard.html         # Tableau de bord
│       ├── projet_list.html       # Liste des projets
│       ├── projet_form.html       # Formulaire (créer/modifier)
│       ├── projet_detail.html     # Détails d'un projet
│       ├── confirm_delete.html    # Confirmation suppression
│       ├── 404.html               # Page d'erreur
│       └── 500.html
│
├── 📁 static/                     # Fichiers statiques
│   ├── 📁 css/
│   │   └── style.css              # Styles personnalisés
│   └── 📁 js/
│       └── main.js                # Scripts JavaScript
│
├── 📁 migrations/                 # Migrations Django (auto-générées)
│
├── manage.py                      # CLI Django
├── setup_project.py               # Script de configuration initiale
├── requirements.txt               # Dépendances Python
├── .env.example                   # Modèle de configuration
├── .gitignore                     # Fichiers à ignorer en Git
├── README.md                      # Documentation principale
├── INSTALLATION.md                # Guide d'installation
├── FONCTIONNALITES.md            # Guide des fonctionnalités
└── ARCHITECTURE.md                # Ce fichier
```

---

## 🏗️ Architecture MVT Django

L'application suit le pattern **Model-View-Template** de Django:

```
HTTP Request
    ↓
URL Router (urls.py)
    ↓
View (views.py) ← Business Logic
    ↓
    ├→ Model (models.py) ← Database
    │
    └→ Template (*.html) ← HTML Rendering
    ↓
HTTP Response
```

---

## 📊 Modèles de données (models.py)

### Diagramme des relations

```
User (Django)
  ↓
  ├─→ ProjetUrbain (1:N)
  │    ↓
  │    ├─→ PropositionAmenagement (1:1)
  │    ├─→ ImageGeneree (1:N)
  │    └─→ HistoriqueProjet (1:N)
```

### ProjetUrbain
**Champs:**
- `id` (auto-généré)
- `utilisateur` → User (ForeignKey)
- `titre` (CharField)
- `description` (TextField)
- `nombre_familles` (IntegerField)
- `taille_moyenne_famille` (IntegerField)
- `surface_terrain` (FloatField)
- `niveau_budget` (CharField + choices)
- `priorite` (CharField + choices)
- `date_creation` (DateTimeField, auto)
- `date_modification` (DateTimeField, auto)

**Propriétés:**
- `population_totale` (computed property)

---

## 🔧 Utilitaires (utils.py)

### Fonctions principales

#### `generer_proposition_amenagement(projet)`
Génère une proposition basée sur:
- Paramètres du projet
- Règles de calcul standardisées
- Priorité du projet

Retourne: `dict` avec tous les paramètres

#### `generer_description_proposition(...)`
Crée une description textuelle complète et formatée

#### `generer_prompt_image(proposition)`
Génère un prompt prêt pour API IA (Midjourney, DALL-E, etc.)

---

## 👁️ Vues (views.py)

### Vues d'authentification
- `register_view()` - GET/POST - Page inscription
- `login_view()` - GET/POST - Page connexion
- `logout_view()` - GET - Déconnexion

### Vues du dashboard
- `dashboard_view()` - GET - Tableau de bord avec statistiques

### Vues des projets (CRUD)
- `projet_list_view()` - GET - Liste tous les projets
- `projet_create_view()` - GET/POST - Crée un projet
- `projet_detail_view()` - GET - Détails d'un projet
- `projet_update_view()` - GET/POST - Modifie un projet
- `projet_delete_view()` - GET/POST - Supprime un projet

### Vues de génération
- `generer_proposition_view()` - POST - Génère/regénère une proposition
- `generer_prompt_image_view()` - POST - Génère un prompt d'image

### Vues d'erreur
- `page_not_found_view()` - 404
- `server_error_view()` - 500

---

## 📋 Formulaires (forms.py)

### RegisterForm
Champs: username, email, password, password_confirm
Validations: Les mots de passe doivent correspondre

### LoginForm
Champs: username, password
Validations: Basique

### ProjetUrbainForm
Champs: titre, description, nombre_familles, taille_moyenne_famille, surface_terrain, niveau_budget, priorite
Widget: TextInput, TextArea, NumberInput, Select
Validation: Django gère tout

---

## 🔀 URLs (urls.py)

**Format de pattern:**
```python
path('route/', view_function, name='nom_route')
```

**Routes principales:**
- `/register/` → register_view
- `/login/` → login_view
- `/logout/` → logout_view
- `/dashboard/` → dashboard_view
- `/projets/` → projet_list_view
- `/projets/ajouter/` → projet_create_view
- `/projets/<id>/` → projet_detail_view
- `/projets/<id>/modifier/` → projet_update_view
- `/projets/<id>/supprimer/` → projet_delete_view
- `/projets/<id>/generer-proposition/` → generer_proposition_view
- `/projets/<id>/generer-image-prompt/` → generer_prompt_image_view

---

## 🎨 Templates (HTML)

### Hiérarchie des templates

```
base.html (navbar, footer, structure principale)
├── login.html (page de connexion)
├── register.html (page d'inscription)
├── dashboard.html (tableau de bord)
├── projet_list.html (liste des projets)
├── projet_form.html (formulaire créer/modifier)
├── projet_detail.html (détails complet)
├── confirm_delete.html (confirmation suppression)
├── 404.html (page non trouvée)
└── 500.html (erreur serveur)
```

### Blocs personnalisables dans base.html

```django
{% block title %} - Titre de la page
{% block content %} - Contenu principal
{% block extra_css %} - CSS additif
{% block extra_js %} - JS additif
```

### Tags Jinja2 utilisés

```django
{% if condition %}
{% for item in items %}
{% url 'nom_route' %}
{% csrf_token %}
{% load static %}
```

---

## 🔐 Sécurité

### Authentification
```python
@login_required(login_url='login')
def protected_view(request):
    pass
```

### Vérification de propriété
```python
projet = get_object_or_404(ProjetUrbain, pk=pk, utilisateur=request.user)
```

### Protection CSRF
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### Validation des inputs
Django ORM + formulaires Django = protection automatique

---

## 🧪 Tests (tests.py)

### Classes de tests

**UserAuthenticationTest**
- Test inscription
- Test connexion
- Test déconnexion

**ProjetUrbainTest**
- Test création
- Test calculs
- Test permissions

**PropositionAmenagementTest**
- Test génération
- Test calculs selon priorité

**SecurityTest**
- Test authentification requise
- Test propriété des données

### Exécuter les tests

```bash
python manage.py test
python manage.py test urban_design.tests.UserAuthenticationTest
python manage.py test --verbose
```

---

## 🎯 Flux utilisateur

### Première visite
```
Visiteur
├─ Accueil (redirect vers login)
├─ Inscription (register/)
├─ Confirmation automatique
└─ Dashboard
```

### Création de projet
```
Utilisateur connecté
├─ Dashboard
├─ Bouton "Nouveau projet"
├─ Remplir formulaire
├─ POST création
├─ Entrée historique "création"
└─ Vue détails du projet
```

### Génération de proposition
```
Projet créé
├─ Vue détails
├─ Bouton "Générer proposition"
├─ Calculs utils.py
├─ Création PropositionAmenagement
├─ Entrée historique "proposition_generee"
└─ Affichage résultats
```

---

## 📦 Dépendances

```
Django==4.2.0              # Framework Web
mysqlclient==2.2.0         # Driver MySQL
python-decouple==3.8       # Gestion variables d'environnement
```

---

## 🔄 Cycle de vie d'une requête

### Exemple: GET /projets/1/

1. **URL Routing** (config/urls.py)
   - Identifie `projet_detail_view` avec `pk=1`

2. **View** (urban_design/views.py)
   - Récupère l'utilisateur de `request.user`
   - Query: `ProjetUrbain.objects.get(pk=1, utilisateur=user)`
   - Récupère les propositions, images, historique
   - Crée context dict

3. **Template** (urban_design/projet_detail.html)
   - Boucles sur les données
   - Génère HTML avec Jinja2

4. **Response**
   - HTTP 200 avec HTML rendu

---

## 🛠️ Extension du projet

### Ajouter une nouvelle fonctionnalité

1. **Modèle** (models.py)
   ```python
   class NouveauModele(models.Model):
       ...
   ```

2. **Vue** (views.py)
   ```python
   def nouvelle_vue(request):
       ...
   ```

3. **URL** (urls.py)
   ```python
   path('route/', views.nouvelle_vue, name='nom')
   ```

4. **Template**
   ```django
   {% extends "base.html" %}
   {% block content %}...{% endblock %}
   ```

5. **Migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## 📚 Ressources

- [Documentation Django officielle](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

---

**Document créé le 27 avril 2026**
**Version 1.0 - Django 4.2**
