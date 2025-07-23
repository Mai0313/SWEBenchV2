"""GitHub PR data extractor for LLM training data generation."""

from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor


def main() -> ExtractionResult:
    # Create extractor instance
    extractor = GitHubPRExtractor()
    data = extractor.extract_all_pr_data(repo_url="https://github.com/google-gemini/gemini-cli")
    return data


if __name__ == "__main__":
    main()
