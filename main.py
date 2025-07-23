import os
import json
import time
import base64
from typing import Any
from datetime import datetime

from pydantic import Field, ConfigDict, computed_field
import requests
from pydantic_settings import BaseSettings


class GitHubPRExtractor(BaseSettings):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    token: str | None = Field(
        default=None,
        validation_alias="GITHUB_TOKEN",
        description="GitHub API token for authentication",
        frozen=False,
        deprecated=False,
    )
    base_url: str = Field(
        default="https://api.github.com",
        description="Base URL for GitHub API",
        frozen=False,
        deprecated=False,
    )

    @computed_field
    @property
    def session(self) -> requests.Session:
        """Headers for GitHub API requests, including authorization if token is provided."""
        headers = {
            "Authorization": f"token {self.token}" if self.token else None,
            "Accept": "application/vnd.github.v3+json",
        }
        if not self.token:
            headers.pop("Authorization")
        session = requests.Session()
        session.headers.update(headers)
        return session

    def get_merged_prs(self, repo_owner, repo_name, per_page=100):
        """获取所有已合并的 PR"""
        all_prs = []
        page = 1

        while True:
            url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls"
            params = {
                "state": "closed",
                "sort": "updated",
                "direction": "desc",
                "per_page": per_page,
                "page": page,
            }

            response = self.session.get(url, params=params)

            if response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                if reset_time:
                    wait_time = reset_time - int(time.time()) + 1
                    print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

            if response.status_code != 200:
                print(f"Error fetching PRs: {response.status_code}")
                break

            prs = response.json()
            if not prs:
                break

            # 只保留已合并的 PR
            merged_prs = [pr for pr in prs if pr["merged_at"] is not None]
            all_prs.extend(merged_prs)

            print(f"Page {page}: Found {len(merged_prs)} merged PRs")
            page += 1

            # 避免过快请求
            time.sleep(0.1)

        return all_prs

    def get_pr_files(self, repo_owner, repo_name, pr_number):
        """获取 PR 中修改的文件列表"""
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
        response = self.session.get(url)

        if response.status_code != 200:
            print(f"Error fetching PR files: {response.status_code}")
            return []

        return response.json()

    def get_file_content(self, repo_owner, repo_name, file_path, sha):
        """获取指定版本的文件内容"""
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        params = {"ref": sha}

        response = self.session.get(url, params=params)

        if response.status_code != 200:
            return None

        file_info: dict[str, Any] = response.json()
        if file_info.get("encoding") == "base64":
            try:
                content = base64.b64decode(file_info["content"]).decode("utf-8")
                return content
            except Exception as e:
                print(f"Error decoding file content: {e}")
                return None

        return file_info.get("content", "")

    def extract_pr_data(self, repo_owner, repo_name, pr):
        """提取单个 PR 的详细数据"""
        pr_number = pr["number"]
        print(f"Processing PR #{pr_number}: {pr['title']}")

        # 获取 PR 修改的文件
        files: dict[str, Any] = self.get_pr_files(repo_owner, repo_name, pr_number)

        if not files:
            return None

        # 获取 PR 的详细信息
        pr_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        pr_response = self.session.get(pr_url)

        if pr_response.status_code != 200:
            return None

        pr_detail: dict[str, Any] = pr_response.json()

        # 构建训练数据
        training_data = {
            "pr_info": {
                "number": pr_number,
                "title": pr["title"],
                "body": pr["body"] or "",
                "url": pr["html_url"],
                "created_at": pr["created_at"],
                "merged_at": pr["merged_at"],
                "author": pr["user"]["login"],
                "base_branch": pr["base"]["ref"],
                "head_branch": pr["head"]["ref"],
                "base_sha": pr["base"]["sha"],
                "head_sha": pr["head"]["sha"],
            },
            "question": self.format_question(pr),
            "files": [],
        }

        # 处理每个修改的文件
        for file_info in files:
            if file_info["status"] == "removed":
                # 文件被删除
                before_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["base"]["sha"]
                )

                file_data = {
                    "filename": file_info["filename"],
                    "status": file_info["status"],
                    "additions": file_info["additions"],
                    "deletions": file_info["deletions"],
                    "changes": file_info["changes"],
                    "before_content": before_content or "",
                    "after_content": "",
                    "patch": file_info.get("patch", ""),
                }

            elif file_info["status"] == "added":
                # 文件被添加
                after_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["head"]["sha"]
                )

                file_data = {
                    "filename": file_info["filename"],
                    "status": file_info["status"],
                    "additions": file_info["additions"],
                    "deletions": file_info["deletions"],
                    "changes": file_info["changes"],
                    "before_content": "",
                    "after_content": after_content or "",
                    "patch": file_info.get("patch", ""),
                }

            else:
                # 文件被修改
                before_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["base"]["sha"]
                )
                after_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["head"]["sha"]
                )

                file_data = {
                    "filename": file_info["filename"],
                    "status": file_info["status"],
                    "additions": file_info["additions"],
                    "deletions": file_info["deletions"],
                    "changes": file_info["changes"],
                    "before_content": before_content or "",
                    "after_content": after_content or "",
                    "patch": file_info.get("patch", ""),
                }

            training_data["files"].append(file_data)

            # 避免过快请求
            time.sleep(0.1)

        return training_data

    def format_question(self, pr):
        """格式化问题描述"""
        question = f"PR #{pr['number']}: {pr['title']}"
        if pr["body"]:
            question += f"\n\nDescription:\n{pr['body']}"
        return question

    def save_to_json(self, data, filename) -> None:
        """保存数据到 JSON 文件"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")

    def extract_all_pr_data(self, repo_url, output_file="pr_training_data.json"):
        """提取所有 PR 数据的主函数"""
        # 解析仓库 URL
        parts = repo_url.replace("https://github.com/", "").split("/")
        repo_owner = parts[0]
        repo_name = parts[1]

        print(f"Extracting data from {repo_owner}/{repo_name}")

        # 获取所有已合并的 PR
        merged_prs = self.get_merged_prs(repo_owner, repo_name)
        print(f"Found {len(merged_prs)} merged PRs")

        # 提取每个 PR 的详细数据
        all_training_data = []

        for i, pr in enumerate(merged_prs):
            try:
                pr_data = self.extract_pr_data(repo_owner, repo_name, pr)
                if pr_data:
                    all_training_data.append(pr_data)

                print(f"Processed {i + 1}/{len(merged_prs)} PRs")

                # 每处理 10 个 PR 保存一次（防止数据丢失）
                if (i + 1) % 10 == 0:
                    temp_file = f"temp_{output_file}"
                    self.save_to_json(all_training_data, temp_file)

            except Exception as e:
                print(f"Error processing PR #{pr['number']}: {e}")
                continue

        # 保存最终数据
        final_data = {
            "repository": f"{repo_owner}/{repo_name}",
            "extracted_at": datetime.now().isoformat(),
            "total_prs": len(all_training_data),
            "prs": all_training_data,
        }

        self.save_to_json(final_data, output_file)

        # 删除临时文件
        temp_file = f"temp_{output_file}"
        if os.path.exists(temp_file):
            os.remove(temp_file)

        return final_data


def main() -> None:
    # 设置 GitHub token（可选，但推荐使用以避免 API 限制）
    token = os.getenv("GITHUB_TOKEN")  # 从环境变量获取
    # 或者直接设置: token = 'your_github_token_here'

    if not token:
        print("Warning: No GitHub token provided. You may hit rate limits.")
        print("Consider setting GITHUB_TOKEN environment variable.")

    # 创建提取器实例
    extractor = GitHubPRExtractor(token)

    # 提取数据
    repo_url = "https://github.com/google-gemini/gemini-cli"
    output_file = "gemini_cli_pr_training_data.json"

    try:
        data = extractor.extract_all_pr_data(repo_url, output_file)
        print("\nExtraction completed!")
        print(f"Total PRs processed: {data['total_prs']}")
        print(f"Data saved to: {output_file}")

    except Exception as e:
        print(f"Error during extraction: {e}")


if __name__ == "__main__":
    main()
