# SWEBenchV2

[![PyPI version](https://img.shields.io/pypi/v/swebenchv2.svg)](https://pypi.org/project/swebenchv2/)
[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/SWEBenchV2/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/SWEBenchV2/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/SWEBenchV2/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/SWEBenchV2/actions/workflows/code-quality-check.yml)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/SWEBenchV2/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/SWEBenchV2/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/SWEBenchV2.svg)](https://github.com/Mai0313/SWEBenchV2/graphs/contributors)

**An innovative alternative to SWE-Bench that focuses on measuring how closely AI models match real developer coding patterns rather than binary correctness.**

**Other Languages**: [English](README.md) | [中文](README_cn.md)

## 🚀 Overview

Traditional benchmarks like SWE-Bench test whether models can solve predefined problems correctly. SWEBenchV2 takes a different approach: it measures how similar an AI model's coding style and decisions are to those of experienced developers who have already reviewed and approved the code changes.

### Core Philosophy

Instead of asking "Did the model get the right answer?", we ask "How closely does the model's approach match what experienced developers actually do?"

This approach assumes that merged pull requests represent consensus among experienced developers about the "right" way to implement changes. By comparing model outputs to these real-world solutions, we can evaluate not just correctness but also coding style, problem-solving approach, and adherence to project conventions.

## 🎯 Key Features

- **🔍 Real-world Data**: Extracts training data from actual merged pull requests
- **📊 Pattern Matching**: Focuses on similarity to developer patterns rather than binary correctness
- **📋 Comprehensive Analysis**: Captures before/after code states, PR context, and metadata
- **🔗 GitHub & Gitea Integration**: Seamlessly connects to any GitHub or Gitea repository
- **⚡ High-Performance Async**: Multi-level concurrent processing with `asyncio.gather()` for maximum speed
- **🚦 Smart Rate Limiting**: Built-in GitHub API rate limit management with semaphore-based concurrency control
- **⚙️ Flexible Configuration**: Configurable extraction parameters for different use cases
- **📚 Comprehensive Documentation**: All functions include detailed Google-style docstrings with parameter types and return values

## 📊 How It Works

1. **Data Extraction**: Scans GitHub or Gitea repositories for merged pull requests
2. **Content Capture**: Records the before and after states of all modified files
3. **Context Preservation**: Maintains PR titles, descriptions, and metadata
4. **Dataset Generation**: Creates structured training data suitable for LLM evaluation
5. **Benchmark Creation**: Provides question-context-answer triplets for model testing

### Data Structure

Each extracted PR becomes a benchmark item with:

- **Question**: PR title and description (the problem to solve)
- **Context**: Before-state of modified files and filenames
- **Expected Answer**: After-state of modified files (the "correct" solution)

## �️ Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- GitHub API token (for accessing repositories)

### Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Mai0313/SWEBenchV2.git
cd SWEBenchV2
```

1. **Install dependencies:**

```bash
uv sync
```

1. **Install as a package (for CLI usage):**

```bash
uv pip install -e .
```

1. **Set up your GitHub token:**

```bash
export GITHUB_TOKEN="your_github_token_here"
```

## 📖 Usage

### CLI Usage (Recommended)

After installing the package, you can use the `swebenchv2` command directly:

```bash
# Basic usage - extract PRs from a GitHub repository
swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Extract PRs from a Gitea repository
swebenchv2 --repo_url="https://gitea.com/gitea/gitea-mcp"

# With custom parameters
swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2" --max_page=5 --per_page=50

# Using synchronous mode
swebenchv2 main --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Using asynchronous mode (faster for large repositories)
swebenchv2 a_main --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Works with Gitea repositories too
swebenchv2 --repo_url="https://gitea.com/gitea/gitea-mcp"

# The extracted data will be saved to ./data/{owner}/{repo}/log_{timestamp}.json
```

### Python Library Usage

```python
from swebenchv2.datamodule.github import GitHubPRExtractor
from swebenchv2.datamodule.gitea import GiteaPRExtractor

# Initialize the GitHub extractor
github_extractor = GitHubPRExtractor(
    repo_url="https://github.com/Mai0313/SWEBenchV2",
    max_page=10,  # Limit pages to extract
    per_page=50,  # PRs per page
)

# Initialize the Gitea extractor
gitea_extractor = GiteaPRExtractor(
    repo_url="https://gitea.com/gitea/gitea-mcp", max_page=10, per_page=50
)

# Extract all PR data from GitHub - now with comprehensive docstrings
github_result = github_extractor.extract_all_pr_data(save_json=True)
print(f"Extracted {github_result.total_prs} PRs from {github_result.repository}")

# Extract all PR data from Gitea
gitea_result = gitea_extractor.extract_all_pr_data(save_json=True)
print(f"Extracted {gitea_result.total_prs} PRs from {gitea_result.repository}")

# All methods now include detailed documentation
# Check rate limits before extraction (GitHub only)
rate_limit = github_extractor.get_rate_limit()  # Returns RateLimit with remaining calls info
print(f"Remaining requests: {rate_limit.rate.remaining}")

# Get specific PR files with full documentation
merged_prs = github_extractor.get_merged_prs()  # Returns list[PullRequest] with pagination
for pr in merged_prs[:3]:
    files = github_extractor.get_pr_files(pr.number)  # Returns list[FileData] for modified files
    print(f"PR #{pr.number} modified {len(files)} files")
```

### Alternative Execution Methods

You can run the tool in several different ways:

```bash
# Method 1: Direct CLI (after pip install -e .)
swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Method 2: Using poethepoet task
poe main --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Method 3: Direct Python module execution
python src/swebenchv2/cli.py --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Method 4: Using uv run with cli entry point
uv run cli --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Method 5: Using uv run with swebenchv2 entry point
uv run swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"

# Method 6: Using uvx (new addition)
uvx swebenchv2 --repo_url="https://github.com/Mai0313/SWEBenchV2"

# All methods work with Gitea repositories too
swebenchv2 --repo_url="https://gitea.com/gitea/gitea-mcp"
uvx swebenchv2 --repo_url="https://gitea.com/gitea/gitea-mcp"

# The extracted data will be saved to ./data/{owner}/{repo}/log_{timestamp}.json
```

### Advanced Configuration

```python
# GitHub configuration
github_extractor = GitHubPRExtractor(
    repo_url="https://github.com/your_org/your_repo",
    max_page=5,  # Limit to first 5 pages
    per_page=100,  # 100 PRs per page
    token="your_token",  # Optional: set token directly
)

# Gitea configuration
gitea_extractor = GiteaPRExtractor(
    repo_url="https://gitea.com/your_org/your_repo",
    max_page=5,
    per_page=100,
    token="your_gitea_token",  # Optional: set Gitea token directly
)

# Check rate limits before extraction (GitHub only)
rate_limit = github_extractor.get_rate_limit()
print(f"Remaining requests: {rate_limit.rate.remaining}")

# Extract data for specific PRs from GitHub
merged_prs = github_extractor.get_merged_prs()
for pr in merged_prs[:5]:  # Process first 5 PRs
    pr_data = github_extractor.extract_pr_data(pr)
    print(f"Extracted data for PR #{pr.number}: {pr.title}")

# Extract data from Gitea (no rate limit checking needed)
gitea_merged_prs = gitea_extractor.get_merged_prs()
for pr in gitea_merged_prs[:5]:
    pr_data = gitea_extractor.extract_pr_data(pr)
    print(f"Extracted Gitea PR #{pr.number}: {pr.title}")
```

### Asynchronous Usage

For better performance with large repositories, use the asynchronous version with optimized concurrent processing:

```python
import asyncio
from swebenchv2.datamodule.github import AsyncGitHubPRExtractor
from swebenchv2.datamodule.gitea import AsyncGiteaPRExtractor


async def extract_data():
    # GitHub async extraction
    github_extractor = AsyncGitHubPRExtractor(
        repo_url="https://github.com/your_org/your_repo", max_page=5, per_page=100
    )

    # Gitea async extraction
    gitea_extractor = AsyncGiteaPRExtractor(
        repo_url="https://gitea.com/your_org/your_repo", max_page=5, per_page=100
    )

    # Async extraction with multi-level concurrency
    # - File content fetching: concurrent before/after retrieval
    # - PR processing: concurrent file handling with semaphore control
    # - Batch processing: concurrent PR extraction across repository
    github_result = await github_extractor.extract_all_pr_data(save_json=True)
    gitea_result = await gitea_extractor.extract_all_pr_data(save_json=True)

    print(f"Extracted {github_result.total_prs} GitHub PRs with high-speed async processing")
    print(f"Extracted {gitea_result.total_prs} Gitea PRs with high-speed async processing")
    return github_result, gitea_result


# Run async extraction
github_result, gitea_result = asyncio.run(extract_data())
```

### Performance Benefits

The async implementation provides significant performance improvements:

- **Concurrent File Processing**: Before/after content fetched simultaneously using `asyncio.gather()`
- **Parallel PR Handling**: Multiple PRs processed concurrently with semaphore-controlled limits
- **Batch API Optimization**: Reduced total execution time through intelligent parallel operations
- **Resource Efficiency**: Optimal utilization of network resources and API rate limits

Example performance improvements observed:

- Large repositories: 3-5x faster extraction compared to synchronous implementation
- Medium repositories: 2-3x speed improvement with concurrent processing
- Better API rate limit utilization through intelligent batching

## 📁 Output Format

The extracted data is saved in JSON format with the following structure:

```json
{
  "repository": "Mai0313/SWEBenchV2",
  "extracted_at": "2024-01-01T12:00:00",
  "total_prs": 100,
  "prs": [
    {
      "pr_info": {
        "number": 123,
        "title": "Fix bug in authentication",
        "body": "This PR fixes the authentication issue...",
        "merged_at": "2024-01-01T10:00:00Z"
      },
      "question": "PR #123: Fix bug in authentication\nDescription:\nThis PR fixes...",
      "files": [
        {
          "filename": "src/auth.py",
          "status": "modified",
          "before_edit": "# Original code...",
          "after_edit": "# Modified code...",
          "additions": 5,
          "deletions": 2
        }
      ]
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

| Variable              | Description           | Default                           |
| --------------------- | --------------------- | --------------------------------- |
| `GITHUB_TOKEN`        | GitHub API token      | None (required for private repos) |
| `GITHUB_API_BASE_URL` | Custom GitHub API URL | `https://api.github.com`          |
| `GITEA_TOKEN`         | Gitea API token       | None (required for private repos) |
| `GITEA_API_BASE_URL`  | Custom Gitea API URL  | `https://gitea.com/api/v1`        |

### Rate Limiting

The tool automatically handles GitHub API rate limits:

- 🔍 Monitors remaining requests
- ⏳ Automatically waits when limits are hit
- 📝 Provides informative logging about rate limit status

## 🤖 Using with LLMs

The extracted data is designed to work seamlessly with language models:

```python
# Example: Testing a model against extracted data
for pr_data in result.prs:
    question = pr_data.question
    context = {"files": {file.filename: file.before_edit for file in pr_data.files}}
    expected_answer = {file.filename: file.after_edit for file in pr_data.files}

    # Send to your LLM and compare similarity
    model_response = your_llm.generate(question, context)
    similarity_score = calculate_similarity(model_response, expected_answer)
```

## 🗂️ Project Structure

```
├── src/
│   └── swebenchv2/
│       ├── cli.py                # CLI interface with documented entry points
│       ├── datamodule/
│       │   ├── github.py         # GitHub extraction logic with comprehensive docstrings
│       │   └── gitea.py          # Gitea extraction logic with comprehensive docstrings
│       └── typings/
│           ├── models.py         # Data models with documented save methods
│           ├── prs.py           # GitHub pull request types and enums
│           ├── gitea_prs.py     # Gitea pull request types and enums
│           └── limit.py         # Rate limit handling with status checking
├── tests/                        # Comprehensive test suite
├── data/                         # Output directory for extracted data
├── pyproject.toml               # Project configuration with CLI entry points
└── README.md                    # This file
```

### Key Functions Documentation

All core functions now include comprehensive Google-style docstrings:

**CLI Functions (`cli.py`)**:

- `SWEBench.main()` - Synchronous PR extraction with full documentation
- `SWEBench.a_main()` - Asynchronous PR extraction with performance notes
- `SWEBench.__call__()` - Callable interface documentation
- `main()` - CLI entry point with Fire integration details

**GitHub Integration (`github.py`)** and **Gitea Integration (`gitea.py`)**:

- `GitHubPRExtractor.get_rate_limit()` - Rate limit checking with return type info
- `GitHubPRExtractor.get_merged_prs()` - PR fetching with pagination details
- `GitHubPRExtractor.get_pr_files()` - File extraction with metadata handling
- `GitHubPRExtractor.get_file_content()` - Content retrieval with SHA handling
- `GitHubPRExtractor.extract_pr_data()` - Single PR processing documentation
- `GitHubPRExtractor.extract_all_pr_data()` - Complete extraction orchestration

**Async Versions** - All async methods include concurrency and performance documentation

**Data Models (`models.py`)**:

- `ExtractionResult.save_log()` - JSON export with timestamp organization
- `ExtractionResult.a_save_log()` - Async file operations documentation

**Rate Limiting (`limit.py`)**:

- `RateLimit.is_rate_limited()` - API quota checking with boolean logic

## 🔬 Evaluation Methodology

Unlike traditional benchmarks that focus on binary correctness, SWEBenchV2 evaluates:

1. **Code Similarity**: How similar is the generated code to the approved solution?
2. **Style Consistency**: Does the model follow the project's coding conventions?
3. **Problem-solving Approach**: Does the model tackle problems the same way experienced developers do?
4. **Contextual Awareness**: Does the model properly consider existing codebase patterns?

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes with tests**
4. **Submit a pull request**

Please see our [Contributing Guidelines](CONTRIBUTING) for more details.

## � Use Cases

- **Model Evaluation**: Assess how well AI models match real developer patterns
- **Training Data Generation**: Create realistic coding datasets from real repositories
- **Code Style Analysis**: Study coding patterns across different projects
- **Developer Behavior Research**: Analyze how experienced developers solve problems

## � Acknowledgments

- Inspired by the original [SWE-Bench](https://www.swebench.com/) project
- Built on the principle that real developer consensus represents quality standards
- Designed for the era of AI-assisted software development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for the AI and software development community**

[Report Bug](https://github.com/Mai0313/SWEBenchV2/issues) • [Request Feature](https://github.com/Mai0313/SWEBenchV2/issues) • [Documentation](https://mai0313.github.io/SWEBenchV2/)

</div>
