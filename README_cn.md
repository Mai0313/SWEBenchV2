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

**一個創新的 SWE-Bench 替代方案，專注於測量 AI 模型與真實開發者編程模式的相似度，而非簡單的對錯判斷。**

**其他語言版本**: [English](README.md) | [中文](README_cn.md)

## 🚀 概述

傳統的基準測試如 SWE-Bench 專注於測試模型是否能正確解決預定義問題。SWEBenchV2 採用了不同的方法：它測量 AI 模型的編程風格和決策與已經審核和批准代碼變更的經驗開發者的相似程度。

### 核心理念

我們不問「模型得到了正確答案嗎？」，而是問「模型的方法與有經驗的開發者實際做法有多相似？」

這種方法假設已合併的拉取請求代表了有經驗開發者對於「正確」實現變更方式的共識。通過將模型輸出與這些真實世界的解決方案進行比較，我們不僅可以評估正確性，還可以評估編程風格、問題解決方法和對專案慣例的遵循。

## 🎯 主要功能

- **🔍 真實世界數據**：從實際已合併的拉取請求中提取訓練數據
- **� 模式匹配**：專注於與開發者模式的相似性，而非簡單的對錯判斷
- **📋 全面分析**：捕獲修改前後的代碼狀態、PR 上下文和元數據
- **🔗 GitHub 整合**：無縫連接任何 GitHub 儲存庫
- **⚡ 速率限制處理**：內建 GitHub API 速率限制管理
- **⚙️ 靈活配置**：針對不同使用情況的可配置提取參數

## 📊 工作原理

1. **數據提取**：掃描 GitHub 儲存庫中已合併的拉取請求
2. **內容捕獲**：記錄所有修改文件的修改前後狀態
3. **上下文保存**：維護 PR 標題、描述和元數據
4. **數據集生成**：創建適用於 LLM 評估的結構化訓練數據
5. **基準創建**：提供問題-上下文-答案三元組用於模型測試

### 數據結構

每個提取的 PR 都成為一個基準項目，包含：

- **問題**：PR 標題和描述（需要解決的問題）
- **上下文**：修改文件的修改前狀態和文件名
- **期望答案**：修改文件的修改後狀態（「正確」的解決方案）

## 🛠️ 安裝

### 先決條件

- Python 3.10 或更高版本
- [uv](https://github.com/astral-sh/uv) 用於依賴管理
- GitHub API 令牌（用於訪問儲存庫）

### 設置

1. **克隆儲存庫：**

```bash
git clone https://github.com/Mai0313/swe_bench_v2.git
cd swe_bench_v2
```

1. **安裝依賴：**

```bash
uv sync
```

1. **設置您的 GitHub 令牌：**

```bash
export GITHUB_TOKEN="your_github_token_here"
```

## � 使用方法

### 基本使用

```python
from src.datamodule.github import GitHubPRExtractor

# 初始化提取器
extractor = GitHubPRExtractor(
    repo_owner="owner_name",
    repo_name="repository_name",
    max_page=10,  # 限制提取頁面數
    per_page=50,  # 每頁 PR 數量
)

# 提取所有 PR 數據
result = extractor.extract_all_pr_data(save_json=True)
print(f"從 {result.repository} 提取了 {result.total_prs} 個 PR")
```

### 命令行使用

```bash
# 使用默認配置運行
uv run python main.py

# 提取的數據將保存到 ./data/{owner}/{repo}/log_{timestamp}.json
```

### 高級配置

```python
extractor = GitHubPRExtractor(
    repo_owner="your_org",
    repo_name="your_repo",
    max_page=5,  # 限制為前 5 頁
    per_page=100,  # 每頁 100 個 PR
    token="your_token",  # 可選：直接設置令牌
)

# 提取前檢查速率限制
rate_limit = extractor.get_rate_limit()
print(f"剩餘請求數：{rate_limit.rate.remaining}")

# 為特定 PR 提取數據
merged_prs = extractor.get_merged_prs()
for pr in merged_prs[:5]:  # 處理前 5 個 PR
    pr_data = extractor.extract_pr_data(pr)
    print(f"已為 PR #{pr.number} 提取數據：{pr.title}")
```

## 📁 輸出格式

提取的數據以 JSON 格式保存，結構如下：

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
          "before_content": "# Original code...",
          "after_content": "# Modified code...",
          "additions": 5,
          "deletions": 2
        }
      ]
    }
  ]
}
```

## � 配置

### 環境變量

| 變量                  | 描述                  | 默認值                   |
| --------------------- | --------------------- | ------------------------ |
| `GITHUB_TOKEN`        | GitHub API 令牌       | 無（私有儲存庫需要）     |
| `GITHUB_API_BASE_URL` | 自定義 GitHub API URL | `https://api.github.com` |

