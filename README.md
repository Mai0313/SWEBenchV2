# SWEBenchV2

[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/swe_bench_v2/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/swe_bench_v2/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/swe_bench_v2/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/swe_bench_v2/actions/workflows/code-quality-check.yml)
[![codecov](https://codecov.io/gh/Mai0313/swe_bench_v2/branch/master/graph/badge.svg)](https://codecov.io/gh/Mai0313/swe_bench_v2)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/swe_bench_v2/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/swe_bench_v2/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/swe_bench_v2.svg)](https://github.com/Mai0313/swe_bench_v2/graphs/contributors)

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
- **🔗 GitHub Integration**: Seamlessly connects to any GitHub repository
- **⚡ Rate Limit Handling**: Built-in GitHub API rate limit management
- **⚙️ Flexible Configuration**: Configurable extraction parameters for different use cases

## 📊 How It Works

1. **Data Extraction**: Scans GitHub repositories for merged pull requests
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
git clone https://github.com/Mai0313/swe_bench_v2.git
cd swe_bench_v2
```

1. **Install dependencies:**

```bash
uv sync
```

1. **Set up your GitHub token:**

```bash
export GITHUB_TOKEN="your_github_token_here"
```

## 📖 Usage

### Basic Usage

```python
from src.datamodule.github import GitHubPRExtractor

# Initialize the extractor
extractor = GitHubPRExtractor(
    repo_owner="owner_name",
    repo_name="repository_name",
    max_page=10,  # Limit pages to extract
    per_page=50,  # PRs per page
)

# Extract all PR data
result = extractor.extract_all_pr_data(save_json=True)
print(f"Extracted {result.total_prs} PRs from {result.repository}")
```

### Command Line Usage

```bash
# Run with default configuration
uv run python main.py

# The extracted data will be saved to ./data/{owner}/{repo}/log_{timestamp}.json
```

### Advanced Configuration

```python
extractor = GitHubPRExtractor(
    repo_owner="your_org",
    repo_name="your_repo",
    max_page=5,  # Limit to first 5 pages
    per_page=100,  # 100 PRs per page
    token="your_token",  # Optional: set token directly
)

# Check rate limits before extraction
rate_limit = extractor.get_rate_limit()
print(f"Remaining requests: {rate_limit.rate.remaining}")

# Extract data for specific PRs
merged_prs = extractor.get_merged_prs()
for pr in merged_prs[:5]:  # Process first 5 PRs
    pr_data = extractor.extract_pr_data(pr)
    print(f"Extracted data for PR #{pr.number}: {pr.title}")
```

## 📁 Output Format

The extracted data is saved in JSON format with the following structure:

```json
{
  "repository": "owner/repo",
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
│   ├── datamodule/
│   │   └── github.py          # Main extraction logic
│   └── types/
│       ├── models.py          # Data models
│       ├── prs.py            # Pull request types
│       └── limit.py          # Rate limit handling
├── tests/                     # Comprehensive test suite
├── data/                      # Output directory for extracted data
├── main.py                   # Example usage script
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

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

[Report Bug](https://github.com/Mai0313/swe_bench_v2/issues) • [Request Feature](https://github.com/Mai0313/swe_bench_v2/issues) • [Documentation](https://mai0313.github.io/swe_bench_v2/)

</div>
