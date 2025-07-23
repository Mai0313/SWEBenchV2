"""GitHub PR data extractor for LLM training data generation."""

from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor


def main() -> ExtractionResult:
    extractor = GitHubPRExtractor(repo_url="https://github.com/ag2ai/ag2", max_page=1, per_page=5)
    data = extractor.extract_all_pr_data(save_json=True)
    return data


if __name__ == "__main__":
    main()