### 速率限制

工具自動處理 GitHub API 速率限制：

- 🔍 監控剩餘請求數
- ⏳ 達到限制時自動等待
- 📝 提供關於速率限制狀態的詳細日誌

## 🤖 與 LLM 一起使用

提取的數據設計為與語言模型無縫配合：

```python
# 示例：使用提取的數據測試模型
for pr_data in result.prs:
    question = pr_data.question
    context = {"files": {file.filename: file.before_content for file in pr_data.files}}
    expected_answer = {file.filename: file.after_content for file in pr_data.files}

    # 發送給您的 LLM 並比較相似度
    model_response = your_llm.generate(question, context)
    similarity_score = calculate_similarity(model_response, expected_answer)
```

## 🗂️ 項目結構

```
├── src/
│   ├── datamodule/
│   │   └── github.py          # 主要提取邏輯
│   └── types/
│       ├── models.py          # 數據模型
│       ├── prs.py            # 拉取請求類型
│       └── limit.py          # 速率限制處理
├── tests/                     # 全面測試套件
├── data/                      # 提取數據的輸出目錄
├── main.py                   # 示例使用腳本
├── pyproject.toml            # 項目配置
└── README.md                 # 此文件
```

## 🔬 評估方法

與專注於二元正確性的傳統基準不同，SWEBenchV2 評估：

1. **代碼相似性**：生成的代碼與批准的解決方案有多相似？
2. **風格一致性**：模型是否遵循項目的編程約定？
3. **問題解決方法**：模型是否像經驗豐富的開發者一樣處理問題？
4. **上下文意識**：模型是否適當考慮了現有代碼庫模式？

## 🤝 貢獻

歡迎貢獻！您可以通過以下方式幫助：

1. **分叉儲存庫**
2. **創建功能分支**：`git checkout -b feature-name`
3. **進行更改並添加測試**
4. **提交拉取請求**

更多詳情請參閱我們的[貢獻指南](CONTRIBUTING)。

## 📊 使用案例

- **模型評估**：評估 AI 模型與真實開發者模式的匹配程度
- **訓練數據生成**：從真實儲存庫創建現實的編程數據集
- **代碼風格分析**：研究不同項目的編程模式
- **開發者行為研究**：分析有經驗的開發者如何解決問題

## 🙏 致謝

- 靈感來自原始的 [SWE-Bench](https://www.swebench.com/) 項目
- 基於真實開發者共識代表質量標準的原則
- 為 AI 輔助軟件開發時代而設計

## 📄 許可證

本項目根據 MIT 許可證授權 - 詳情請參閱 [LICENSE](LICENSE) 文件。

---

<div align="center">

**為 AI 和軟件開發社區用 ❤️ 製作**

[報告錯誤](https://github.com/Mai0313/swe_bench_v2/issues) • [請求功能](https://github.com/Mai0313/swe_bench_v2/issues) • [文檔](https://mai0313.github.io/swe_bench_v2/)

</div>

## 🤝 貢獻

我們歡迎貢獻！請隨時：

- 開啟問題回報錯誤或功能請求
- 提交拉取請求進行改進
- 分享您使用此模板的經驗

## 📖 文檔

詳細文檔請訪問：[https://mai0313.github.io/swe_bench_v2/](https://mai0313.github.io/swe_bench_v2/)

## 👥 貢獻者

[![Contributors](https://contrib.rocks/image?repo=Mai0313/swe_bench_v2)](https://github.com/Mai0313/swe_bench_v2/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks)

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。
