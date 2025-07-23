import time

from pydantic import BaseModel, computed_field


class RateLimitInfo(BaseModel):
    limit: int
    used: int
    remaining: int
    reset: int

    @computed_field
    @property
    def reset_time(self) -> int:
        return self.reset - int(time.time()) + 1


class RateLimitResources(BaseModel):
    core: RateLimitInfo
    search: RateLimitInfo
    graphql: RateLimitInfo
    integration_manifest: RateLimitInfo
    source_import: RateLimitInfo
    code_scanning_upload: RateLimitInfo
    code_scanning_autofix: RateLimitInfo
    actions_runner_registration: RateLimitInfo
    scim: RateLimitInfo
    dependency_snapshots: RateLimitInfo
    dependency_sbom: RateLimitInfo
    audit_log: RateLimitInfo
    audit_log_streaming: RateLimitInfo
    code_search: RateLimitInfo


class RateLimit(BaseModel):
    resources: RateLimitResources
    rate: RateLimitInfo

    def is_rate_limited(self) -> bool:
        """Check if the current rate limit has been exceeded.

        Determines whether the GitHub API rate limit has been reached
        by checking if there are any remaining API calls available.

        Returns:
            bool: True if rate limit is exceeded (no remaining calls), False otherwise.
        """
        return self.rate.remaining == 0
