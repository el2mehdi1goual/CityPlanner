# Guide des fonctionnalités - AI Urban Design Planner

## 1️⃣ Authentification

### Inscription
- Allez sur `/register/`
- Remplissez le formulaire avec:
  - Nom d'utilisateur (unique)
  - Email
  - Mot de passe
  - Confirmation du mot de passe
- Cliquez sur "S'inscrire"
- Vous serez automatiquement connecté et redirigé vers le dashboard

### Connexion
- Allez sur `/login/`
- Entrez votre nom d'utilisateur et mot de passe
- Cliquez sur "Se connecter"

### Déconnexion
- Cliquez sur votre nom d'utilisateur dans la navbar
- Sélectionnez "Déconnexion"

---

## 2️⃣ Tableau de bord

Le tableau de bord affiche:
- **Nombre total de projets** créés par l'utilisateur
- **Nombre de propositions générées**
- **Les derniers projets** (5 plus récents)
- **Statistiques rapides** dans des cartes colorées

Boutons d'action:
- 🔵 "Créer un nouveau projet"

---

## 3️⃣ Gestion des projets

### Créer un projet
1. Cliquez sur "Nouveau projet" (dans le navbar ou le dashboard)
2. Remplissez le formulaire:
   - **Titre**: Nom du projet (ex: "Zone de relogement A")
   - **Description**: Détails optionnels
   - **Nombre de familles**: Ex: 500
   - **Taille moyenne des familles**: Ex: 5
   - **Superficie du terrain**: En hectares (ex: 75 ha)
   - **Niveau du budget**: Faible / Moyen / Élevé
   - **Priorité**: Logements / Espaces verts / Services publics / Équilibré
3. Cliquez sur "Créer un nouveau projet"

### Consulter les détails
1. Allez sur "/projets/"
2. Cliquez sur le bouton "Voir" (oeil) du projet
3. Vous verrez:
   - Toutes les informations du projet
   - La proposition générée (si elle existe)
   - Les prompts d'images générés
   - L'historique des actions

### Modifier un projet
1. Allez sur la page détails du projet
2. Cliquez sur "Modifier"
3. Changez les paramètres
4. Cliquez sur "Modifier le projet"

### Supprimer un projet
1. Allez sur la page détails du projet
2. Cliquez sur "Supprimer"
3. Confirmez la suppression

---

## 4️⃣ Génération de propositions

### Générer une proposition
1. Allez sur la page détails d'un projet
2. Cliquez sur "Générer proposition"
3. Le système calcule automatiquement:
   - Nombre de logements = nombre de familles
   - Nombre d'écoles = Population ÷ 500 (min. 1)
   - Nombre de centres de santé = Population ÷ 1000 (min. 1)
   - Nombre de marchés = Population ÷ 800 (min. 1)
   - Surface d'espaces verts = selon la priorité (7%, 10%, ou 15%)
   - Surface des routes = 20% du terrain

### Regénérer une proposition
- Si une proposition existe déjà, le bouton devient "Regénérer proposition"
- Cliquez pour recalculer avec les paramètres actuels du projet

### Affichage de la proposition
La proposition affiche:
- 📊 Cartes de synthèse (logements, écoles, etc.)
- 📝 Description détaillée en texte
- 📅 Date de génération

---

## 5️⃣ Génération de prompts d'images

### Générer un prompt
1. Allez sur la page détails d'un projet
2. Cliquez sur "Générer prompt image"
   - Cela génère automatiquement une proposition si elle n'existe pas
3. Le prompt s'affiche dans la section "Prompts d'images générées"

### Utiliser le prompt
Le prompt peut être utilisé avec:
- 🎨 **Midjourney**: `/imagine [prompt]`
- 🖼️ **DALL-E**: Copier-coller le prompt
- 🌟 **Stable Diffusion**: Entrer le prompt
- 🤖 Toute autre API de génération d'images

### Format du prompt
```
Generate a realistic top-view urban neighborhood master plan for 
[nombre] families including housing blocks, [écoles] school, 
[santé] health center, green spaces, roads, public spaces and 
local markets...
```

---

## 6️⃣ Historique des actions

