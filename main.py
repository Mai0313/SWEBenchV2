"""GitHub PR data extractor for LLM training data generation."""

from rich.console import Console

from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor

console = Console()


def main() -> ExtractionResult:
    extractor = GitHubPRExtractor(
        repo_owner="mai0313", repo_name="repo_template", max_page=1, per_page=1
    )
    data = extractor.extract_all_pr_data(save_json=True)
    console.print(data.model_dump())
    return data


if __name__ == "__main__":
    main()
