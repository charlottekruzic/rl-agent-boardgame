# 1. Définition de l'Espace d'Action
La définition de l'espace d'action est cruciale pour que l'agent puisse interagir efficacement avec l'environnement. Deux approches principales ont été proposées pour modéliser l'espace d'action du jeu Labyrinthe.

## 1.1 Espace d'Action Aplati
**Description** :

- L'espace d'action est défini comme un espace `Discrete` unique, où chaque action possible est codée par un entier unique.
- Le nombre total d'actions est le produit des possibilités de chaque composante d'action :
  - 12 positions d'insertion.
  - 4 orientations possibles de la tuile.
  - 49 positions de déplacement (sur un plateau 7x7).
- Total des actions : `12 * 4 * 49 = 2352` actions possibles.

**Avantages** :

- Compatibilité avec les algorithmes RL standards : Les algorithmes comme PPO peuvent gérer directement un espace d'action discret.
- Simplicité d'implémentation : Pas besoin de personnaliser l'algorithme pour gérer des espaces d'action complexes.

**Inconvénients** :

- Grande dimensionnalité : L'espace d'action est très large, ce qui peut rendre l'apprentissage plus difficile.
- Actions invalides fréquentes : L'agent risque de choisir souvent des actions invalides, surtout au début de l'entraînement.

**Implémentation** :

- **Encodage de l'action** : Conversion des composantes (insertion, rotation, déplacement) en un entier unique.
- **Décodage de l'action** : Dans la méthode `step`, l'action entière est décodée en ses composantes pour être traitée.

## 1.2 Espace d'Action Structuré avec `spaces.Tuple` ou `spaces.MultiDiscrete`
**Description** :

- L'espace d'action est défini comme un tuple ou un vecteur où chaque composante représente une sous-action.
  - `spaces.Tuple((spaces.Discrete(12), spaces.Discrete(4), spaces.Discrete(49)))`
  - Ou `spaces.MultiDiscrete([12, 4, 49])`

**Avantages** :

- Clarté et lisibilité : Les actions sont naturellement séparées en leurs composantes, ce qui facilite le traitement.
- Modularité : Permet de gérer chaque composante d'action indépendamment.

**Inconvénients** :

- Incompatibilité avec certains algorithmes : Les algorithmes comme PPO dans `stable-baselines3` ne supportent pas directement les espaces d'action de type Tuple ou MultiDiscrete.
- Complexité d'implémentation : Nécessite de personnaliser la politique de l'agent pour gérer cet espace d'action.

**Implémentation** :

- **Action sous forme de tuple** : L'action est traitée comme un tuple `(idx_insertion, idx_rotation, action_deplacement)`.
- **Adaptation de la politique** : Peut nécessiter une politique personnalisée pour que l'algorithme d'apprentissage gère cet espace d'action.

# 2. Définition de l'Espace d'Observation
L'espace d'observation doit fournir à l'agent toutes les informations nécessaires pour prendre des décisions éclairées.

**Proposition** :

- Utilisation d'un `spaces.Dict` pour structurer l'observation.

**Composantes de l'observation** :
- `plateau` : Un tableau de dimensions `(7, 7, 6)` contenant :
  - Les informations des murs (Nord, Sud, Est, Ouest).
  - La présence de joueurs.
  - La présence de trésors.
- `tuile_sup` : Un vecteur contenant les informations sur la tuile supplémentaire.
- `tresor_a_trouver` : Le trésor que le joueur doit actuellement trouver, normalisé entre 0 et 1.

**Avantages** :

- Richesse de l'information : Fournit à l'agent une vue complète de l'état du jeu.
- Structure claire : L'utilisation d'un dictionnaire permet de séparer logiquement les différentes parties de l'observation.

**Inconvénients** :

- Compatibilité limitée : Certains algorithmes ou implémentations ne supportent pas directement les espaces d'observation de type `Dict`.
- Besoin de prétraitement : Peut nécessiter d'aplatir l'observation ou de créer des extracteurs de caractéristiques personnalisés.

**Solutions** :

- Utiliser le wrapper `FlattenObservation` : Permet d'aplatir l'observation en un vecteur unique compatible avec les politiques par défaut.
- Créer une politique personnalisée : Adapter la politique de l'agent pour traiter directement l'espace d'observation structuré.

# 3. Gestion des Actions Invalides
Les actions invalides (par exemple, insérer une tuile dans une direction interdite ou se déplacer vers une position inaccessible) peuvent perturber l'apprentissage de l'agent.

## 3.1 Pénalisation des Actions Invalides
**Description** :

- Lorsqu'une action invalide est exécutée, l'agent reçoit une pénalité (récompense négative).
- L'épisode continue, permettant à l'agent de corriger son comportement.

**Avantages** :

- Simplicité d'implémentation : Facile à mettre en place dans la méthode `step`.
- Encourage l'exploration : L'agent apprend à éviter les actions invalides au fil du temps.

**Inconvénients** :

- Apprentissage plus lent : L'agent peut passer beaucoup de temps à explorer des actions invalides, surtout dans un espace d'action large.
- Frustration de l'agent : Des pénalités fréquentes peuvent rendre l'apprentissage instable.

## 3.2 Utilisation de Masques d'Action
**Description** :

- Fournir à l'agent un masque indiquant quelles actions sont valides à chaque étape.
- L'agent ne peut choisir que parmi les actions valides.

**Avantages** :

- Apprentissage plus efficace : L'agent se concentre sur les actions valides, accélérant l'apprentissage.
- Réduction des pénalités inutiles : Évite de pénaliser l'agent pour des actions qu'il ne peut pas savoir invalides.

**Inconvénients** :

- Complexité d'implémentation : Nécessite de modifier l'environnement pour générer le masque d'action.
- Compatibilité limitée : Tous les algorithmes ou implémentations ne supportent pas les masques d'action.

**Solutions** :

- Personnaliser la politique de l'agent : Adapter l'algorithme pour tenir compte des masques d'action.
- Pré-filtrer les actions : Réduire l'espace d'action aux actions valides, bien que cela puisse être complexe avec un grand espace d'action.
