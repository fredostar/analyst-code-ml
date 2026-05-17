# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Python 3.13 CLI tool that performs AI-powered code reviews on GitHub and GitLab repositories using the Mistral AI API. Built with a hexagonal architecture (ports & adapters).

## Commands

```bash
# Install dependencies
uv sync

# Run the application (real entry point — cli.py, currently a stub)
uv run python src/main.py   # scratch file, calls Mistral directly

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/domain/test_models.py

# Lint
uv run ruff check src tests

# Format
uv run ruff format src tests
```

## Configuration

All settings are read via `pydantic-settings` from environment variables prefixed with `CR_`:

```bash
export CR_MISTRAL_API_KEY=<your_key>
export CR_GITHUB_TOKEN=<your_token>
export CR_GITLAB_TOKEN=<your_token>
export CR_ANTHROPIC_API_KEY=<your_key>  # optional
```

`Settings` is defined in `src/code_reviewer/config.py`.

## Architecture

Hexagonal architecture under `src/code_reviewer/`:

- **`domain/models.py`** — `FileToReview`, `FileAnalysis`, `ReviewReport`, `Severity`. All `frozen=True` dataclasses. No external deps.
- **`domain/ports.py`** — `RepoFetcher`, `CodeAnalyzer`, `ReportWriter` as `typing.Protocol`. `fetch_files` and `analyze` are `async`.
- **`config.py`** — `Settings` (pydantic-settings), env prefix `CR_`. Instantiate once and inject into adapters.
- **`adapters/github_repo.py`** — **Implemented.** `GitHubRepoFetcher` via PyGitHub. Filters blobs by `_LANGUAGES_BY_EXTENSION` (`.py .java .kt .ts .js`). `repo.get_contents()` returns `ContentFile | list[ContentFile]` — always assert `isinstance(result, ContentFile)` when called with a file path.
- **`adapters/gitlab_repo.py`** — **Stub.**
- **`adapters/mistral_analyzer.py`** — **Stub.** Must implement `CodeAnalyzer` protocol.
- **`adapters/markdown_reporter.py`** — **Implemented.** `MarkdownReportWriter` writes structured `.md` files; uses `_SEVERITY_ICONS` for emoji per `Severity` level.
- **`review/reviewer.py`** — **Implemented.** `CodeReviewer` orchestrates: `fetch_files` → `asyncio.gather(analyze)` → build `ReviewReport` → `write`.
- **`cli.py`** — **Stub.** Typer entry point, wires adapters together.

The domain layer has zero external dependencies. Adapters depend on the domain, never the reverse.

### Async

The pipeline is fully async. `CodeReviewer.review()` uses `asyncio.gather` to parallelize file analysis. Tests use `pytest-asyncio`; add `asyncio_mode = "auto"` to `[tool.pytest.ini_options]` in `pyproject.toml` if not already set.

## Skills disponibles

Two skills are available in `.agents/skills/`:

- **`python-design-patterns`** — KISS, SRP, composition over inheritance, rule of three, dependency injection. Invoke when designing new components or refactoring.
- **`python-mcp-server-generator`** — Generates a complete Python MCP server (FastMCP, tools, resources, stdio or HTTP transports).