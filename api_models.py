"""
api_models.py

Pydantic request/response models for the backend API.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural-language analytics question")
    include_sql: bool = Field(default=True, description="Whether to include SQL in the response")


class QueryResponse(BaseModel):
    status: Literal["ok", "error"]
    question: str
    rewritten_question: str | None = None
    sql: str | None = None
    answer: str | None = None
    insights: list[str] = Field(default_factory=list)
    chart: str | None = None
    explanation: str | None = None
    llm: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    plan: dict[str, Any] | None = None
    error: str | None = None


class DashboardResponse(BaseModel):
    status: Literal["ok", "error"]
    sql: str | list[str] | None = None
    kpis: list[dict[str, Any]] = Field(default_factory=list)
    impactAnalysis: dict[str, Any] | None = None
    revenueOrderTrend: list[dict[str, Any]] = Field(default_factory=list)
    topStates: list[dict[str, Any]] = Field(default_factory=list)
    topPerformers: list[dict[str, Any]] = Field(default_factory=list)
    worstPerformers: list[dict[str, Any]] = Field(default_factory=list)
    aovTrend: list[dict[str, Any]] = Field(default_factory=list)
    insights: list[str] = Field(default_factory=list)
    explanation: str | None = None
    chart: str | None = None
    llm: dict[str, Any] | None = None
    error: str | None = None
