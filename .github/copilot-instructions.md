<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: After making any code changes, adding features, or updating functionality, you MUST update .github/copilot-instructions.md to reflect the current project state and capabilities.

🎯 **DOCUMENTATION STATUS**: All functions in the codebase now include comprehensive Google-style docstrings with parameter types, return values, and detailed descriptions. This represents a major documentation improvement across the entire project.

# Project Background

SWEBenchV2 is an innovative alternative to SWE-Bench that focuses on measuring how closely AI models match real developer coding patterns rather than binary correctness. Instead of asking "Did the model get the right answer?", we ask "How closely does the model's approach match what experienced developers actually do?"

The project extracts training data from actual merged pull requests from GitHub repositories, creating benchmark datasets that capture not just correctness but also coding style, problem-solving approach, and adherence to project conventions.

# Project Structure / Features

## Core Data Extraction System

### CLI Interface (`src/swebenchv2/cli.py`)

The project provides a fully documented command-line interface for easy data extraction with multiple execution methods. All CLI functions now include comprehensive Google-style docstrings:

- **Direct CLI Usage**: `swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"`
- **Sync Mode**: `swebenchv2 main --repo_url="..."`
- **Async Mode**: `swebenchv2 a_main --repo_url="..."` (recommended for large repositories)
- **Poethepoet Task**: `poe main --repo_url="..."`
- **Python Module**: `python src/swebenchv2/cli.py --repo_url="..."`
- **UV Run CLI**: `uv run cli --repo_url="..."`
- **UV Run SWEBenchV2**: `uv run swebenchv2 --repo_url="..."`
- **Custom Parameters**: `--max_page`, `--per_page` for fine-tuning extraction
- **JSON Output**: Automatically saves to `./data/{owner}/{repo}/log_{timestamp}.json`

Installation for CLI usage:

```bash
uv pip install -e .  # Install package in development mode
export GITHUB_TOKEN="your_token_here"
swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"
```

### GitHubPRExtractor (`src/swebenchv2/datamodule/github.py`)

The main extraction engine with comprehensive documentation for all methods. Every function includes detailed Google-style docstrings covering:

- **GitHub API Integration**: Connects to GitHub repositories using authenticated API requests
- **PR Discovery**: Finds and filters merged pull requests using pagination and state filtering
- **Rate Limit Management**: Automatically handles GitHub API rate limits with intelligent waiting
- **Content Extraction**: Retrieves before/after file contents for each modified file in PRs
- **Data Structuring**: Converts raw GitHub data into structured training datasets
- **URL Parsing**: Accepts full GitHub URLs and automatically extracts Mai0313/SWEBenchV2sitory names
- **High-Performance Async**: Multi-level concurrent processing with `asyncio.gather()` optimizations

Key Classes:

- `GitHubPRExtractorBase`: Base configuration class with URL parsing and shared settings
- `GitHubPRExtractor`: Synchronous implementation for data extraction
- `AsyncGitHubPRExtractor`: Asynchronous implementation with optimized concurrent processing featuring:
    - Multi-level `asyncio.gather()` usage for maximum throughput
    - Semaphore-controlled concurrency (5 for PRs, 10 for files)
    - Parallel before/after content fetching for modified files
    - Concurrent processing across repository, PR, and file levels

Key Methods (All Fully Documented):

- `get_rate_limit()`: Checks current GitHub API rate limit status with detailed return type documentation
- `get_merged_prs()`: Retrieves all merged PRs from a repository with pagination handling documentation
- `get_pr_files()`: Gets list of files modified in a specific PR with parameter type specifications
- `get_file_content()`: Fetches file content at a specific SHA/commit with base64 decoding details
- `extract_pr_data()`: Processes a single PR into training data format with comprehensive workflow documentation
- `extract_all_pr_data()`: Orchestrates full repository extraction with complete parameter and return documentation

**Documentation Coverage**: Both synchronous and asynchronous versions include:

- Function purpose and behavior descriptions
- Complete parameter documentation with types
- Return value specifications with types
- Error handling and edge case documentation
- Performance optimization notes for async versions

## Data Models (`src/swebenchv2/typings/`)

All data models now include comprehensive documentation for their methods and functionality.

### PullRequest Model (`prs.py`)

Comprehensive Pydantic model representing GitHub PR data including:

- Basic PR info (number, title, body, state)
- User information and associations
- Merge details and timestamps
- Base and head branch information
- Repository metadata

