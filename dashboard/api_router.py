"""
api_router.py

FastAPI routes for query and dashboard access.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import APIRouter, HTTPException

from api_models import DashboardResponse, QueryRequest, QueryResponse
from orchestrator import Orchestrator


router = APIRouter()


# ---------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_orchestrator() -> Orchestrator:
    return Orchestrator()


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@router.get("/health")
def health() -> dict[str, Any]:
    orchestrator = get_orchestrator()

    return {
        "status": "ok",
        "semantic_layer": orchestrator.semantic.dataset.get(
            "name",
            "unknown",
        ),
        "databricks": (
            "configured"
            if orchestrator.data_agent
            else "unknown"
        ),
        "llm_provider": orchestrator.llm.provider,
    }


# ---------------------------------------------------------
# Query
# ---------------------------------------------------------

@router.post(
    "/query",
    response_model=QueryResponse,
)
def query(payload: QueryRequest) -> QueryResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_structured(
        payload.question
    )

    error_text = result.get("error")

    if (
        error_text is None
        and isinstance(result.get("data"), dict)
    ):
        error_text = result["data"].get("error")

    response = QueryResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        question=result.get(
            "question",
            payload.question,
        ),
        rewritten_question=result.get(
            "rewritten_question"
        ),
        sql=(
            result.get("sql")
            if payload.include_sql
            else None
        ),
        answer=result.get("answer"),
        insights=result.get("insights", []),
        chart=result.get("chart"),
        explanation=result.get("explanation"),
        llm=result.get("llm"),
        data=result.get("data"),
        plan=result.get("plan"),
        error=error_text,
    )

    if (
        response.status == "error"
        and not response.error
    ):
        raise HTTPException(
            status_code=500,
            detail="Query execution failed.",
        )

    return response


# =========================================================
# DASHBOARD FILTERS
# =========================================================
#
# Expected body:
#
# {
#     "search": "",
#     "state": "Maharashtra",
#     "category": "Kurta",
#     "fromPeriod": "2022-04",
#     "toPeriod": "2022-06"
# }
#
# All five dashboard endpoints receive the same filters.
# =========================================================


# ---------------------------------------------------------
# Dashboard KPIs
# ---------------------------------------------------------

@router.post(
    "/dashboard/kpis",
    response_model=DashboardResponse,
)
def dashboard_kpis(
    filters: dict[str, Any] | None = None,
) -> DashboardResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_dashboard_kpis(
        filters
    )

    kpis_payload = result.get(
        "kpis",
        [],
    )

    if isinstance(kpis_payload, dict):
        kpis_payload = kpis_payload.get(
            "kpis",
            [],
        )

    return DashboardResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        sql=result.get("sql"),
        kpis=kpis_payload,
        insights=result.get(
            "insights",
            [],
        ),
        explanation=result.get(
            "explanation"
        ),
        chart=result.get("chart"),
        llm=result.get("llm"),
        error=result.get("error"),
    )


# ---------------------------------------------------------
# Dashboard Trends
# ---------------------------------------------------------

@router.post(
    "/dashboard/trends",
    response_model=DashboardResponse,
)
def dashboard_trends(
    filters: dict[str, Any] | None = None,
) -> DashboardResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_dashboard_trends(
        filters
    )

    return DashboardResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        sql=result.get("sql"),
        revenueOrderTrend=result.get(
            "revenueOrderTrend",
            [],
        ),
        aovTrend=result.get(
            "aovTrend",
            [],
        ),
        insights=result.get(
            "insights",
            [],
        ),
        explanation=result.get(
            "explanation"
        ),
        chart=result.get("chart"),
        llm=result.get("llm"),
        error=result.get("error"),
    )


# ---------------------------------------------------------
# Dashboard Top States
# ---------------------------------------------------------

@router.post(
    "/dashboard/top-states",
    response_model=DashboardResponse,
)
def dashboard_top_states(
    filters: dict[str, Any] | None = None,
) -> DashboardResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_dashboard_top_states(
        filters
    )

    return DashboardResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        sql=result.get("sql"),
        topStates=result.get(
            "topStates",
            [],
        ),
        insights=result.get(
            "insights",
            [],
        ),
        explanation=result.get(
            "explanation"
        ),
        chart=result.get("chart"),
        llm=result.get("llm"),
        error=result.get("error"),
    )


# ---------------------------------------------------------
# Dashboard Rankings
# ---------------------------------------------------------

@router.post(
    "/dashboard/rankings",
    response_model=DashboardResponse,
)
def dashboard_rankings(
    filters: dict[str, Any] | None = None,
) -> DashboardResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_dashboard_rankings(
        filters
    )

    return DashboardResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        sql=result.get("sql"),
        topPerformers=result.get(
            "topPerformers",
            [],
        ),
        worstPerformers=result.get(
            "worstPerformers",
            [],
        ),
        insights=result.get(
            "insights",
            [],
        ),
        explanation=result.get(
            "explanation"
        ),
        chart=result.get("chart"),
        llm=result.get("llm"),
        error=result.get("error"),
    )


# ---------------------------------------------------------
# Dashboard Impact
# ---------------------------------------------------------

@router.post(
    "/dashboard/impact",
    response_model=DashboardResponse,
)
def dashboard_impact(
    filters: dict[str, Any] | None = None,
) -> DashboardResponse:

    orchestrator = get_orchestrator()

    result = orchestrator.run_dashboard_impact(
        filters
    )

    return DashboardResponse(
        status=(
            "error"
            if result.get("status") == "error"
            else "ok"
        ),
        sql=result.get("sql"),
        impactAnalysis=result.get(
            "impactAnalysis"
        ),
        insights=result.get(
            "insights",
            [],
        ),
        explanation=result.get(
            "explanation"
        ),
        chart=result.get("chart"),
        llm=result.get("llm"),
        error=result.get("error"),
    )