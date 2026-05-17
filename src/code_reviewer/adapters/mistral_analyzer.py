import json

from mistralai import Mistral

from code_reviewer.config import Settings
from code_reviewer.domain.models import FileAnalysis, FileToReview, Severity

_MODEL = "mistral-small-latest"

_SYSTEM_PROMPT = """Tu es un expert en revue de code. Analyse le fichier fourni et réponds UNIQUEMENT avec du JSON valide, sans markdown ni explication :
{
  "summary": "résumé en 1-2 phrases",
  "issues": ["liste des problèmes détectés"],
  "suggestions": ["liste des suggestions d'amélioration"],
  "severity": "INFO"
}
Règles pour severity : CRITICAL si faille de sécurité ou bug bloquant, WARNING si mauvaise pratique ou code smell, INFO sinon."""


class MistralAnalyzer:
    def __init__(self, settings: Settings) -> None:
        self._client = Mistral(api_key=settings.mistral_api_key)

    async def analyze(self, file: FileToReview) -> FileAnalysis:
        prompt = f"Fichier : {file.path} ({file.language})\n\n```{file.language}\n{file.content}\n```"
        response = await self._client.chat.complete_async(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        raw = response.choices[0].message.content.strip()
        return _parse_analysis(file.path, raw)


def _parse_analysis(path: str, raw: str) -> FileAnalysis:
    try:
        data = json.loads(raw)
        return FileAnalysis(
            path=path,
            summary=data.get("summary", ""),
            issues=data.get("issues", []),
            suggestions=data.get("suggestions", []),
            severity=Severity(data.get("severity", "INFO")),
        )
    except (json.JSONDecodeError, ValueError):
        return FileAnalysis(
            path=path,
            summary=raw[:200],
            issues=[],
            suggestions=[],
            severity=Severity.INFO,
        )