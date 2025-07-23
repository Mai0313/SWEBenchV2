"""GitHub PR data extractor for LLM training data generation."""

from rich.console import Console

from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor

console = Console()


def main() -> ExtractionResult:
    extractor = GitHubPRExtractor(repo_owner="ag2ai", repo_name="ag2", max_page=10, per_page=100)
    data = extractor.extract_all_pr_data(save_json=True)
    console.print(data.model_dump())
    return data


if __name__ == "__main__":
    main()
