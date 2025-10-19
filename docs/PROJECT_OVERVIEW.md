# Projet Mini Display - Afficheur d'Information Familial Générique

## Résumé du Projet

Il s'agit d'un **projet d'afficheur d'information générique** pour Raspberry Pi qui affiche diverses données utiles pour la famille sur un écran e-ink. Le projet fournit un système d'affichage flexible et configurable qui peut présenter différentes informations familiales (horaires de transport, météo, calendrier, rappels, etc.) tout en minimisant la consommation d'énergie grâce à une planification intelligente.

## Objectif Principal

- **Afficheur d'Information Familial** : Affiche diverses informations utiles pour la vie quotidienne familiale
- **Écran E-ink** : Utilise un écran e-ink Inky Phat (212x104 pixels) pour une faible consommation d'énergie et une bonne lisibilité
- **Système Générique et Configurable** : Architecture flexible permettant d'afficher différents types de données selon les besoins familiaux
- **Planification Intelligente** : Ne s'active que pendant les heures définies par l'utilisateur pour économiser l'énergie

## Composants Principaux

### 1. Application Principale (`idelis-phat.py`)
- Point d'entrée qui orchestre l'ensemble du système
- Gère la récupération des données de différentes sources (API, services web, données locales)
- Gère la planification de l'affichage en fonction des fenêtres temporelles
- Prend en charge les arguments de ligne de commande pour les tests et simulations
- *Note : `idelis-phat.py` est l'implémentation actuelle (horaires de bus) mais l'architecture supporte d'autres sources de données*

### 2. Architecture du Système d'Affichage
Une conception modulaire avec des composants distincts et bien définis :

- **`display_models.py`** : Modèles de données et validation pour les mises en page et éléments d'affichage
  - `DisplayElement` : Définit les composants UI individuels (texte, icônes)
  - `DisplayLayout` : Gère les arrangements de plusieurs éléments
  - Constantes pour les dimensions et le style d'affichage

- **`display_devices.py`** : Couche d'abstraction matérielle
  - `Display` : Classe de base abstraite définissant l'interface d'affichage
  - `InkyDisplay` : Implémentation physique de l'écran e-ink
  - `VirtualDisplay` : Affichage basé sur fichiers pour les tests/simulations

- **`display_output.py`** : Moteur de rendu qui transforme les mises en page en sortie visuelle

### 3. Configuration (`config.json`)
- Paramètres API et authentification pour différentes sources de données
- Heures d'activité de l'affichage (heures de début/fin)
- Gestion des fichiers de verrouillage pour le mode veille
- Configuration modulaire des différentes sources d'information (transport, météo, calendrier, etc.)

## Fonctionnalités Clés

### **Intégration Multi-Sources**
- Supporte différentes sources de données (API transport, API météo, calendriers, rappels, etc.)
- Gère l'authentification via les variables d'environnement
- Gestion gracieuse des erreurs réseau et service unavailable
- Architecture extensible pour ajouter de nouvelles sources de données

### **Mode Simulation pour Tests**
- Le drapeau `--use-mock` active le mode simulation
- `--mock-time` permet de tester des scénarios temporels spécifiques
- Génère des données de simulation réalistes pour différentes sources

