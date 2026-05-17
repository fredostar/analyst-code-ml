import asyncio
from collections import Counter

from code_reviewer.domain.models import FileAnalysis, ReviewReport, Severity
from code_reviewer.domain.ports import CodeAnalyzer, RepoFetcher


class CodeReviewer:
    """Orchestre le pipeline : fetch → analyze → report."""

    def __init__(self, fetcher: RepoFetcher, analyzer: CodeAnalyzer) -> None:
        self._fetcher = fetcher
        self._analyzer = analyzer

    async def review(self, repo: str, branch: str = "main") -> ReviewReport:
        files = await self._fetcher.fetch_files(repo, branch)
        analyses = await asyncio.gather(*(self._analyzer.analyze(f) for f in files))
        return ReviewReport(
            repository_name=repo,
            branch_name=branch,
            files_analyzed=list(analyses),
            overall_summary=_build_summary(analyses),
        )


def _build_summary(analyses: list[FileAnalysis]) -> str:
    counts = Counter(analysis.severity for analysis in analyses)
    return (
        f"{len(analyses)} fichiers analysés. "
        f"{counts[Severity.CRITICAL]} problème(s) critique(s), "
        f"{counts[Severity.WARNING]} avertissement(s)."
    )