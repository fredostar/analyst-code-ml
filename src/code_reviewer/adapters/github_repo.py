from github import Github, Auth
from github.Repository import Repository

from code_reviewer.domain.models import FileToReview
from code_reviewer.config import Settings

_EXTENSIONS = {".py", ".java", ".kt", ".ts", ".js"}


class GitHubRepoFetcher:
    """Récupère les fichiers d'un dépôt GitHub via PyGithub."""

    def __init__(self, settings: Settings) -> None:
        auth = Auth.Token(settings.github_token)
        self._client = Github(auth=auth)

    async def fetch_files(self, repo: str, branch: str = "main") -> list[FileToReview]:
        repository = self._client.get_repo(repo)
        tree = repository.get_git_tree(sha=branch, recursive=True).tree

        return [
            _to_file(repository, entry.path, branch)
            for entry in tree
            if entry.type == "blob" and _is_reviewable(entry.path)
        ]


def _to_file(repo: Repository, path: str, branch: str) -> FileToReview:
    from github.ContentFile import ContentFile
    result = repo.get_contents(path, ref=branch)
    assert isinstance(result, ContentFile)
    return FileToReview(
        path=path,
        content=result.decoded_content.decode("utf-8"),
        language=_extract_language(path),
    )


def _is_reviewable(path: str) -> bool:
    return any(path.endswith(ext) for ext in _EXTENSIONS)


def _extract_language(path: str) -> str:
    return path.rsplit(".", 1)[-1] if "." in path else "unknown"