from swebenchv2.datamodule.github import AsyncGitHubPRExtractor
from swebenchv2.datamodule.gitea import AsyncGiteaPRExtractor


async def extract(repo_url: str, max_page: int = 1, per_page: int = 1) -> None:
    """Extract training data from GitHub repository pull requests asynchronously.

    This function serves as the main CLI entry point for extracting training data from merged pull requests in a GitHub repository.
    It creates an AsyncGitHubPRExtractor instance and orchestrates the complete data extraction process, automatically saving results to a JSON file in the ./data/{owner}/{repo}/ directory.

    Args:
        repo_url (str): GitHub repository URL or Mai0313/SWEBenchV2 format, e.g., `https://github.com/Mai0313/SWEBenchV2` or `Mai0313/SWEBenchV2`.
        max_page (int, optional): Maximum number of pages to fetch for PRs, Defaults to 1.
        per_page (int, optional): Number of PRs to fetch per API request page, Defaults to 1.

    Returns:
        None: Results are automatically saved to JSON file in ./data/ directory.

    Raises:
        ValueError: If repo_url format is invalid or repository doesn't exist.
        httpx.HTTPError: If GitHub API requests fail or authentication is invalid.
        RateLimitError: If GitHub API rate limit is exceeded (handled with automatic waiting).

    Example:
        Basic usage with minimal extraction:
        >>> await extract("Mai0313/SWEBenchV2")

        Complete repository extraction:
        >>> await extract("https://github.com/Mai0313/SWEBenchV2", max_page=None, per_page=100)

        Custom pagination for large repositories:
        >>> await extract("Mai0313/SWEBenchV2", max_page=10, per_page=50)

    Note:
        - Requires GITHUB_TOKEN environment variable for API authentication
        - Output files are saved to ./data/{owner}/{repo}/log_{timestamp}.json
        - Uses asynchronous processing for optimal performance with concurrent API calls
        - Automatically handles GitHub API rate limits with intelligent waiting
    """
    if "github.com" in repo_url:
        extractor = AsyncGitHubPRExtractor(repo_url=repo_url, max_page=max_page, per_page=per_page)
    else:
        extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=max_page, per_page=per_page)
    await extractor.extract_all_pr_data(save_json=True)


def main() -> None:
    import fire

    fire.Fire(extract)


if __name__ == "__main__":
    main()
