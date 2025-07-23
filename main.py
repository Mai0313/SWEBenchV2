"""GitHub PR data extractor for LLM training data generation."""

from pydantic import BaseModel

from src.types.models import ExtractionResult
from src.datamodule.github import GitHubPRExtractor, AsyncGitHubPRExtractor


class SWEBench(BaseModel):
    repo_url: str
    max_page: int | None = 1
    per_page: int | None = 5

    def main(self) -> ExtractionResult:
        extractor = GitHubPRExtractor(
            repo_url=self.repo_url, max_page=self.max_page, per_page=self.per_page
        )
        result = extractor.extract_all_pr_data(save_json=True)
        return result

    async def a_main(self) -> ExtractionResult:
        extractor = AsyncGitHubPRExtractor(
            repo_url=self.repo_url, max_page=self.max_page, per_page=self.per_page
        )
        result = await extractor.extract_all_pr_data(save_json=True)
        return result

    async def __call__(self) -> None:
        """Run the async extraction."""
        await self.a_main()


if __name__ == "__main__":
    import fire

    fire.Fire(SWEBench)
