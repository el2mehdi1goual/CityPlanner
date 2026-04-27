# Guide d'Installation Rapide - AI Urban Design Planner

## ⚡ Installation en 5 minutes

### Étape 1: Préparer l'environnement
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Étape 2: Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 3: Configurer MySQL
```bash
# Assurez-vous que MySQL est lancé, puis dans MySQL:
CREATE DATABASE ai_urban_design CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Étape 4: Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Étape 5: Créer un compte admin
```bash
python manage.py createsuperuser
# Entrez votre nom d'utilisateur, email et mot de passe
```

### Étape 6: Lancer le serveur
```bash
python manage.py runserver
```

L'application est maintenant disponible à **http://127.0.0.1:8000**

---

## 📝 Utilisation

1. **Créer un compte** : Allez sur http://127.0.0.1:8000/register/
2. **Se connecter** : Utilisez vos identifiants
3. **Créer un projet** : Cliquez sur "Nouveau projet"
4. **Générer une proposition** : Cliquez sur "Générer proposition"
5. **Générer un prompt image** : Cliquez sur "Générer prompt image"

---

## 🛠️ Commandes utiles

```bash
# Voir les migrations
python manage.py showmigrations

# Réinitialiser la base de données (ATTENTION!)
python manage.py flush

# Créer des données de test
python manage.py shell

# Lancer les tests
python manage.py test

# Accéder à l'admin
http://127.0.0.1:8000/admin/
```

---

## 🔧 Dépannage

**Erreur: "django not found"**
```
pip install -r requirements.txt
```

**Erreur: "No module named 'MySQLdb'"**
```
pip install mysqlclient
```

**Erreur: "Can't connect to MySQL"**
- Vérifiez que MySQL est lancé
- Vérifiez les paramètres DATABASES dans settings.py

**Erreur de migration**
```
python manage.py migrate --run-syncdb
```

---

## 📚 Documentation complète

Voir [README.md](README.md) pour la documentation complète.

---

## 🎯 Prochaines étapes

1. Créer votre premier projet
2. Générer une proposition d'aménagement
3. Générer des prompts d'images
4. Explorer les fonctionnalités avancées

---

Bon développement! 🚀
