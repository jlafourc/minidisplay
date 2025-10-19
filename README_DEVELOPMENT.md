# Mini Display Family Information System - Guide de Développement

## 🎯 Vue d'Ensemble

Ce projet implémente un système d'affichage d'information familial pour Raspberry Pi avec écran e-ink. La version actuelle inclut une couche d'abstraction de sources de données complète avec la Story 1.1 implémentée.

## 🚀 Configuration Rapide

### 1. Configuration de l'Environnement Virtuel

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate     # Sur Windows

# Installer les dépendances
pip install -r requirements.txt

# Installation en mode développement
pip install -e .
```

### 2. Configuration de l'API

Créer un fichier `.env` à la racine du projet :

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec votre token IDELIS
nano .env
```

```env
# Token pour l'API Idelis
IDELIS_API_TOKEN=votre_token_ici

# Configuration display (optionnel)
INKY_DISPLAY_AVAILABLE=true
```

## 🧪 Exécution des Tests

### Tests Unitaires

```bash
# Exécuter tous les tests
pipenv run pytest -v

# Avec couverture de code
pipenv run pytest --cov=minidisplay.datasources --cov-report=html
```

### Tests d'Intégration

```bash
# Mode mock (pas besoin d'API)
pipenv run python -m minidisplay --use-mock

# Mode virtuel (pas besoin d'écran e-ink)
INKY_DISPLAY_AVAILABLE=false pipenv run python -m minidisplay --use-mock

# Mode simulation avec heure spécifique
pipenv run python -m minidisplay --use-mock --mock-time 07:30
```

## 📁 Structure du Projet

```
mini-display/
├── minidisplay/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── defaults.json
│   ├── display/
│   │   ├── __init__.py
│   │   ├── devices.py
│   │   ├── models.py
│   │   └── renderer.py
│   ├── resources/
│   │   └── bus-icon.png
│   ├── datasources/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── idelis.py
│   │   └── manager.py
│   └── utils/
│       ├── __init__.py
│       └── paths.py
├── idelis-phat.py            # Wrapper vers le CLI interne
├── resources/
│   └── generated/            # Sorties rendues localement
├── tests/
│   └── datasources/
│       └── test_manager.py
├── docs/
│   └── ...                   # Documentation produit & technique
├── requirements.txt
├── Pipfile
└── setup.py
```

## 🔧 Comment Utiliser l'Abstraction de Données

### Exemple d'utilisation de la nouvelle architecture

```python
from minidisplay.datasources import DataSourceManager

# Initialiser avec la configuration existante
config = {
    "api_url": "https://api.idelis.fr/GetStopMonitoring",
    "api_code": "LAGUTS_1",
    "api_ligne": "5",
    "api_next": 3
}

# Créer le gestionnaire de sources
manager = DataSourceManager(config)
manager.initialize_data_sources()

# Récupérer des données (même API qu'avant)
data = manager.fetch_primary_data()

# Vérifier le statut
status = manager.get_status()
print(f"Sources disponibles: {status['available_sources']}")
```

### Ajouter une nouvelle source de données

```python
from minidisplay.datasources import DataSource
from nob import Nob

class WeatherSource(DataSource):
    def __init__(self, config):
        super().__init__("Weather", config)
        self.api_key = config.get("api_key")
        self.location = config.get("location", "Paris")

    def fetch_data(self) -> Optional[Nob]:
        # Implémenter la logique météo
        pass

    def is_available(self) -> bool:
        return bool(self.api_key)

    def get_refresh_interval(self) -> int:
        return 1800  # 30 minutes

# Ajouter au gestionnaire
manager.data_sources["weather"] = WeatherSource(weather_config)
```

## 📋 Stories Implémentées

### ✅ Story 1.1 - Data Source Abstraction Layer (Terminée)

**Objectif** : Créer une couche d'abstraction générique pour les sources de données

**Implémentation** :
- `minidisplay/datasources/base.py` - Interface DataSource abstraite
- `minidisplay/datasources/idelis.py` - Refactorisation de l'intégration Idelis
- `minidisplay/datasources/manager.py` - Gestionnaire de coordination
- `tests/datasources/test_manager.py` - 18 tests unitaires

**Backward Compatibility** : 100% préservée

### 📋 Stories Futures (Planifiées)

- **Story 1.2** : Enhanced Configuration System
- **Story 1.3** : Extensible Data Source Framework
- **Story 1.4** : Content Type Abstraction
- **Story 1.5** : Time-Based Content Scheduling
- **Story 1.6** : Dynamic Layout Generation

## 🚨 Dépannage

### Problèmes Communs

#### 1. Module 'nob' non trouvé
```bash
# Solution : Installer dans le venv
source venv/bin/activate
pip install nob
```

#### 2. Token API Idelis manquant
```bash
# Solution : Configurer la variable d'environnement
export IDELIS_API_TOKEN="votre_token"
# ou ajouter au fichier .env
```

#### 3. Tests qui échouent
```bash
# Solution : Exécuter depuis la racine du projet avec le venv activé
source venv/bin/activate
pipenv run pytest -v
```

#### 4. Import de modules échoue
```bash
# Solution : Installation en mode développement
source venv/bin/activate
pip install -e .
```

### Vérification de l'Installation

```bash
# 1. Vérifier les dépendances
source venv/bin/activate
pip list | grep -E "(nob|requests|pytest)"

# 2. Vérifier les imports Python
pipenv run python -c "from minidisplay.datasources import DataSourceManager; print('✅ OK')"

# 3. Vérifier les tests
pipenv run pytest -v

# 4. Vérifier l'application principale
pipenv run python -m minidisplay --use-mock --mock-time 07:30
```

## 🔄 Développement Continu

### Flux de Travail Recommandé

1. **Activer le venv** : `source venv/bin/activate`
2. **Faire les changements** : Modifier le code
3. **Exécuter les tests** : `pipenv run pytest -v`
4. **Valider l'intégration** : `pipenv run python -m minidisplay --use-mock`
5. **Documenter les changements** : Mettre à jour README/notes

### Standards de Code

- **Python 3.8+** requis (dataclasses)
- **Type hints** encouragés
- **Docstrings** obligatoires pour les classes publiques
- **Tests unitaires** requis pour toute nouvelle fonctionnalité
- **Backward compatibility** doit être préservée

## 📚 Documentation Complémentaire

- [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) - Vue d'ensemble du projet
- [brownfield-architecture.md](docs/brownfield-architecture.md) - Architecture technique
- [market-research.md](docs/market-research.md) - Analyse de marché
- [PRD](docs/prd.md) - Product Requirements Document

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche de feature
3. Implémenter avec tests
4. Valider la rétrocompatibilité
5. Soumettre une Pull Request

---

**Note** : Cette configuration est optimisée pour le développement de la Story 1.1 et prépare le terrain pour les stories futures du PRD brownfield.
