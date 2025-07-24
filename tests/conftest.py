import pytest

from swebenchv2.datamodule.github import GitHubPRExtractor, AsyncGitHubPRExtractor


@pytest.fixture(scope="session")
def extractor() -> GitHubPRExtractor:
    extractor = GitHubPRExtractor(repo_url="Mai0313/SWEBenchV2", max_page=1, per_page=1)
    return extractor


@pytest.fixture(scope="session")
def async_extractor() -> AsyncGitHubPRExtractor:
    async_extractor = AsyncGitHubPRExtractor(
        repo_url="https://github.com/Mai0313/SWEBenchV2", max_page=1, per_page=1
    )
    return async_extractor
