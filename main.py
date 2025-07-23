"""GitHub PR data extractor for LLM training data generation."""

from src.types.prs import PullRequest
from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor


def test_get_merged_prs() -> list[PullRequest]:
    extractor = GitHubPRExtractor()
    extractor.get_rate_limit()  # Ensure rate limit is fetched
    merged_prs = extractor.get_merged_prs(
        repo_owner="mai0313", repo_name="repo_template", per_page=1
    )
    return merged_prs


def main() -> ExtractionResult:
    extractor = GitHubPRExtractor()
    data = extractor.extract_all_pr_data(repo_url="https://github.com/mai0313/repo_template")
    return data


if __name__ == "__main__":
    test_get_merged_prs()
