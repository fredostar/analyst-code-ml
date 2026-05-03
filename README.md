# analyst-code-ml

Projet Python d'exploration de l'API Mistral AI. Il envoie une question au modèle et affiche la réponse dans le terminal.

## Prérequis

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances
- Une clé API Mistral (obtenue sur [console.mistral.ai](https://console.mistral.ai))

## Installation

```bash
uv sync
```

## Configuration

Définir la variable d'environnement `MISTRAL_API_KEY` :

```bash
export MISTRAL_API_KEY=votre_clé_api
```

## Utilisation

```bash
uv run python main.py
```