### FileData Model (`models.py`)

Represents changes to individual files:

- File metadata (path, SHA, status)
- Change statistics (additions, deletions, total changes)
- Content states (before_edit, after_edit)
- Git patch information

### TrainingData Model (`models.py`)

Final structured format for LLM training:

- PR context (full PR information)
- Formatted question (PR title + description)
- Complete file change data
- Ready for AI model consumption

### ExtractionResult Model (`models.py`)

Container for full extraction results with documented save methods:

- Repository metadata
- Extraction timestamp
- Complete dataset of all processed PRs
- Built-in JSON export functionality with comprehensive documentation:
    - `save_log()`: Synchronous JSON export with timestamp organization documentation
    - `a_save_log()`: Asynchronous file operations with thread handling documentation

### Rate Limit Handling (`limit.py`)

Manages GitHub API quotas with documented status checking:

- Tracks remaining requests
- Monitors reset timestamps
- Provides structured rate limit information
- `is_rate_limited()`: Documented boolean check for API quota status with clear return logic

## Configuration System

### CLI Entry Points

The package is configured with CLI entry points in `pyproject.toml`:

```toml
[project.scripts]
cli = "swebenchv2.cli:main"
swebenchv2 = "swebenchv2.cli:main"
```

This allows users to run the tool directly from the command line after installation using multiple methods:

- `swebenchv2 --repo_url="..."`
- `uv run cli --repo_url="..."`
- `uv run swebenchv2 --repo_url="..."`

Additionally, there's a poethepoet task configured in `pyproject.toml`:

```toml
[tool.poe.tasks]
main = "python ./src/swebenchv2/cli.py"
```

This enables running with `poe main --repo_url="..."` for development convenience.

### Environment Variables

- `GITHUB_TOKEN`: GitHub API authentication token
- `GITHUB_API_BASE_URL`: Custom GitHub API endpoint (default: api.github.com)

### Extraction Parameters

- `repo_url`: Target repository URL (e.g., `https://github.com/Mai0313/SWEBenchV2` or `Mai0313/SWEBenchV2`)
- `max_page`: Limit pagination depth
- `per_page`: Results per API request page
- `token`: Optional direct token specification (overrides environment variable)

## Data Flow Architecture

1. **Input**: Repository specification (URL or Mai0313/SWEBenchV2 format)
2. **Discovery**: Find all merged PRs using GitHub API with intelligent pagination
3. **Analysis**: For each PR, extract file changes and content using concurrent before/after SHA fetching
4. **Processing**: Convert to structured training format with parallel file content retrieval
5. **Output**: JSON dataset ready for LLM evaluation with comprehensive metadata

### Performance Optimizations

The async implementation uses multi-level concurrency:

- **Repository Level**: All PRs processed concurrently with semaphore limits
- **PR Level**: All modified files processed simultaneously
- **File Level**: Before/after content fetched in parallel using `asyncio.gather()`
- **Rate Limiting**: Intelligent semaphore control (5 for PRs, 10 for files) to respect API limits

## Output Format

The system generates structured JSON containing:

- Repository metadata
- Extraction timestamps
- Array of training examples, each with:
    - Question: PR title and description
    - Context: Before-state of modified files (before_edit field)
    - Expected Answer: After-state of modified files (after_edit field)
    - Metadata: PR details, file statistics, change counts, etc.

## Evaluation Philosophy

Unlike traditional benchmarks that focus on binary correctness, SWEBenchV2 enables evaluation of:

- **Code Similarity**: How similar is generated code to approved solutions?
- **Style Consistency**: Does the model follow project coding conventions?
- **Problem-solving Approach**: Does the model tackle problems like experienced developers?
- **Contextual Awareness**: Does the model consider existing codebase patterns?

# Rule Sheet

## Coding Style

- Follow `ruff-check` and `ruff-format` for code style and formatting using `pre-commit` hooks
- Follow PEP 8 naming conventions:
    - snake_case for functions and variables
    - PascalCase for classes
    - UPPER_CASE for constants
- Use type hints for all function parameters and returns
- Maximum line length of 99 characters
- Use absolute imports over relative imports

## Pydantic Models

- All data models must use Pydantic for validation and serialization
- Include descriptive `Field` declarations with proper descriptions
- Use appropriate type annotations with Union types where needed
- Implement model validation for complex business logic

### Example

