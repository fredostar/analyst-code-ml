from pathlib import Path

from code_reviewer.domain.models import FileAnalysis, ReviewReport, Severity

_SEVERITY_ICONS: dict[Severity, str] = {
    Severity.INFO: "ℹ️",
    Severity.WARNING: "⚠️",
    Severity.CRITICAL: "🔴",
}


class MarkdownReportWriter:
    """Génère un fichier .md structuré à partir du rapport de revue."""

    def write(self, report: ReviewReport, output_path: str) -> str:
        lines = [
            f"# Revue de code — {report.repository_name}",
            f"**Branche** : `{report.branch_name}`  ",
            f"**Fichiers analysés** : {len(report.files_analyzed)}",
            "",
            "## Synthèse globale",
            report.overall_summary,
            "",
        ]
        for analysis in report.files_analyzed:
            lines.extend(_render_file_section(analysis))

        Path(output_path).write_text("\n".join(lines), encoding="utf-8")
        return output_path


def _render_file_section(analysis: FileAnalysis) -> list[str]:
    icon = _SEVERITY_ICONS[analysis.severity]
    section = [
        f"## {icon} `{analysis.path}`",
        analysis.summary,
        "",
    ]
    if analysis.issues:
        section.append("### Problèmes")
        section.extend(f"- {issue}" for issue in analysis.issues)
        section.append("")
    if analysis.suggestions:
        section.append("### Suggestions")
        section.extend(f"- {suggestion}" for suggestion in analysis.suggestions)
        section.append("")
    return section