import pytest

from swebenchv2.typings.models import FileData, TrainingData, ExtractionResult
from swebenchv2.datamodule.gitea import GiteaPRExtractor, AsyncGiteaPRExtractor
from swebenchv2.typings.gitea_prs import GiteaPullRequest

short_url = "gitea/gitea-mcp"
full_url = "https://gitea.com/gitea/gitea-mcp"


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
def test_get_merged_prs(repo_url: str) -> None:
    extractor = GiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    merged_prs = extractor.get_merged_prs()
    for merged_pr in merged_prs:
        assert isinstance(merged_pr, GiteaPullRequest)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
@pytest.mark.asyncio
async def test_get_merged_prs_async(repo_url: str) -> None:
    extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    merged_prs = await extractor.get_merged_prs()
    for merged_pr in merged_prs:
        assert isinstance(merged_pr, GiteaPullRequest)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
def test_get_pr_files(repo_url: str) -> None:
    extractor = GiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    pr_files = extractor.get_pr_files(pr_number=1)
    for pr_file in pr_files:
        assert isinstance(pr_file, FileData)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
@pytest.mark.asyncio
async def test_get_pr_files_async(repo_url: str) -> None:
    extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    pr_files = await extractor.get_pr_files(pr_number=1)
    for pr_file in pr_files:
        assert isinstance(pr_file, FileData)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
def test_get_file_content(repo_url: str) -> None:
    extractor = GiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    content = extractor.get_file_content(
        file_path="README.md", sha="69ef90b8aa8c99435f2f9b7284e5d5001392bc6a"
    )
    assert isinstance(content, str)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
@pytest.mark.asyncio
async def test_get_file_content_async(repo_url: str) -> None:
    extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    content = await extractor.get_file_content(
        file_path="README.md", sha="69ef90b8aa8c99435f2f9b7284e5d5001392bc6a"
    )
    assert isinstance(content, str)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
def test_extract_pr_data(repo_url: str) -> None:
    extractor = GiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    merged_prs = extractor.get_merged_prs()
    data = extractor.extract_pr_data(pr_info=merged_prs[0])
    assert isinstance(data, TrainingData)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
@pytest.mark.asyncio
async def test_extract_pr_data_async(repo_url: str) -> None:
    extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    merged_prs = await extractor.get_merged_prs()
    data = await extractor.extract_pr_data(pr_info=merged_prs[0])
    assert isinstance(data, TrainingData)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
def test_extract_all_pr_data(repo_url: str) -> None:
    extractor = GiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    data = extractor.extract_all_pr_data(save_json=False)
    assert isinstance(data, ExtractionResult)
    assert isinstance(data.prs, list)
    if data.prs:
        assert isinstance(data.prs[0], TrainingData)


@pytest.mark.parametrize(argnames="repo_url", argvalues=[full_url])
@pytest.mark.asyncio
async def test_extract_all_pr_data_async(repo_url: str) -> None:
    extractor = AsyncGiteaPRExtractor(repo_url=repo_url, max_page=1, per_page=1)
    data = await extractor.extract_all_pr_data(save_json=False)
    assert isinstance(data, ExtractionResult)
    assert isinstance(data.prs, list)
    if data.prs:
        assert isinstance(data.prs[0], TrainingData)
