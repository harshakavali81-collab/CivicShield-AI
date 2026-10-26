"""Public API contracts; reject unknown fields, oversized text and impossible coordinates."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class RiskRequest(StrictModel):
    city: str = Field(min_length=2, max_length=80)
    rainfall_24h_mm: float = Field(ge=0, le=1000)
    temperature_c: float = Field(ge=-40, le=65)
    humidity_pct: float = Field(ge=0, le=100)
    forecast_age_hours: float = Field(ge=0, le=720)

class IncidentCreate(StrictModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10, max_length=1000)
    city: str = Field(min_length=2, max_length=80)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    language: Literal["en", "te", "hi", "ta", "kn"] = "en"
    @model_validator(mode="after")
    def coordinates_together(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be provided together")
        return self

class AssistantQuestion(StrictModel):
    question: str = Field(min_length=2, max_length=300)
    language: Literal["en", "te", "hi", "ta", "kn"] = "en"

class IncidentReview(StrictModel):
    status: Literal["verified", "dismissed", "needs_info"]
    reviewer_note: str = Field(default="", max_length=500)
