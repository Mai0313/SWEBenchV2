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
        return self.rate.remaining == 0
