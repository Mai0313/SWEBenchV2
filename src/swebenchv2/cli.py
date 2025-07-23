"""GitHub PR data extractor for LLM training data generation."""

from swebenchv2.typings.models import ExtractionResult
from swebenchv2.datamodule.github import (
    GitHubAPISettings,
    GitHubPRExtractor,
    AsyncGitHubPRExtractor,
)


class SWEBench(GitHubAPISettings):
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


def main() -> None:
    """CLI entry point."""
    import fire

    fire.Fire(SWEBench)


if __name__ == "__main__":
    main()
