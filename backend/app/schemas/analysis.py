from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnalyzeUrlRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)


class FindingSchema(BaseModel):
    code: str
    title: str
    description: str
    weight: int


class AnalysisResponse(BaseModel):
    id: int
    original_url: str
    normalized_url: str
    domain: str | None
    scheme: str | None
    risk_score: int
    risk_level: RiskLevelEnum
    findings: list[FindingSchema]
    explanation: str
    recommendations: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisListResponse(BaseModel):
    items: list[AnalysisResponse]
    limit: int
    offset: int
    total: int


class ReportResponse(BaseModel):
    analysis_id: int
    report_markdown: str


class HealthResponse(BaseModel):
    status: str
    service: str


class AnalysisListParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    risk_level: RiskLevelEnum | None = None

    @field_validator("risk_level", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value
