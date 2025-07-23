"""GitHub PR data extractor for LLM training data generation."""

from rich.console import Console

from src.types.prs import PullRequest
from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor

console = Console()


def test_get_merged_prs() -> list[PullRequest]:
    extractor = GitHubPRExtractor(repo_owner="mai0313", repo_name="repo_template")
    extractor.get_rate_limit()  # Ensure rate limit is fetched
    merged_prs = extractor.get_merged_prs(per_page=1)
    console.print(merged_prs)
    return merged_prs


def main() -> ExtractionResult:
    extractor = GitHubPRExtractor(repo_owner="mai0313", repo_name="repo_template")
    data = extractor.extract_all_pr_data()
    return data


if __name__ == "__main__":
    test_get_merged_prs()
