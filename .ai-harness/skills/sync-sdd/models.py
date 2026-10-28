"""Data models for sync-sdd."""

from pydantic import BaseModel, ConfigDict, Field


class SddSyncItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    spec_id: str
    spec_path: str
    target: str
    status: str
    version: str
    has_user_story: bool
    has_target: bool
    sync_state: str
    details: str = ""


class SddSyncReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    total: int
    not_applicable: int
    missing: int
    present: int
    diverged: int
    items: list[SddSyncItem] = Field(default_factory=list)
    is_successful: bool = True
