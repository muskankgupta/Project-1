"""
orchestrator.py

Main controller for the MetricMind Agentic BI System.

Pipeline:
1. Query Rewrite Agent
2. Parser Agent
3. Validation Agent
4. Time Intelligence Agent
5. SQL Generation Agent
6. Data Agent
7. Reasoning Agent
8. Insight Agent
9. Chart Agent
10. Explanation Agent
11. LLM Service
"""

from __future__ import annotations

from typing import Any

from loader import get_semantic_loader
from query_rewrite_agent import QueryRewriteAgent
from parser_agent import ParserAgent, QueryPlan
from validation_agent import ValidationAgent
from time_intelligence_agent import TimeIntelligenceAgent
from sql_agent import SQLGenerationAgent
from data_agent import DataAgent
from reasoning_agent import ReasoningAgent
from insight_agent import InsightAgent
from chart_agent import ChartAgent
from explanation_agent import ExplanationAgent
from llm_service import LLMService


class Orchestrator:
    """
    Main controller for the complete agentic BI pipeline.
    """

    def __init__(self) -> None:
        print("=" * 60)
        print("Initializing Agentic Orchestrator...")
        print("=" * 60)

        # Shared semantic layer
        self.semantic = get_semantic_loader()

        # Agents
        self.rewriter = QueryRewriteAgent(self.semantic)
        self.parser = ParserAgent(self.semantic)
        self.validator = ValidationAgent(self.semantic)
        self.time_agent = TimeIntelligenceAgent()
        self.sql_agent = SQLGenerationAgent(self.semantic)
        self.data_agent = DataAgent(self.semantic)
        self.reasoning = ReasoningAgent()
        self.insight = InsightAgent()
        self.chart = ChartAgent()
        self.explainer = ExplanationAgent()
        self.llm = LLMService(self.semantic)

        print("Initialization complete.")
        print("=" * 60)

    # ============================================================
    # GENERAL QUERY PIPELINE
    # ============================================================

    def run(self, query: str) -> str:
        """
        Run a natural-language query through the complete agentic pipeline.
        """
        structured = self.run_structured(query)
        return self._format_console_output(structured)

    def run_structured(self, query: str) -> dict[str, Any]:
        """
        Run the complete agentic pipeline and return structured JSON-safe data.
        """

        query = query.strip()

        if not query:
            return {
                "status": "error",
                "question": "",
                "answer": "Please enter a question.",
                "insights": ["Please enter a question."],
                "chart": None,
                "explanation": None,
                "sql": None,
                "data": None,
                "plan": None,
                "error": "Empty query.",
            }

        # --------------------------------------------------------
        # 1. Query Rewrite
        # --------------------------------------------------------

        rewritten_query = self.rewriter.rewrite(query)

        result: Any = None
        answer = ""
        insights: list[str] = []
        chart = None
        explanation = None
        sql = None
        plan: QueryPlan | None = None

        # --------------------------------------------------------
        # 2-6. Parse -> Validate -> Time -> SQL -> Data
        # --------------------------------------------------------

        try:
            plan = self.parser.parse(rewritten_query)

            plan = self.validator.validate(plan)

            plan = self.time_agent.enhance(
                rewritten_query,
                plan,
            )

            sql = self.sql_agent.generate(plan)

            result = self.data_agent.run(sql)

            # ----------------------------------------------------
            # 7-10. Reasoning -> Insights -> Chart -> Explanation
            # ----------------------------------------------------

            answer = self._build_answer(
                rewritten_query,
                result,
            )

            insights = self._build_insights(
                rewritten_query,
                result,
            )

            chart = self.chart.suggest(
                rewritten_query,
                result,
            )

            explanation = self.explainer.generate(
                rewritten_query,
                result,
            )

        except ValueError as exc:
            error_message = str(exc)

            return {
                "status": "error",
                "question": query,
                "rewritten_question": rewritten_query,
                "plan": self._serialize_plan(plan) if plan else None,
                "sql": sql,
                "data": None,
                "answer": error_message,
                "insights": [error_message],
                "chart": None,
                "explanation": None,
                "error": error_message,
            }

        except Exception as exc:
            error_message = str(exc)

            return {
                "status": "error",
                "question": query,
                "rewritten_question": rewritten_query,
                "plan": self._serialize_plan(plan) if plan else None,
                "sql": sql,
                "data": None,
                "answer": f"Unable to process the query: {error_message}",
                "insights": [
                    f"Unable to process the query: {error_message}"
                ],
                "chart": None,
                "explanation": None,
                "error": error_message,
            }

        # --------------------------------------------------------
        # 11. LLM Service
        # --------------------------------------------------------

        try:
            llm_payload = self.llm.generate(
                {
                    "question": query,
                    "rewritten_question": rewritten_query,
                    "answer": answer,
                    "insights": insights,
                    "explanation": explanation,
                    "chart": chart,
                    "sql": sql,
                }
            )
        except Exception as exc:
            llm_payload = {
                "status": "error",
                "text": f"LLM generation failed: {exc}",
                "error": str(exc),
            }

        # --------------------------------------------------------
        # Final response
        # --------------------------------------------------------

        status = (
            result.get("status", "ok")
            if isinstance(result, dict)
            else "ok"
        )

        return {
            "status": status,
            "question": query,
            "rewritten_question": rewritten_query,
            "plan": self._serialize_plan(plan) if plan else None,
            "sql": sql,
            "data": self._serialize_result(result),
            "answer": answer,
            "insights": insights,
            "chart": chart,
            "explanation": explanation,
            "llm": llm_payload,
        }

    # ============================================================
    # DASHBOARD - KPIs
    # ============================================================

    def run_dashboard_kpis(self) -> dict[str, Any]:
        """
        Generate dashboard KPI metrics.
        """

        plan = QueryPlan(
            metrics=[
                "revenue",
                "order_count",
                "units_sold",
                "average_order_value",
            ],
            metric="revenue",
            order_by="revenue",
        )

        return self._run_manual_dashboard_query(
            section="kpis",
            question=(
                "Show dashboard KPIs for revenue, orders, "
                "units sold, and average order value."
            ),
            plan=plan,
            postprocess=self._build_kpi_payload,
        )

    # ============================================================
    # DASHBOARD - TRENDS
    # ============================================================

    def run_dashboard_trends(self) -> dict[str, Any]:
        """
        Generate monthly revenue, orders and AOV trends.
        """

        revenue_sql = self._build_monthly_trend_sql(
            "SUM(Amount)",
            "revenue",
        )

        order_id_column = self.semantic.to_sql_column(
            "Order ID"
        )

        orders_sql = self._build_monthly_trend_sql(
            f"COUNT(DISTINCT {order_id_column})",
            "orders",
        )

        aov_sql = self._build_monthly_trend_sql(
            (
                f"SUM(Amount) / "
                f"COUNT(DISTINCT {order_id_column})"
            ),
            "aov",
        )

        revenue_result = self.data_agent.run(revenue_sql)
        orders_result = self.data_agent.run(orders_sql)
        aov_result = self.data_agent.run(aov_sql)

        revenue_order_trend = self._combine_trends(
            revenue_result,
            orders_result,
        )

        aov_trend = self._rows_to_series(
            aov_result,
            value_key="aov",
        )

        question = "Revenue and order trends by month"

        answer = self._build_answer(
            question,
            revenue_result,
        )

        insights = self._build_insights(
            question,
            revenue_result,
        )

        explanation = self.explainer.generate(
            question,
            revenue_result,
        )

        chart = "Line Chart"

        llm_payload = self._safe_llm_generate(
            {
                "question": question,
                "rewritten_question": question,
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": [
                    revenue_sql,
                    orders_sql,
                    aov_sql,
                ],
            }
        )

        return {
            "status": self._merge_status(
                revenue_result,
                orders_result,
                aov_result,
            ),
            "revenueOrderTrend": revenue_order_trend,
            "aovTrend": aov_trend,
            "sql": [
                revenue_sql,
                orders_sql,
                aov_sql,
            ],
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    # ============================================================
    # DASHBOARD - TOP STATES
    # ============================================================

    def run_dashboard_top_states(self) -> dict[str, Any]:
        """
        Generate top states by revenue.
        """

        sql = self._build_top_states_sql(
            limit=5
        )

        result = self.data_agent.run(sql)

        payload = self._rows_to_top_states(
            result
        )

        question = "Top states by revenue"

        answer = self._build_answer(
            question,
            result,
        )

        insights = self._build_insights(
            question,
            result,
        )

        explanation = self.explainer.generate(
            question,
            result,
        )

        chart = self.chart.suggest(
            question,
            result,
        )

        llm_payload = self._safe_llm_generate(
            {
                "question": question,
                "rewritten_question": question,
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": sql,
            }
        )

        return {
            "status": (
                result.get("status", "ok")
                if isinstance(result, dict)
                else "ok"
            ),
            "topStates": payload,
            "sql": sql,
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    # ============================================================
    # DASHBOARD - RANKINGS
    # ============================================================

    def run_dashboard_rankings(self) -> dict[str, Any]:
        """
        Generate best and worst performing categories.
        """

        top_sql = self._build_category_rankings_sql(
            order="DESC",
            limit=3,
        )

        worst_sql = self._build_category_rankings_sql(
            order="ASC",
            limit=3,
        )

        top_result = self.data_agent.run(
            top_sql
        )

        worst_result = self.data_agent.run(
            worst_sql
        )

        top_payload = self._rows_to_rankings(
            top_result
        )

        worst_payload = self._rows_to_rankings(
            worst_result
        )

        question = (
            "Best and worst performing categories"
        )

        answer = self._build_answer(
            question,
            top_result,
        )

        insights = self._build_insights(
            question,
            top_result,
        )

        explanation = self.explainer.generate(
            question,
            top_result,
        )

        chart = self.chart.suggest(
            question,
            top_result,
        )

        llm_payload = self._safe_llm_generate(
            {
                "question": question,
                "rewritten_question": question,
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": [
                    top_sql,
                    worst_sql,
                ],
            }
        )

        return {
            "status": self._merge_status(
                top_result,
                worst_result,
            ),
            "topPerformers": top_payload,
            "worstPerformers": worst_payload,
            "sql": [
                top_sql,
                worst_sql,
            ],
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    # ============================================================
    # DASHBOARD - IMPACT ANALYSIS
    # ============================================================

    def run_dashboard_impact(self) -> dict[str, Any]:
        """
        Generate order-status impact analysis.
        """

        sql = self._build_status_impact_sql()

        result = self.data_agent.run(sql)

        payload = self._rows_to_impact_analysis(
            result
        )

        question = "Impact analysis by order status"

        answer = self._build_answer(
            question,
            result,
        )

        insights = self._build_insights(
            question,
            result,
        )

        explanation = self.explainer.generate(
            question,
            result,
        )

        chart = self.chart.suggest(
            question,
            result,
        )

        llm_payload = self._safe_llm_generate(
            {
                "question": question,
                "rewritten_question": question,
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": sql,
            }
        )

        return {
            "status": (
                result.get("status", "ok")
                if isinstance(result, dict)
                else "ok"
            ),
            "impactAnalysis": payload,
            "sql": sql,
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    # ============================================================
    # MANUAL DASHBOARD QUERY
    # ============================================================

    def _run_manual_dashboard_query(
        self,
        section: str,
        question: str,
        plan: QueryPlan,
        postprocess,
    ) -> dict[str, Any]:

        try:
            sql = self.sql_agent.generate(plan)

            result = self.data_agent.run(sql)

            answer = self._build_answer(
                question,
                result,
            )

            insights = self._build_insights(
                question,
                result,
            )

            explanation = self.explainer.generate(
                question,
                result,
            )

            chart = self.chart.suggest(
                question,
                result,
            )

            llm_payload = self._safe_llm_generate(
                {
                    "question": question,
                    "rewritten_question": question,
                    "answer": answer,
                    "insights": insights,
                    "explanation": explanation,
                    "chart": chart,
                    "sql": sql,
                }
            )

            return {
                "status": (
                    result.get("status", "ok")
                    if isinstance(result, dict)
                    else "ok"
                ),
                section: postprocess(result),
                "sql": sql,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "llm": llm_payload,
            }

        except Exception as exc:
            return {
                "status": "error",
                section: postprocess(
                    {
                        "status": "error",
                        "rows": [],
                        "columns": [],
                        "error": str(exc),
                    }
                ),
                "sql": None,
                "insights": [
                    f"Dashboard query failed: {exc}"
                ],
                "explanation": None,
                "chart": None,
                "llm": {
                    "status": "error",
                    "text": str(exc),
                },
            }

    # ============================================================
    # ANSWER / INSIGHT HELPERS
    # ============================================================

    def _build_answer(
        self,
        question: str,
        result: Any,
    ) -> str:

        if (
            isinstance(result, dict)
            and result.get("status") == "error"
        ):
            return (
                "Query execution failed: "
                f"{result.get('error', 'Unknown error')}"
            )

        return self.reasoning.generate(
            question,
            result,
        )

    def _build_insights(
        self,
        question: str,
        result: Any,
    ) -> list[str]:

        if (
            isinstance(result, dict)
            and result.get("status") == "error"
        ):
            return [
                (
                    "Query execution failed: "
                    f"{result.get('error', 'Unknown error')}"
                )
            ]

        generated = self.insight.generate(
            question,
            result,
        )

        if generated is None:
            return []

        if isinstance(generated, str):
            return [generated]

        return list(generated)

    def _safe_llm_generate(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        try:
            result = self.llm.generate(payload)

            if isinstance(result, dict):
                return result

            return {
                "status": "ok",
                "text": str(result),
            }

        except Exception as exc:
            return {
                "status": "error",
                "text": f"LLM generation failed: {exc}",
                "error": str(exc),
            }

    # ============================================================
    # SERIALIZATION
    # ============================================================

    def _serialize_plan(
        self,
        plan: QueryPlan,
    ) -> dict[str, Any]:

        return {
            "metrics": list(plan.metrics),
            "metric": plan.metric,
            "dimensions": list(plan.dimensions),
            "filters": list(plan.filters),
            "group_by": list(plan.group_by),
            "order_by": plan.order_by,
            "order": plan.order,
            "limit": plan.limit,
            "raw_query": plan.raw_query,
            "rewritten_query": plan.rewritten_query,
            "notes": list(plan.notes),
        }

    def _serialize_result(
        self,
        result: Any,
    ) -> Any:

        if isinstance(result, dict):
            serializable = dict(result)

            rows = serializable.get("rows")

            if rows is not None:
                serializable["rows"] = [
                    list(row)
                    for row in rows
                ]

            return serializable

        if isinstance(result, tuple):
            columns, rows = result

            return {
                "columns": list(columns),
                "rows": [
                    list(row)
                    for row in rows
                ],
            }

        return result

    # ============================================================
    # SQL BUILDERS
    # ============================================================

    def _build_monthly_trend_sql(
        self,
        metric_expr: str,
        alias: str,
    ) -> str:

        revenue_metric = self.semantic.get_metric(
            "revenue"
        )

        table_name = self._build_table_name(
            revenue_metric
        )

        date_column = self.semantic.to_sql_column(
            "Date"
        )

        default_filter = (
            revenue_metric.default_filters[0]
            if revenue_metric.default_filters
            else "1=1"
        )

        return (
            "SELECT\n"
            f"    date_format({date_column}, "
            "'yyyy-MM') AS period,\n"
            f"    {metric_expr} AS {alias}\n"
            f"FROM {table_name}\n"
            f"WHERE {default_filter}\n"
            f"GROUP BY date_format({date_column}, 'yyyy-MM')\n"
            "ORDER BY period"
        )

    def _build_top_states_sql(
        self,
        limit: int = 5,
    ) -> str:

        revenue_metric = self.semantic.get_metric(
            "revenue"
        )

        table_name = self._build_table_name(
            revenue_metric
        )

        state_case = (
            self._build_state_case_expression()
        )

        order_id_column = (
            self.semantic.to_sql_column("Order ID")
        )

        default_filter = (
            revenue_metric.default_filters[0]
            if revenue_metric.default_filters
            else "1=1"
        )

        return (
            "WITH normalized AS (\n"
            f"    SELECT {state_case} AS state, "
            f"Amount, {order_id_column}\n"
            f"    FROM {table_name}\n"
            f"    WHERE {default_filter}\n"
            ")\n"
            "SELECT\n"
            "    state,\n"
            "    SUM(Amount) AS sales,\n"
            f"    COUNT(DISTINCT {order_id_column}) AS orders,\n"
            "    ROUND(\n"
            "        100 * SUM(Amount) /\n"
            "        SUM(SUM(Amount)) OVER (),\n"
            "        1\n"
            "    ) AS share\n"
            "FROM normalized\n"
            "GROUP BY state\n"
            "ORDER BY sales DESC\n"
            f"LIMIT {limit}"
        )

    def _build_category_rankings_sql(
        self,
        order: str,
        limit: int = 3,
    ) -> str:

        revenue_metric = self.semantic.get_metric(
            "revenue"
        )

        table_name = self._build_table_name(
            revenue_metric
        )

        order = (
            "DESC"
            if order.upper() == "DESC"
            else "ASC"
        )

        default_filter = (
            revenue_metric.default_filters[0]
            if revenue_metric.default_filters
            else "1=1"
        )

        return (
            "SELECT\n"
            "    Category AS name,\n"
            "    Category AS category,\n"
            "    SUM(Amount) AS value,\n"
            "    0.0 AS change,\n"
            "    ROUND(\n"
            "        100 * SUM(Amount) /\n"
            "        SUM(SUM(Amount)) OVER (),\n"
            "        1\n"
            "    ) AS share\n"
            f"FROM {table_name}\n"
            f"WHERE {default_filter}\n"
            "GROUP BY Category\n"
            f"ORDER BY value {order}\n"
            f"LIMIT {limit}"
        )

    def _build_status_impact_sql(
        self,
    ) -> str:

        revenue_metric = self.semantic.get_metric(
            "revenue"
        )

        table_name = self._build_table_name(
            revenue_metric
        )

        status_case = (
            self._build_status_group_case_expression()
        )

        order_id_column = (
            self.semantic.to_sql_column("Order ID")
        )

        return (
            "WITH grouped AS (\n"
            f"    SELECT {status_case} AS status_group,\n"
            f"           {order_id_column},\n"
            "           Amount\n"
            f"    FROM {table_name}\n"
            ")\n"
            "SELECT\n"
            "    status_group,\n"
            f"    COUNT(DISTINCT {order_id_column}) AS orders,\n"
            "    SUM(Amount) AS revenue,\n"
            f"    ROUND(\n"
            f"        100 * COUNT(DISTINCT {order_id_column}) /\n"
            f"        SUM(COUNT(DISTINCT {order_id_column})) OVER (),\n"
            "        1\n"
            "    ) AS orderShare,\n"
            "    ROUND(\n"
            "        100 * SUM(Amount) /\n"
            "        SUM(SUM(Amount)) OVER (),\n"
            "        1\n"
            "    ) AS revenueShare\n"
            "FROM grouped\n"
            "GROUP BY status_group\n"
            "ORDER BY revenue DESC"
        )

    # ============================================================
    # SEMANTIC EXPRESSIONS
    # ============================================================

    def _build_state_case_expression(
        self,
    ) -> str:

        state_column = (
            self.semantic.to_sql_column(
                "ship-state"
            )
        )

        cases: list[str] = []

        for alias, canonical in sorted(
            self.semantic.state_normalization.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):

            escaped_alias = alias.replace(
                "'",
                "''",
            )

            escaped_canonical = canonical.replace(
                "'",
                "''",
            )

            cases.append(
                "WHEN "
                f"upper(trim({state_column})) = "
                f"upper(trim('{escaped_alias}')) "
                f"THEN '{escaped_canonical}'"
            )

        if not cases:
            return (
                f"initcap(trim({state_column}))"
            )

        return (
            "CASE "
            + " ".join(cases)
            + f" ELSE initcap(trim({state_column})) END"
        )

    def _build_status_group_case_expression(
        self,
    ) -> str:

        status_column = (
            self.semantic.to_sql_column(
                "Status"
            )
        )

        cases: list[str] = []

        for group_name, values in (
            self.semantic.status_groups.items()
        ):

            escaped_values = ", ".join(
                "'"
                + value.replace("'", "''")
                + "'"
                for value in values
            )

            cases.append(
                f"WHEN {status_column} IN "
                f"({escaped_values}) "
                f"THEN '{group_name}'"
            )

        if not cases:
            return "'other'"

        return (
            "CASE "
            + " ".join(cases)
            + " ELSE 'other' END"
        )

    # ============================================================
    # DASHBOARD PAYLOAD BUILDERS
    # ============================================================

    def _build_kpi_payload(
        self,
        result: Any,
    ) -> dict[str, Any]:

        if not isinstance(result, dict):
            return {
                "kpis": []
            }

        rows = result.get(
            "rows",
            [],
        ) or []

        columns = result.get(
            "columns",
            [],
        ) or []

        values = (
            rows[0]
            if rows
            else []
        )

        metrics: list[dict[str, Any]] = []

        specs = [
            (
                "total-revenue",
                "Total Revenue",
                "currency",
            ),
            (
                "total-orders",
                "Total Orders",
                "number",
            ),
            (
                "units-sold",
                "Units Sold",
                "number",
            ),
            (
                "average-order-value",
                "Average Order Value",
                "currency",
            ),
        ]

        for index, (
            metric_name,
            label,
            format_name,
        ) in enumerate(specs):

            value = (
                values[index]
                if index < len(values)
                else 0
            )

            metrics.append(
                {
                    "id": metric_name,
                    "label": label,
                    "value": (
                        float(value)
                        if isinstance(
                            value,
                            (int, float),
                        )
                        else value
                    ),
                    "format": format_name,
                    "delta": 0,
                    "trend": "flat",
                }
            )

        return {
            "kpis": metrics,
            "columns": columns,
        }

    def _combine_trends(
        self,
        revenue_result: Any,
        orders_result: Any,
    ) -> list[dict[str, Any]]:

        revenue_rows = self._result_rows(
            revenue_result
        )

        orders_rows = self._result_rows(
            orders_result
        )

        orders_by_period = {
            row[0]: row[1]
            for row in orders_rows
            if len(row) >= 2
        }

        trend: list[dict[str, Any]] = []

        for row in revenue_rows:

            if len(row) < 2:
                continue

            period = row[0]
            revenue = row[1]

            trend.append(
                {
                    "period": period,
                    "revenue": revenue,
                    "orders": orders_by_period.get(
                        period,
                        0,
                    ),
                }
            )

        return trend

    def _rows_to_series(
        self,
        result: Any,
        value_key: str,
    ) -> list[dict[str, Any]]:

        rows = self._result_rows(result)

        series: list[dict[str, Any]] = []

        for row in rows:

            if len(row) < 2:
                continue

            series.append(
                {
                    "period": row[0],
                    value_key: row[1],
                }
            )

        return series

    def _rows_to_top_states(
        self,
        result: Any,
    ) -> list[dict[str, Any]]:

        rows = self._result_rows(result)

        payload: list[dict[str, Any]] = []

        total = sum(
            float(row[1])
            for row in rows
            if len(row) > 1
            and row[1] is not None
        )

        for index, row in enumerate(
            rows,
            start=1,
        ):

            if len(row) < 4:
                continue

            payload.append(
                {
                    "id": f"state-{index}",
                    "state": row[0],
                    "sales": row[1],
                    "orders": row[2],
                    "share": (
                        row[3]
                        if row[3] is not None
                        else (
                            round(
                                float(row[1])
                                / total
                                * 100,
                                1,
                            )
                            if total
                            else 0
                        )
                    ),
                }
            )

        return payload

    def _rows_to_rankings(
        self,
        result: Any,
    ) -> list[dict[str, Any]]:

        rows = self._result_rows(result)

        payload: list[dict[str, Any]] = []

        for index, row in enumerate(
            rows,
            start=1,
        ):

            if len(row) < 5:
                continue

            payload.append(
                {
                    "id": f"ranking-{index}",
                    "name": row[0],
                    "category": row[1],
                    "value": row[2],
                    "change": (
                        float(row[3])
                        if row[3] is not None
                        else 0.0
                    ),
                    "share": row[4],
                }
            )

        return payload

    def _rows_to_impact_analysis(
        self,
        result: Any,
    ) -> dict[str, Any]:

        rows = self._result_rows(result)

        statuses: list[dict[str, Any]] = []
        comparison: list[dict[str, Any]] = []

        total_orders = sum(
            float(row[1])
            for row in rows
            if len(row) > 1
            and row[1] is not None
        )

        total_revenue = sum(
            float(row[2])
            for row in rows
            if len(row) > 2
            and row[2] is not None
        )

        color_map = {
            "cancelled": "#fb7185",
            "successfully_delivered": "#22d3ee",
            "returned": "#f59e0b",
            "pending": "#a78bfa",
            "failed_delivery": "#f97316",
            "in_transit_or_shipped_generic": "#60a5fa",
            "other": "#94a3b8",
        }

        for row in rows:

            if len(row) < 5:
                continue

            status_id = str(row[0])

            statuses.append(
                {
                    "id": status_id,
                    "label": (
                        status_id
                        .replace("_", " ")
                        .title()
                    ),
                    "orders": row[1],
                    "revenue": row[2],
                    "orderShare": row[3],
                    "revenueShare": row[4],
                    "color": color_map.get(
                        status_id,
                        "#94a3b8",
                    ),
                }
            )

        delivered = next(
            (
                item
                for item in statuses
                if item["id"]
                == "successfully_delivered"
            ),
            None,
        )

        cancelled = next(
            (
                item
                for item in statuses
                if item["id"]
                == "cancelled"
            ),
            None,
        )

        if delivered:
            comparison.append(
                {
                    "label": "Delivered",
                    "orders": delivered["orders"],
                    "revenue": delivered["revenue"],
                }
            )

        if cancelled:
            comparison.append(
                {
                    "label": "Cancelled",
                    "orders": cancelled["orders"],
                    "revenue": cancelled["revenue"],
                }
            )

        return {
            "statuses": statuses,
            "comparison": comparison,
            "totals": {
                "orders": total_orders,
                "revenue": total_revenue,
            },
        }

    # ============================================================
    # RESULT HELPERS
    # ============================================================

    def _result_rows(
        self,
        result: Any,
    ) -> list[tuple[Any, ...]]:

        if isinstance(result, dict):

            rows = result.get(
                "rows",
                [],
            ) or []

            return [
                tuple(row)
                for row in rows
            ]

        if isinstance(result, tuple):

            if len(result) < 2:
                return []

            return [
                tuple(row)
                for row in result[1]
            ]

        return []

    def _merge_status(
        self,
        *results: Any,
    ) -> str:

        for result in results:

            if (
                isinstance(result, dict)
                and result.get("status")
                == "error"
            ):
                return "error"

        return "ok"

    def _build_table_name(
        self,
        metric: Any,
    ) -> str:

        parts = [
            part
            for part in [
                getattr(metric, "catalog", None),
                getattr(metric, "schema", None),
                getattr(metric, "table", None),
            ]
            if part
        ]

        return ".".join(parts)

    # ============================================================
    # CONSOLE OUTPUT
    # ============================================================

    def _format_console_output(
        self,
        structured: dict[str, Any],
    ) -> str:

        output = [
            "=" * 60,
            "ANSWER",
            "=" * 60,
            str(
                structured.get(
                    "answer",
                    "",
                )
            ),
        ]

        if structured.get("insights"):

            output.append(
                "\nBUSINESS INSIGHTS"
            )

            output.extend(
                f"• {item}"
                for item in structured["insights"]
            )

        if structured.get("chart"):

            output.append(
                "\nRECOMMENDED VISUAL"
            )

            output.append(
                str(
                    structured["chart"]
                )
            )

        if structured.get("explanation"):

            output.append(
                "\nEXPLANATION"
            )

            output.append(
                str(
                    structured["explanation"]
                )
            )

        llm = structured.get(
            "llm",
            {},
        )

        if (
            isinstance(llm, dict)
            and llm.get("text")
        ):

            output.append(
                "\nLLM RESPONSE"
            )

            output.append(
                str(
                    llm["text"]
                )
            )

        return "\n".join(output)


# ================================================================
# CLI ENTRYPOINT
# ================================================================

def main() -> None:

    orchestrator = Orchestrator()

    print("\nAgentic Orchestrator Ready!")
    print(
        "Type 'exit' or 'quit' to stop.\n"
    )

    while True:

        try:
            query = input(
                "Ask a question: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):
            print(
                "\n\nGoodbye!"
            )
            break

        if query.lower() in (
            "exit",
            "quit",
        ):
            print(
                "\nGoodbye!"
            )
            break

        if not query:
            print(
                "\nPlease enter a question.\n"
            )
            continue

        try:

            response = orchestrator.run(
                query
            )

            print()
            print(response)
            print()

        except Exception as exc:

            print(
                "\nERROR"
            )
            print(exc)
            print()


if __name__ == "__main__":
    main()