from github import Auth, Github
from github.ContentFile import ContentFile
from github.Repository import Repository

from code_reviewer.config import Settings
from code_reviewer.domain.models import FileToReview

_LANGUAGES_BY_EXTENSION: dict[str, str] = {
    ".py": "python",
    ".java": "java",
    ".kt": "kotlin",
    ".ts": "typescript",
    ".js": "javascript",
}


class GitHubRepoFetcher:
    """Récupère les fichiers d'un dépôt GitHub via PyGithub."""

    def __init__(self, settings: Settings) -> None:
        self._client = Github(auth=Auth.Token(settings.github_token))

    async def fetch_files(self, repo: str, branch: str = "main") -> list[FileToReview]:
        repository = self._client.get_repo(repo)
        tree = repository.get_git_tree(sha=branch, recursive=True).tree

        return [
            _to_file(repository, entry.path, branch)
            for entry in tree
            if entry.type == "blob" and _language_for(entry.path) is not None
        ]


def _to_file(repo: Repository, path: str, branch: str) -> FileToReview:
    result = repo.get_contents(path, ref=branch)
    assert isinstance(result, ContentFile)
    language = _language_for(path)
    assert language is not None
    return FileToReview(
        path=path,
        content=result.decoded_content.decode("utf-8"),
        language=language,
    )


def _language_for(path: str) -> str | None:
    for extension, language in _LANGUAGES_BY_EXTENSION.items():
        if path.endswith(extension):
            return language
    return None