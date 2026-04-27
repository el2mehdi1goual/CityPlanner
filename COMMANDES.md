# 🚀 COMMANDES RAPIDES - AI URBAN DESIGN PLANNER

## ⚡ Installation en 5 minutes

### 1. Activer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Créer la base de données MySQL
```bash
# Dans MySQL:
CREATE DATABASE ai_urban_design CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
# Entrez: username, email, password
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

### 7. Accéder à l'application
```
http://127.0.0.1:8000
```

---

## 📋 Commandes Django courantes

### Gestion de la base de données
```bash
# Voir les migrations
python manage.py showmigrations

# Appliquer les migrations
python manage.py migrate

# Créer les migrations
python manage.py makemigrations

# Migrations spécifiques
python manage.py migrate urban_design

# Revenir à une migration antérieure
python manage.py migrate urban_design 0001
```

### Administrateur
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le shell Django interactif
python manage.py shell

# Charger des données de test
python manage.py loaddata fixture.json

# Exporter les données
python manage.py dumpdata > data.json
```

### Serveur
```bash
# Lancer sur le port par défaut (8000)
python manage.py runserver

# Lancer sur un port personnalisé
python manage.py runserver 8080

# Lancer sur 0.0.0.0 (tous les IPs)
python manage.py runserver 0.0.0.0:8000
```

### Fichiers statiques
```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Vérifier les fichiers statiques
python manage.py findstatic css/style.css
```

### Tests
```bash
# Exécuter tous les tests
python manage.py test

# Tests avec verbosité
python manage.py test --verbose

# Tests spécifiques
python manage.py test urban_design.tests
python manage.py test urban_design.tests.UserAuthenticationTest

# Avec couverture de code
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Nettoyage
```bash
# Supprimer tous les fichiers statiques
python manage.py collectstatic --clear

# Vider la base de données
python manage.py flush

# Supprimer les migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

---

## 🔧 Scripts personnalisés

### Configurer le projet automatiquement
```bash
python setup_project.py
```

Cela va:
1. Vérifier les dépendances
2. Tester la connexion à MySQL
3. Appliquer les migrations
4. Créer un compte admin
5. Créer des données d'exemple

---

## 📊 Accès aux interfaces

### Application web
```
http://127.0.0.1:8000
```

### Admin Django
```
http://127.0.0.1:8000/admin/
```
Identifiants: username/password créés avec `createsuperuser`

### Shell Django
```bash
python manage.py shell
```

---

## 🐛 Débogage

### Activer le debug mode
Dans `config/settings.py`:
```python
DEBUG = True
```

### Logs
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Erreur")
```

### Afficher les requêtes SQL
```bash
# Dans settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

---

## 🔐 Configuration de sécurité

### Pour la production:
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['votredomaine.com', 'www.votredomaine.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Générer une clé secrète
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 📦 Gestion des dépendances

### Mettre à jour les dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### Geler les versions actuelles
```bash
pip freeze > requirements.txt
```

### Installer une dépendance
```bash
pip install nomdupackage
pip freeze > requirements.txt
```

---

## 🌐 Déploiement (bases)

### Collecteur les fichiers statiques (production)
```bash
python manage.py collectstatic --noinput
```

### Gunicorn (application server)
```bash
pip install gunicorn
gunicorn config.wsgi
```

### Nginx (reverse proxy)
Voir documentation Nginx pour la configuration

---

## 🧪 Workflow de développement

### 1. Créer une branche
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

### 2. Modifier le code
```bash
# Éditer models.py, views.py, etc.
```

### 3. Faire les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Tester
```bash
python manage.py test
```

### 5. Formatter le code
```bash
pip install black
black .
```

### 6. Commit
```bash
git add .
git commit -m "Ajout de la nouvelle fonctionnalité"
```

### 7. Push
```bash
git push origin feature/nouvelle-fonctionnalite
```

---

## 📚 Liens utiles

- Django Docs: https://docs.djangoproject.com/
- Bootstrap Docs: https://getbootstrap.com/docs/
- MySQL Docs: https://dev.mysql.com/doc/
- Python PEP 8: https://www.python.org/dev/peps/pep-0008/

---

## ✅ Checklist d'installation

- [ ] Python 3.8+ installé
- [ ] MySQL installé et lancé
- [ ] Environnement virtuel créé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Base de données créée (`CREATE DATABASE ai_urban_design`)
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superutilisateur créé (`python manage.py createsuperuser`)
- [ ] Serveur lancé (`python manage.py runserver`)
- [ ] Accès à http://127.0.0.1:8000 ✓

---

## 🎯 Prochaines étapes

1. Lancer le serveur: `python manage.py runserver`
2. Créer un compte: http://127.0.0.1:8000/register/
3. Créer un projet: Cliquer sur "Nouveau projet"
4. Générer une proposition: Cliquer sur "Générer proposition"
5. Générer un prompt image: Cliquer sur "Générer prompt image"

---

Bon développement! 🚀
