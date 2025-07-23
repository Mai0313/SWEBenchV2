from swebenchv2.typings.models import ExtractionResult
from swebenchv2.datamodule.github import (
    GitHubAPISettings,
    GitHubPRExtractor,
    AsyncGitHubPRExtractor,
)


class SWEBench(GitHubAPISettings):
    def main(self) -> ExtractionResult:
        """Extract pull request data synchronously from GitHub repository.

        Creates a synchronous GitHub PR extractor and processes all merged pull requests
        from the configured repository, saving the results to JSON format.

        Returns:
            ExtractionResult: Complete extraction results containing all PR data and metadata.
        """
        extractor = GitHubPRExtractor(
            repo_url=self.repo_url, max_page=self.max_page, per_page=self.per_page
        )
        result = extractor.extract_all_pr_data(save_json=True)
        return result

    async def a_main(self) -> ExtractionResult:
        """Extract pull request data asynchronously from GitHub repository.

        Creates an asynchronous GitHub PR extractor and processes all merged pull requests
        from the configured repository concurrently, saving the results to JSON format.

        Returns:
            ExtractionResult: Complete extraction results containing all PR data and metadata.
        """
        extractor = AsyncGitHubPRExtractor(
            repo_url=self.repo_url, max_page=self.max_page, per_page=self.per_page
        )
        result = await extractor.extract_all_pr_data(save_json=True)
        return result

    async def __call__(self) -> None:
        """Execute the asynchronous main extraction process.

        Callable interface that runs the asynchronous PR extraction workflow.
        This method is invoked when the SWEBench instance is called directly.
        """
        await self.a_main()


def main() -> None:
    """Entry point for the SWEBench CLI application.

    Initializes and runs the Fire CLI interface for the SWEBench class,
    allowing command-line access to PR extraction functionality.
    """
    import fire

    fire.Fire(SWEBench)


if __name__ == "__main__":
    main()