```python
from pydantic import BaseModel, Field
from typing import Optional


class GitHubFile(BaseModel):
    """Represents a file change in a GitHub PR.

    Attributes:
        filename: Path to the modified file
        status: Type of change (added, modified, removed)
        before_edit: File content before changes
        after_edit: File content after changes
    """

    filename: str = Field(..., description="File path and name")
    status: str = Field(..., description="File status (added, modified, removed)")
    before_edit: str = Field(default="", description="File content before changes")
    after_edit: str = Field(default="", description="File content after changes")
```

## GitHub API Integration

- Always handle rate limits gracefully with automatic waiting
- Use proper authentication headers for all requests
- Implement robust error handling for API failures
- Log all API interactions for debugging
- Cache API responses when appropriate to reduce requests
- Leverage `asyncio.gather()` for parallel API calls in async implementations

## Data Processing

- Validate all input data using Pydantic models
- Handle edge cases (deleted files, binary files, large files)
- Preserve all relevant metadata for downstream analysis
- Ensure data consistency across the entire extraction pipeline
- Optimize concurrent processing using semaphore-controlled async operations

## Error Handling

- Use structured logging with logfire for all operations
- Implement graceful degradation for API failures
- Provide clear error messages for configuration issues
- Handle network timeouts and connection errors

## Testing

- Use `pytest` for all testing, place tests in `tests/` directory
- Mock GitHub API calls in tests to avoid rate limiting
- Test edge cases (empty repos, no merged PRs, API failures)
- Validate data model serialization/deserialization

### CLI Testing (`tests/test_cli.py`)

Comprehensive CLI testing covering all execution methods and input formats. The CLI test suite includes:

#### **Execution Methods Tested**:

- `uv run cli --repo_url <url>` - UV package runner with cli entry point
- `uv run swebenchv2 --repo_url <url>` - UV package runner with swebenchv2 entry point
- `python src/swebenchv2/cli.py --repo_url <url>` - Direct Python module execution
- `poe main --repo_url <url>` - Poethepoet task runner execution

#### **Repository URL Formats Tested**:

- Short format: `"Mai0313/SWEBenchV2
- Full URL format: `"https://github.com/Mai0313/SWEBenchV2

#### **Test Categories**:

- **Mock Tests** (`TestCLIWithMockedExtraction`): Test function logic with mocked GitHub API
- **Integration Tests** (`TestIntegrationCLI`): Real subprocess execution with actual CLI commands
- **Error Handling Tests** (`TestCLIErrorHandling`): Invalid input and edge case handling
- **Documentation Tests** (`TestAsyncCLIFunctions`): Verify docstring compliance and quality

#### **Test Implementation Features**:

- Uses `@pytest.mark.parametrize` to test multiple repo URL formats efficiently
- Default test parameters: `max_page=1`, `per_page=1` to minimize GitHub API usage
- Integration tests handle authentication gracefully (pass if token missing)
- All tests include comprehensive docstrings explaining purpose and behavior
- Tests verify both successful execution and proper error handling

#### **Running CLI Tests**:

```bash
# Run all CLI tests
uv run python -m pytest tests/test_cli.py -v

# Run specific test categories
uv run python -m pytest tests/test_cli.py::TestCLIWithMockedExtraction -v
uv run python -m pytest tests/test_cli.py::TestIntegrationCLI -v

# Run with slow tests (integration tests)
uv run python -m pytest tests/test_cli.py -v -m "not slow"  # Skip slow tests
uv run python -m pytest tests/test_cli.py -v  # Run all including slow tests
```

- **Documentation Testing**: Verify that all new functions include proper docstrings
- **Test Documentation**: All test functions should also include clear docstrings explaining test purpose

## Documentation

- **COMPLETED**: All functions now use comprehensive Google-style docstrings
- **Current Status**: Every function includes parameter types, return values, and detailed descriptions
- Document all configuration options and environment variables
- Provide clear examples for common use cases
- Keep README files updated with current functionality
- **Documentation Standards**: All new functions must include:
    - Clear purpose and behavior description
    - Complete Args section with parameter types and descriptions
    - Returns section with return type and meaning
    - Examples for complex functions
    - Consistent formatting with existing codebase

## Dependencies

- Use `uv` for dependency management
- Production dependencies: `uv add <package>`
- Development dependencies: `uv add <package> --dev`
- Pin versions for reproducible builds
- Regularly update dependencies for security
