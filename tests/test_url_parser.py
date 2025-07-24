from swebenchv2.datamodule.github import GitHubPRExtractorBase

short_url = "Mai0313/repo_template"
full_url = "https://github.com/Mai0313/repo_template"


def test_repo_owner_and_name():
    short = GitHubPRExtractorBase(repo_url=short_url)
    full = GitHubPRExtractorBase(repo_url=full_url)
    assert short.repo_owner == full.repo_owner == "Mai0313"
    assert short.repo_name == full.repo_name == "repo_template"
