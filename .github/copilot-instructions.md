<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: After making any code changes, adding features, or updating functionality, you MUST update .github/copilot-instructions.md to reflect the current project state and capabilities.

# Project Background

SWEBenchV2 is an innovative alternative to SWE-Bench that focuses on measuring how closely AI models match real developer coding patterns rather than binary correctness. Instead of asking "Did the model get the right answer?", we ask "How closely does the model's approach match what experienced developers actually do?"

The project extracts training data from actual merged pull requests from GitHub repositories, creating benchmark datasets that capture not just correctness but also coding style, problem-solving approach, and adherence to project conventions.

# Project Structure / Features

## Core Data Extraction System

### GitHubPRExtractor (`src/datamodule/github.py`)

The main extraction engine that handles:

- **GitHub API Integration**: Connects to GitHub repositories using authenticated API requests
- **PR Discovery**: Finds and filters merged pull requests using pagination and state filtering
- **Rate Limit Management**: Automatically handles GitHub API rate limits with intelligent waiting
- **Content Extraction**: Retrieves before/after file contents for each modified file in PRs
- **Data Structuring**: Converts raw GitHub data into structured training datasets

Key Methods:

- `get_rate_limit()`: Checks current GitHub API rate limit status
- `get_merged_prs()`: Retrieves all merged PRs from a repository with pagination
- `get_pr_files()`: Gets list of files modified in a specific PR
- `get_file_content()`: Fetches file content at a specific SHA/commit
- `extract_pr_data()`: Processes a single PR into training data format
- `extract_all_pr_data()`: Orchestrates full repository extraction

## Data Models (`src/types/`)

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

Container for full extraction results:

- Repository metadata
- Extraction timestamp
- Complete dataset of all processed PRs
- Built-in JSON export functionality

### Rate Limit Handling (`limit.py`)

Manages GitHub API quotas:

- Tracks remaining requests
- Monitors reset timestamps
- Provides structured rate limit information

## Configuration System

### Environment Variables

- `GITHUB_TOKEN`: GitHub API authentication token
- `GITHUB_API_BASE_URL`: Custom GitHub API endpoint (default: api.github.com)

### Extraction Parameters

- `repo_owner`: Target repository owner/organization
- `repo_name`: Target repository name
- `max_page`: Limit pagination depth
- `per_page`: Results per API request page

## Data Flow Architecture

1. **Input**: Repository specification (owner/repo)
2. **Discovery**: Find all merged PRs using GitHub API
3. **Analysis**: For each PR, extract file changes and content
4. **Processing**: Convert to structured training format
5. **Output**: JSON dataset ready for LLM evaluation

## Output Format

The system generates structured JSON containing:

- Repository metadata
- Extraction timestamps
- Array of training examples, each with:
    - Question: PR title and description
    - Context: Before-state of modified files
    - Expected Answer: After-state of modified files
    - Metadata: PR details, file statistics, etc.

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

## Data Processing

- Validate all input data using Pydantic models
- Handle edge cases (deleted files, binary files, large files)
- Preserve all relevant metadata for downstream analysis
- Ensure data consistency across the entire extraction pipeline

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

## Documentation

- Use Google-style docstrings for all functions and classes
- Document all configuration options and environment variables
- Provide clear examples for common use cases
- Keep README files updated with current functionality

## Dependencies

- Use `uv` for dependency management
- Production dependencies: `uv add <package>`
- Development dependencies: `uv add <package> --dev`
- Pin versions for reproducible builds
- Regularly update dependencies for security
