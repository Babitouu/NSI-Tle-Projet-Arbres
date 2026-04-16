# NSI-Tle-Projet-Arbres

## Documents
- [Sujet](https://github.com/Babitouu/NSI-Tle-Projet-Arbres/blob/50afc7ba2b7738df6b08c6ef497b8941335dc23e/Documents/Sujet.pdf)
- [Grille d'évaluation](https://github.com/Babitouu/NSI-Tle-Projet-Arbres/blob/50afc7ba2b7738df6b08c6ef497b8941335dc23e/Documents/Grille%20d'%C3%A9valuation.pdf)

## 📚 Description du Projet

**ArbreViz** est une application web interactive pour la visualisation et la manipulation des arbres binaires. 
Elle permet de :
- Créer des arbres binaires classiques ou des arbres binaires de recherche (ABR)
- Visualiser graphiquement les arbres avec un rendu SVG interactif
- Effectuer des opérations de recherche dans les ABR
- Parcourir les arbres selon différentes méthodes (préfixe, infixe, suffixe, largeur)
- Consulter l'historique des arbres précédemment générés

## ✨ Fonctionnalités Détaillées

### 1. Création d'Arbres Binaires

#### Arbre Binaire Classique
- Créer des arbres binaires en spécifiant les valeurs et la structure
- Support des valeurs `None` pour représenter les nœuds vides
- Insertion de valeurs complètes dans des positions spécifiques

#### Arbre Binaire de Recherche (ABR)
- Créer automatiquement un ABR à partir d'une liste de valeurs
- Les valeurs s'insèrent suivant la propriété BST (gauche < parent < droit)
- Support des nombres entiers et décimaux

### 2. Visualisation Graphique

- **Rendu SVG interactif** : L'arbre s'affiche avec des nœuds circulaires reliés par des liens
- **Zoom et déplacement** (Panzoom) :
  - Zoomer avec la molette de la souris
  - Se déplacer en glissant-déposant
  - Centrer automatiquement l'arbre
  - Bouton de réinitialisation de la vue
- **Mode plein écran** : Agrandir la visualisation à tout l'écran
- **Mise en surbrillance des nœuds** : Les nœuds trouvés lors d'une recherche sont mis en évidence

### 3. Opérations de Recherche (ABR)

- Rechercher une valeur spécifique dans un ABR
- Affichage visuel du nœud trouvé en surbrillance
- Message d'erreur si la valeur n'existe pas
- Support des nombres entiers et décimaux

### 4. Parcours d'Arbres

Quatre méthodes de parcours disponibles :

- **Préfixe (Profondeur d'abord)** : Visite le nœud, puis son sous-arbre gauche, puis son sous-arbre droit
- **Infixe (Parcours interne)** : Visite le sous-arbre gauche, le nœud, puis le sous-arbre droit
- **Suffixe (Post-ordre)** : Visite le sous-arbre gauche, le sous-arbre droit, puis le nœud
- **Largeur (Parcours en largeur)** : Visite tous les nœuds niveau par niveau

Les résultats s'affichent sous forme de liste ordonnée

### 5. Statistiques

Affichage en temps réel de :
- **Hauteur** : Distance maximale entre la racine et les feuilles
- **Taille** : Nombre total de nœuds dans l'arbre

### 6. Historique Persistant

- Sauvegarde automatique des 5 derniers arbres générés
- Stockage dans le `localStorage` du navigateur (persistance entre les sessions)
- Restauration rapide d'un arbre précédent
- Affichage des 20 premiers caractères et du type d'arbre pour identification

### 7. Interface Utilisateur

- **Responsive** : Adaptation à différentes tailles d'écran (desktop, tablet, mobile)
- **Sidebar collapsible** : Sur mobile, la boîte à outils se rétracte pour laisser plus de place
- **Design moderne** : Glassmorphism avec effets de transparence et gradients
- **Navigation intuitive** : Onglets pour basculer entre Configuration et Historique

## 🏗️ Architecture du Projet

### Fichiers Principaux

- **`main.py`** : Logique métier et gestion des événements
  - Récupération et traitement des données du DOM
  - Gestion de l'historique avec localStorage
  - Génération de la représentation graphique SVG des arbres
  - Gestion des opérations (recherche, parcours)

- **`arbre.py`** : Module de gestion des structures de données
  - Classes et méthodes pour créer et manipuler les arbres binaires
  - Algorithmes de recherche et de parcours
  - Calculs de hauteur et de taille

- **`index.html`** : Structure et mise en page de l'interface
  - Formulaires de configuration et de recherche
  - Conteneur SVG pour l'affichage de l'arbre
  - Barre de navigation et boîte à outils (sidebar)
  - Scripts d'initialisation Panzoom pour le zoom/pan

- **`style.css`** : Styles et thème de l'application
  - Design glassmorphism moderne
  - Variables CSS pour la cohérence visuelle
  - Styles responsive pour les appareils mobiles
  - Animations et transitions

- **`pyscript.toml`** : Configuration de PyScript
  - Déclaration des modules Python à charger

### Fichiers de Documentation

- **`journal_ia.md`** : Journal des échanges et décisions de conception
- **`Documents/`** : Sujet du projet et grille d'évaluation

## 🚀 Technologies Utilisées

- **PyScript** : Exécution de code Python dans le navigateur
- **SVG** : Rendu graphique des arbres
- **Panzoom** : Interactivité pour le zoom et le déplacement
- **CSS3** : Styles modernes avec glassmorphism et gradients
- **HTML5** : Structure sémantique
- **LocalStorage** : Gestion persistante de l'historique

## ⚙️ Choix Techniques

### PyScript vs Flask

Nous avons choisi **PyScript** plutôt que Flask pour plusieurs raisons essentielles :

- **Pas de recharargement de page** : Avec Flask, chaque interaction nécessiterait un rechargement complet de la page. PyScript permet une communication directe et efficace entre Python et le DOM sans rechargements incessants.
- **Communication plus directe** : PyScript accède directement aux éléments du DOM et gère les événements en natif, offrant une meilleure réactivité.
- **Expérience utilisateur fluide** : L'application reste responsive et interactive sans latence due aux requêtes serveur.
- **Pas de dépendance serveur pour la logique** : La plupart de la logique métier s'exécute côté client.

## 🚀 Installation et Lancement

### Prérequis
- Python 3.7+ installé (ou un navigateur moderne avec PyScript)
- Un navigateur web moderne (Chrome, Firefox, Edge, Safari)

### Étapes de lancement

**Option 1 : Utiliser ArbreViz.exe**
1. Double-cliquez sur `ArbreViz.exe` (si disponible)
2. Ouvrez votre navigateur et accédez à `localhost:8000`

**Option 2 : Utiliser le serveur Python intégré**
1. Ouvrez un terminal dans le répertoire du projet
2. Lancez la commande :
   ```bash
   python -m http.server
   ```
3. Ouvrez votre navigateur et accédez à `http://localhost:8000`

### ⚠️ Important
- **Ne pas ouvrir `index.html` directement** : L'ouverture directe du fichier HTML provoquera une erreur due aux restrictions CORS (PyScript et les ressources externes ne fonctionnent pas en `file://`).
- L'application **doit obligatoirement être servie via HTTP** pour fonctionner correctement.

## 📝 Comment Utiliser

1. Entrez les valeurs dans le champ "Valeurs et Type de l'arbre"
2. Sélectionnez le type : "Arbre Binaire" ou "Arbre Binaire de Recherche"
3. Cliquez sur "Générer l'Arbre"
4. L'arbre s'affiche graphiquement avec ses statistiques (hauteur, taille)
5. Pour un ABR, utilisez l'onglet "Rechercher" pour trouver une valeur
6. Utilisez l'onglet "Parcourir" pour explorer l'arbre selon différentes méthodes

## 📋 Auteurs

- Romain THIBEAUD
- Cédric VILLEMONAIS

## 👥 Répartition du Travail

### Romain THIBEAUD
- **`arbre.py`** : Structure de données complète des arbres binaires et opérations de base

### Cédric VILLEMONAIS
- **`inserer_classic()`** : Fonction d'insertion pour les arbres binaires classiques
- **`main.py`** : Logique métier, gestion des événements, génération SVG
- **`index.html`** : Structure HTML, formulaires, mise en page
- **`style.css`** : Design glassmorphism, thème et responsivité
- **`pyscript.toml`** : Configuration PyScript

© 2026