### **Fonctionnement Basé sur le Temps**
- **Heures Actives** : Affiche les informations pertinentes selon le contexte (ex: transports le matin, météo l'après-midi)
- **Mode Veille** : Affiche un message personnalisé quand aucune information active n'est à montrer
- Le système de fichiers de verrouillage empêche les mises à jour inutiles pendant la veille
- Possibilité de configurer différents types d'affichage selon les heures/jours

### **Flexibilité Matérielle**
- Détection automatique du matériel d'affichage Inky
- Retour à l'affichage virtuel si le matériel n'est pas disponible
- Contrôle par variable d'environnement du type d'affichage

### **Architecture Propre**
- Logique d'affichage bien séparée de la logique métier
- Conception modulaire permettant des tests et maintenance faciles
- Comportement piloté par la configuration

## Expérience Utilisateur

### **Mode Affichage Actif**
- Affichage adaptable selon le type d'information (icône + texte, texte seul, multiples informations)
- Mises en page configurables (horizontale, verticale, compacte)
- Taille de police et éléments ajustables selon le contenu
- Mises à jour toutes les 60 secondes (ou configurable selon le type de donnée)

### **Mode Veille**
- Message simple "En veille"
- Consommation d'énergie minimale
- Le fichier de verrouillage empêche le traitement inutile

### **Spécifications de Design Visuel**
- **Résolution d'Affichage** : 212x104 pixels (Inky Phat)
- **Taille d'Icône** : 40px de hauteur avec ratio d'aspect maintenu
- **Taille de Police** : 24px pour les heures d'arrivée
- **Marge Intérieure** : 5px de tous les bords de l'affichage
- **Espacement** : 5px cohérents entre les éléments

## Architecture Technique

### **Stack Logiciel**
- **Langage** : Python 3
- **Bibliothèque d'Affichage** : Inky (écran e-ink)
- **HTTP** : Bibliothèque Requests pour les appels API
- **Traitement d'Image** : PIL/Pillow
- **Configuration** : Basée sur JSON

### **Outils de Développement**
- **Framework BMAD** : Workflow de développement structuré
- **Git** : Contrôle de version
- **Pipenv** : Gestion des dépendances

### **Plateforme Cible**
- **Matériel** : Raspberry Pi
- **Affichage** : Écran e-ink Inky Phat
- **OS** : Raspberry Pi OS

## Cas d'Usage Possibles

### **Actuellement Implémenté**
- **Horaires de Transport** : Prochain bus/métro, informations sur les retards

### **Futures Possibilités Familiales**
- **Météo** : Conditions actuelles, prévisions sur 24h, alertes météo
- **Calendrier Familial** : Rendez-vous importants, anniversaires, événements scolaires
- **Rappels Personnels** : Médicaments, tâches ménagères, courses à faire
- **Informations Domestiques** : Consommation énergétique, état des appareils intelligents
- **Actualités** : Titres d'actualités importants, alertes locales
- **Messages Familiaux** : Notes laissées par les membres de la famille

## Objectifs du Projet

✅ **Exigences Fonctionnelles**
- [x] Récupérer les données de différentes sources (API actuelle : transport)
- [x] Afficher des informations formatées selon des modèles configurables
- [x] Afficher un message de veille personnalisé en dehors des heures actives
- [x] Configurable via fichier JSON
- [ ] Supporter plusieurs types de données et sources

✅ **Exigences Non-Fonctionnelles**
- [x] Intervalle de mise à jour configurable selon le type de donnée
- [x] Compatibilité Raspberry Pi
- [x] Faible consommation d'énergie grâce à l'écran e-ink
- [x] Architecture extensible pour de nouvelles sources de données

## User Stories

- **En tant que membre de la famille, je veux voir rapidement les informations importantes du jour sans sortir mon téléphone.**
- **En tant que parent, je veux configurer l'affichage pour qu'il montre les informations pertinentes pour chaque moment de la journée.**
- **En tant qu'utilisateur, je veux que l'affichage soit discret et économe en énergie quand personne n'a besoin des informations.**
- **En tant que développeur familial, je veux pouvoir ajouter facilement de nouvelles sources de données personnalisées.**

## Statut de Développement

Le projet suit une approche de développement structurée avec :
- Architecture modulaire pour la maintenabilité et l'extensibilité
- Gestion complète de la configuration
- Capacités de test via le mode simulation
- Séparation claire des préoccupations
- Développement piloté par la documentation
- **Focalisation actuelle** : Preuve de concept avec les horaires de bus

Ce projet représente une solution pratique et bien conçue pour un afficheur d'information familial polyvalent, avec une attention particulière à l'efficacité énergétique, la maintenabilité et l'adaptabilité aux besoins familiaux évolutifs.