L'historique enregistre:
- ✅ **Création du projet**
- ✏️ **Modifications du projet**
- 🗑️ **Suppression du projet**
- ✨ **Génération de proposition**
- 🔄 **Regénération de proposition**
- 🖼️ **Génération de prompt image**

Chaque entrée affiche:
- Type d'action
- Description
- Date et heure exacte

---

## 7️⃣ Gestion des droits

### Sécurité
- ✅ Vous ne pouvez voir que **vos propres projets**
- ✅ Vous ne pouvez modifier/supprimer que **vos propres projets**
- ✅ Les autres utilisateurs ne peuvent pas accéder à vos données

### Authentification requise
Toutes ces pages nécessitent une connexion:
- `/dashboard/`
- `/projets/`
- `/projets/ajouter/`
- `/projets/<id>/`
- `/projets/<id>/modifier/`
- Etc.

---

## 8️⃣ Admin Django

### Accéder à l'admin
- Allez sur `/admin/`
- Connectez-vous avec un compte superutilisateur
- Tableau de bord complet avec gestion:
  - 👥 Utilisateurs
  - 🏢 Projets urbains
  - 💡 Propositions d'aménagement
  - 🖼️ Images générées
  - 📝 Historique des projets

### Actions dans l'admin
- Voir tous les projets de tous les utilisateurs
- Filtrer par budget, priorité, date
- Rechercher par titre
- Modifier des projets
- Voir les statistiques

---

## 9️⃣ Algorithme de calcul

### Exemple numérique

**Paramètres du projet:**
- Nombre de familles: 500
- Taille moyenne: 5 personnes
- Superficie: 100 hectares
- Budget: Moyen
- Priorité: Équilibré

**Calculs:**
```
Population = 500 × 5 = 2500 habitants

Logements = 500 unités
Écoles = MAX(1, CEIL(2500/500)) = 5
Centres de santé = MAX(1, CEIL(2500/1000)) = 3
Marchés = MAX(1, CEIL(2500/800)) = 4

Espaces verts (équilibré) = 100 × 10% = 10 hectares
Routes = 100 × 20% = 20 hectares
Reste = 70 hectares (logements, services, etc.)
```

---

## 🔟 Conseils pratiques

### Pour de meilleurs résultats:

1. **Définir une priorité claire**
   - "Espaces verts" pour plus d'environnement
   - "Logements" pour densité plus haute
   - "Équilibré" pour compromis

2. **Estimer correctement**
   - Taille moyenne = nombre total de personnes ÷ nombre de familles
   - Superficie = terrain total disponible en hectares

3. **Budget réaliste**
   - Faible: Solution économique, basique
   - Moyen: Standard, équilibré
   - Élevé: Premium, équipements complets

4. **Regénérer si besoin**
   - Modifiez les paramètres du projet
   - Regénérez la proposition pour voir les nouvelles valeurs

---

## ⚠️ Limitations actuelles

- 🎨 Les images ne sont pas générées automatiquement (prompts seulement)
- 🌍 Pas de géolocalisation
- 📄 Pas d'export PDF (peuvent être ajoutés)
- 👥 Pas de partage de projets entre utilisateurs
- 📱 Pas d'interface mobile native

Ces fonctionnalités peuvent être développées dans les versions futures!

---

## ❓ FAQ

**Q: Puis-je modifier mon projet après avoir généré une proposition?**
R: Oui! Modifiez le projet et regénérez la proposition pour voir les changements.

**Q: Les données sont-elles sauvegardées automatiquement?**
R: Oui, Django sauvegarde tout automatiquement en base de données.

**Q: Combien de projets puis-je créer?**
R: Autant que vous le souhaitez! Il n'y a pas de limite.

**Q: Puis-je exporter les données?**
R: Vous pouvez utiliser l'admin Django pour exporter les données.

**Q: Les propositions sont-elles réalistes?**
R: Elles suivent les standards internationaux de planification urbaine. Ajustez selon vos besoins locaux.

---

## 📞 Support

Pour des problèmes ou suggestions:
- Vérifiez le [README.md](README.md)
- Consultez le [guide d'installation](INSTALLATION.md)
- Contactez l'équipe de développement

---

Bonne utilisation! 🎉
