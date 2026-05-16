from code_reviewer.domain.models import ReviewReport
from code_reviewer.domain.ports import RepoFetcher, CodeAnalyzer, ReportWriter

class CodeReviewer:
    """Orchestre le pipeline : fetch → analyze → report."""

    def __init__(
            self,
            fetcher: RepoFetcher,
            analyzer: CodeAnalyzer,
            writer: ReportWriter,
    ) -> None:
        self._fetcher = fetcher
        self._analyzer = analyzer
        self._writer = writer

    async def review(self, repo: str, branch: str, output_path: str) -> str:
        files = await self._fetcher.fetch_files(repo, branch)
        analyses = [await self._analyzer.analyze(f) for f in files]

        report = ReviewReport(
            repo_name=repo,
            branch=branch,
            files_analyzed=analyses,
            overall_summary=_build_summary(analyses),
        )
        return self._writer.write(report, output_path)

def _build_summary(analyses: list) -> str:
    total = len(analyses)
    criticals = sum(1 for a in analyses if a.severity.value == "critical")
    warnings = sum(1 for a in analyses if a.severity.value == "warning")
    return (
        f"{total} fichiers analysés. "
        f"{criticals} problème(s) critique(s), {warnings} avertissement(s)."
    )