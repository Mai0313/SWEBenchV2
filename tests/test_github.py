from swebenchv2.typings.prs import PullRequest
from swebenchv2.typings.limit import RateLimit
from swebenchv2.typings.models import FileData, TrainingData, ExtractionResult
from swebenchv2.datamodule.github import GitHubPRExtractor


def test_get_rate_limit() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    rate_limit = extractor.get_rate_limit()
    assert isinstance(rate_limit, RateLimit)


def test_get_merged_prs() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    merged_prs = extractor.get_merged_prs()
    for merged_pr in merged_prs:
        assert isinstance(merged_pr, PullRequest)


def test_get_pr_files() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    pr_files = extractor.get_pr_files(pr_number=1)
    for pr_file in pr_files:
        assert isinstance(pr_file, FileData)


def test_get_file_content() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    content = extractor.get_file_content(
        file_path="README.md", sha="69ef90b8aa8c99435f2f9b7284e5d5001392bc6a"
    )
    assert isinstance(content, str)


def test_extract_pr_data() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    merged_prs = extractor.get_merged_prs()
    data = extractor.extract_pr_data(pr_info=merged_prs[0])
    assert isinstance(data, TrainingData)


def test_extract_all_pr_data() -> None:
    extractor = GitHubPRExtractor(
        repo_url="https://github.com/Mai0313/repo_template", max_page=1, per_page=1
    )
    data = extractor.extract_all_pr_data(save_json=False)
    assert isinstance(data, ExtractionResult)
    assert isinstance(data.prs, list)
    if data.prs:
        assert isinstance(data.prs[0], TrainingData)
