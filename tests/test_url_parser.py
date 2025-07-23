from swebenchv2.datamodule.github import GitHubPRExtractorBase


def test_repo_owner_and_name():
    http_url = GitHubPRExtractorBase(repo_url="https://github.com/Mai0313/SWEBenchV2")
    repo_name = GitHubPRExtractorBase(repo_url="Mai0313/SWEBenchV2")
    assert http_url.repo_owner == repo_name.repo_owner == "Mai0313"
    assert http_url.repo_name == repo_name.repo_name == "SWEBenchV2"
