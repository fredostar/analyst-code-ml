# analyst-code-ml

Outil CLI de revue de code alimenté par l'IA. Il récupère les fichiers source d'un dépôt GitHub ou GitLab, les analyse via Mistral AI, et génère un rapport Markdown structuré avec diagnostics et suggestions.

## Prérequis

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances
- Une clé API Mistral (obtenue sur [console.mistral.ai](https://console.mistral.ai))
- Un token GitHub ou GitLab selon la plateforme cible

## Installation

```bash
uv sync
```

## Configuration

```bash
export MISTRAL_API_KEY=votre_clé_api
export GITHUB_TOKEN=votre_token_github   # pour les dépôts GitHub
export GITLAB_TOKEN=votre_token_gitlab   # pour les dépôts GitLab
```

## Utilisation

```bash
uv run python src/main.py
```

## Architecture

Le projet suit une architecture hexagonale (ports & adapters) :

- **Domaine** (`domain/`) — modèles métier et interfaces abstraites, sans dépendance externe
- **Adapters** (`adapters/`) — implémentations concrètes : GitHub, GitLab, Mistral AI, rapport Markdown
- **Orchestration** (`review/`) — coordonne la récupération, l'analyse et la génération du rapport
- **CLI** (`cli.py`) — point d'entrée Typer

## Développement

```bash
# Lancer les tests
uv run pytest

# Linter / formateur
uv run ruff check src tests
uv run ruff format src tests
```