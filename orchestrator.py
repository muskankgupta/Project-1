"""
orchestrator.py

Main controller for the Agentic BI System.
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
    def __init__(self) -> None:
        print("=" * 60)
        print("Initializing Agentic Orchestrator...")
        print("=" * 60)

        self.semantic = get_semantic_loader()
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

    def run(self, query: str):
        structured = self.run_structured(query)
        return self._format_console_output(structured)

    def run_structured(self, query: str) -> dict[str, Any]:
        rewritten_query = self.rewriter.rewrite(query)
        result = None
        answer = ""
        insights: list[str] = []
        chart = None
        explanation = None
        sql = None
        plan = None

        try:
            plan = self.parser.parse(rewritten_query)
            plan = self.validator.validate(plan)
            plan = self.time_agent.enhance(rewritten_query, plan)
            sql = self.sql_agent.generate(plan)
            result = self.data_agent.run(sql)

            answer = self._build_answer(rewritten_query, result)
            insights = self._build_insights(rewritten_query, result)
            chart = self.chart.suggest(rewritten_query, result)
            explanation = self.explainer.generate(rewritten_query, result)
        except ValueError as exc:
            # A question that can't be mapped to a metric (e.g. out of scope)
            # should return a clean, informative "error" response instead of
            # propagating an unhandled exception to the API layer.
            return {
                "status": "error",
                "question": query,
                "rewritten_question": rewritten_query,
                "plan": self._serialize_plan(plan) if plan else None,
                "sql": sql,
                "data": None,
                "answer": str(exc),
                "insights": [str(exc)],
                "chart": None,
                "explanation": None,
                "error": str(exc),
            }

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

        return {
            "status": result.get("status", "ok") if isinstance(result, dict) else "ok",
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

    def run_dashboard_kpis(self) -> dict[str, Any]:
        plan = QueryPlan(
            metrics=["revenue", "order_count", "units_sold", "average_order_value"],
            metric="revenue",
            order_by="revenue",
        )
        return self._run_manual_dashboard_query(
            section="kpis",
            question="Show dashboard KPIs for revenue, orders, units sold, and average order value.",
            plan=plan,
            postprocess=self._build_kpi_payload,
        )

    def run_dashboard_trends(self) -> dict[str, Any]:
        revenue_sql = self._build_monthly_trend_sql("SUM(Amount)", "revenue")
        order_id_column = self.semantic.to_sql_column("Order ID")
        orders_sql = self._build_monthly_trend_sql(f"COUNT(DISTINCT {order_id_column})", "orders")
        aov_sql = self._build_monthly_trend_sql(f"SUM(Amount) / COUNT(DISTINCT {order_id_column})", "aov")

        revenue_result = self.data_agent.run(revenue_sql)
        orders_result = self.data_agent.run(orders_sql)
        aov_result = self.data_agent.run(aov_sql)

        revenue_order_trend = self._combine_trends(revenue_result, orders_result)
        aov_trend = self._rows_to_series(aov_result, value_key="aov")

        answer = self.reasoning.generate("Revenue and order trends by month", revenue_result)
        insights = self.insight.generate("Revenue and order trends by month", revenue_result)
        explanation = self.explainer.generate("Revenue and order trends by month", revenue_result)
        chart = "Line Chart"
        llm_payload = self.llm.generate(
            {
                "question": "Revenue and order trends by month",
                "rewritten_question": "Revenue and order trends by month",
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": revenue_sql,
            }
        )

        return {
            "status": self._merge_status(revenue_result, orders_result, aov_result),
            "revenueOrderTrend": revenue_order_trend,
            "aovTrend": aov_trend,
            "sql": [revenue_sql, orders_sql, aov_sql],
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    def run_dashboard_top_states(self) -> dict[str, Any]:
        sql = self._build_top_states_sql(limit=5)
        result = self.data_agent.run(sql)
        payload = self._rows_to_top_states(result)
        answer = self.reasoning.generate("Top states by revenue", result)
        insights = self.insight.generate("Top states by revenue", result)
        explanation = self.explainer.generate("Top states by revenue", result)
        chart = self.chart.suggest("Top states by revenue", result)
        llm_payload = self.llm.generate(
            {
                "question": "Top states by revenue",
                "rewritten_question": "Top states by revenue",
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": sql,
            }
        )

        return {
            "status": result.get("status", "ok") if isinstance(result, dict) else "ok",
            "topStates": payload,
            "sql": sql,
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    def run_dashboard_rankings(self) -> dict[str, Any]:
        top_sql = self._build_category_rankings_sql(order="DESC", limit=3)
        worst_sql = self._build_category_rankings_sql(order="ASC", limit=3)
        top_result = self.data_agent.run(top_sql)
        worst_result = self.data_agent.run(worst_sql)

        top_payload = self._rows_to_rankings(top_result)
        worst_payload = self._rows_to_rankings(worst_result)

        insights = self.insight.generate("Best and worst performing categories", top_result)
        explanation = self.explainer.generate("Best and worst performing categories", top_result)
        chart = self.chart.suggest("Best and worst performing categories", top_result)
        llm_payload = self.llm.generate(
            {
                "question": "Best and worst performing categories",
                "rewritten_question": "Best and worst performing categories",
                "answer": self.reasoning.generate("Best and worst performing categories", top_result),
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": [top_sql, worst_sql],
            }
        )

        return {
            "status": self._merge_status(top_result, worst_result),
            "topPerformers": top_payload,
            "worstPerformers": worst_payload,
            "sql": [top_sql, worst_sql],
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    def run_dashboard_impact(self) -> dict[str, Any]:
        sql = self._build_status_impact_sql()
        result = self.data_agent.run(sql)
        payload = self._rows_to_impact_analysis(result)
        answer = self.reasoning.generate("Impact analysis by order status", result)
        insights = self.insight.generate("Impact analysis by order status", result)
        explanation = self.explainer.generate("Impact analysis by order status", result)
        chart = self.chart.suggest("Impact analysis by order status", result)
        llm_payload = self.llm.generate(
            {
                "question": "Impact analysis by order status",
                "rewritten_question": "Impact analysis by order status",
                "answer": answer,
                "insights": insights,
                "explanation": explanation,
                "chart": chart,
                "sql": sql,
            }
        )

        return {
            "status": result.get("status", "ok") if isinstance(result, dict) else "ok",
            "impactAnalysis": payload,
            "sql": sql,
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    def _run_manual_dashboard_query(
        self,
        section: str,
        question: str,
        plan: QueryPlan,
        postprocess,
    ) -> dict[str, Any]:
        sql = self.sql_agent.generate(plan)
        result = self.data_agent.run(sql)
        answer = self._build_answer(question, result)
        insights = self._build_insights(question, result)
        explanation = self.explainer.generate(question, result)
        chart = self.chart.suggest(question, result)
        llm_payload = self.llm.generate(
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
            "status": result.get("status", "ok") if isinstance(result, dict) else "ok",
            section: postprocess(result),
            "sql": sql,
            "insights": insights,
            "explanation": explanation,
            "chart": chart,
            "llm": llm_payload,
        }

    def _build_answer(self, question: str, result: Any) -> str:
        if isinstance(result, dict) and result.get("status") == "error":
            return f"Query execution failed: {result.get('error', 'Unknown error')}"
        return self.reasoning.generate(question, result)

    def _build_insights(self, question: str, result: Any) -> list[str]:
        if isinstance(result, dict) and result.get("status") == "error":
            return [f"Query execution failed: {result.get('error', 'Unknown error')}"]
        return self.insight.generate(question, result)

    def _serialize_plan(self, plan: QueryPlan) -> dict[str, Any]:
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

    def _serialize_result(self, result: Any) -> dict[str, Any] | Any:
        if isinstance(result, dict):
            serializable = dict(result)
            rows = serializable.get("rows")
            if rows is not None:
                serializable["rows"] = [list(row) for row in rows]
            return serializable

        if isinstance(result, tuple):
            columns, rows = result
            return {"columns": list(columns), "rows": [list(row) for row in rows]}

        return result

    def _build_monthly_trend_sql(self, metric_expr: str, alias: str) -> str:
        revenue_metric = self.semantic.get_metric("revenue")
        table_name = self._build_table_name(revenue_metric)
        date_column = self.semantic.to_sql_column("Date")
        return (
            "SELECT\n"
            f"    date_format({date_column}, 'yyyy-MM') AS period,\n"
            f"    {metric_expr} AS {alias}\n"
            f"FROM {table_name}\n"
            f"WHERE {revenue_metric.default_filters[0]}\n"
            f"GROUP BY date_format({date_column}, 'yyyy-MM')\n"
            "ORDER BY period"
        )

    def _build_top_states_sql(self, limit: int = 5) -> str:
        revenue_metric = self.semantic.get_metric("revenue")
        table_name = self._build_table_name(revenue_metric)
        state_case = self._build_state_case_expression()
        order_id_column = self.semantic.to_sql_column("Order ID")
        return (
            "WITH normalized AS (\n"
            f"    SELECT {state_case} AS state, Amount, {order_id_column}\n"
            f"    FROM {table_name}\n"
            f"    WHERE {revenue_metric.default_filters[0]}\n"
            ")\n"
            "SELECT\n"
            "    state,\n"
            "    SUM(Amount) AS sales,\n"
            f"    COUNT(DISTINCT {order_id_column}) AS orders,\n"
            "    ROUND(100 * SUM(Amount) / SUM(SUM(Amount)) OVER (), 1) AS share\n"
            "FROM normalized\n"
            "GROUP BY state\n"
            "ORDER BY sales DESC\n"
            f"LIMIT {limit}"
        )

    def _build_category_rankings_sql(self, order: str, limit: int = 3) -> str:
        revenue_metric = self.semantic.get_metric("revenue")
        table_name = self._build_table_name(revenue_metric)
        return (
            "SELECT\n"
            "    Category AS name,\n"
            "    Category AS category,\n"
            "    SUM(Amount) AS value,\n"
            "    0.0 AS change,\n"
            "    ROUND(100 * SUM(Amount) / SUM(SUM(Amount)) OVER (), 1) AS share\n"
            f"FROM {table_name}\n"
            f"WHERE {revenue_metric.default_filters[0]}\n"
            "GROUP BY Category\n"
            f"ORDER BY value {order}\n"
            f"LIMIT {limit}"
        )

    def _build_status_impact_sql(self) -> str:
        revenue_metric = self.semantic.get_metric("revenue")
        table_name = self._build_table_name(revenue_metric)
        status_case = self._build_status_group_case_expression()
        order_id_column = self.semantic.to_sql_column("Order ID")
        return (
            "WITH grouped AS (\n"
            f"    SELECT {status_case} AS status_group, {order_id_column}, Amount\n"
            f"    FROM {table_name}\n"
            ")\n"
            "SELECT\n"
            "    status_group,\n"
            f"    COUNT(DISTINCT {order_id_column}) AS orders,\n"
            "    SUM(Amount) AS revenue,\n"
            f"    ROUND(100 * COUNT(DISTINCT {order_id_column}) / SUM(COUNT(DISTINCT {order_id_column})) OVER (), 1) AS orderShare,\n"
            "    ROUND(100 * SUM(Amount) / SUM(SUM(Amount)) OVER (), 1) AS revenueShare\n"
            "FROM grouped\n"
            "GROUP BY status_group\n"
            "ORDER BY revenue DESC"
        )

    def _build_state_case_expression(self) -> str:
        state_column = self.semantic.to_sql_column("ship-state")
        cases = []
        for alias, canonical in sorted(self.semantic.state_normalization.items(), key=lambda item: len(item[0]), reverse=True):
            escaped_alias = alias.replace("'", "''")
            escaped_canonical = canonical.replace("'", "''")
            cases.append(
                f"WHEN upper(trim({state_column})) = upper(trim('{escaped_alias}')) THEN '{escaped_canonical}'"
            )
        return "CASE " + " ".join(cases) + f" ELSE initcap(trim({state_column})) END"

    def _build_status_group_case_expression(self) -> str:
        cases = []
        for group_name, values in self.semantic.status_groups.items():
            escaped_values = ", ".join(f"'{value.replace("'", "''")}'" for value in values)
            cases.append(f"WHEN Status IN ({escaped_values}) THEN '{group_name}'")
        return "CASE " + " ".join(cases) + " ELSE 'other' END"

    def _build_kpi_payload(self, result: Any) -> dict[str, Any]:
        if not isinstance(result, dict):
            return {"kpis": []}

        rows = result.get("rows", []) or []
        columns = result.get("columns", []) or []
        values = rows[0] if rows else []
        metrics: list[dict[str, Any]] = []

        specs = [
            ("total-revenue", "Total Revenue", "currency"),
            ("total-orders", "Total Orders", "number"),
            ("units-sold", "Units Sold", "number"),
            ("average-order-value", "Average Order Value", "currency"),
        ]

        for index, (metric_name, label, format_name) in enumerate(specs):
            value = values[index] if index < len(values) else None
            metrics.append(
                {
                    "id": metric_name.replace("_", "-"),
                    "label": label,
                    "value": value,
                    "format": format_name,
                    "delta": 0,
                    "trend": "flat",
                }
            )

        return {"kpis": metrics, "columns": columns}

    def _combine_trends(self, revenue_result: Any, orders_result: Any) -> list[dict[str, Any]]:
        revenue_rows = self._result_rows(revenue_result)
        orders_rows = self._result_rows(orders_result)
        orders_by_period = {row[0]: row[1] for row in orders_rows if len(row) >= 2}

        trend = []
        for row in revenue_rows:
            if len(row) < 2:
                continue
            period = row[0]
            revenue = row[1]
            trend.append(
                {
                    "period": period,
                    "revenue": revenue,
                    "orders": orders_by_period.get(period),
                }
            )
        return trend

    def _rows_to_series(self, result: Any, value_key: str) -> list[dict[str, Any]]:
        rows = self._result_rows(result)
        series = []
        for row in rows:
            if len(row) < 2:
                continue
            series.append({"period": row[0], value_key: row[1]})
        return series

    def _rows_to_top_states(self, result: Any) -> list[dict[str, Any]]:
        rows = self._result_rows(result)
        payload = []
        total = sum(float(row[1]) for row in rows if len(row) > 1 and row[1] is not None)
        for index, row in enumerate(rows, start=1):
            if len(row) < 4:
                continue
            payload.append(
                {
                    "id": f"state-{index}",
                    "state": row[0],
                    "sales": row[1],
                    "orders": row[2],
                    "share": row[3] if len(row) > 3 else (round(float(row[1]) / total * 100, 1) if total else 0),
                }
            )
        return payload

    def _rows_to_rankings(self, result: Any) -> list[dict[str, Any]]:
        rows = self._result_rows(result)
        payload = []
        for index, row in enumerate(rows, start=1):
            if len(row) < 5:
                continue
            payload.append(
                {
                    "id": f"ranking-{index}",
                    "name": row[0],
                    "category": row[1],
                    "value": row[2],
                    "change": float(row[3]) if row[3] is not None else 0.0,
                    "share": row[4],
                }
            )
        return payload

    def _rows_to_impact_analysis(self, result: Any) -> dict[str, Any]:
        rows = self._result_rows(result)
        statuses = []
        comparison = []
        total_orders = sum(float(row[1]) for row in rows if len(row) > 1 and row[1] is not None)
        total_revenue = sum(float(row[2]) for row in rows if len(row) > 2 and row[2] is not None)

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
            status_id = row[0]
            statuses.append(
                {
                    "id": status_id,
                    "label": status_id.replace("_", " ").title(),
                    "orders": row[1],
                    "revenue": row[2],
                    "orderShare": row[3],
                    "revenueShare": row[4],
                    "color": color_map.get(status_id, "#94a3b8"),
                }
            )

        delivered = next((item for item in statuses if item["id"] == "successfully_delivered"), None)
        cancelled = next((item for item in statuses if item["id"] == "cancelled"), None)
        if delivered:
            comparison.append({"label": "Delivered", "orders": delivered["orders"], "revenue": delivered["revenue"]})
        if cancelled:
            comparison.append({"label": "Cancelled", "orders": cancelled["orders"], "revenue": cancelled["revenue"]})

        return {"statuses": statuses, "comparison": comparison, "totals": {"orders": total_orders, "revenue": total_revenue}}

    def _result_rows(self, result: Any) -> list[tuple[Any, ...]]:
        if isinstance(result, dict):
            rows = result.get("rows", []) or []
            return [tuple(row) for row in rows]
        if isinstance(result, tuple):
            return [tuple(row) for row in result[1]]
        return []

    def _merge_status(self, *results: Any) -> str:
        for result in results:
            if isinstance(result, dict) and result.get("status") == "error":
                return "error"
        return "ok"

    def _build_table_name(self, metric: Any) -> str:
        parts = [part for part in [metric.catalog, metric.schema, metric.table] if part]
        return ".".join(parts)

    def _format_console_output(self, structured: dict[str, Any]) -> str:
        output = ["=" * 60, "ANSWER", "=" * 60, structured.get("answer", "")]

        if structured.get("insights"):
            output.append("\nBUSINESS INSIGHTS")
            output.extend(f"• {item}" for item in structured["insights"])

        if structured.get("chart"):
            output.append("\nRECOMMENDED VISUAL")
            output.append(str(structured["chart"]))

        if structured.get("explanation"):
            output.append("\nEXPLANATION")
            output.append(str(structured["explanation"]))

        llm = structured.get("llm", {})
        if isinstance(llm, dict) and llm.get("text"):
            output.append("\nLLM RESPONSE")
            output.append(str(llm["text"]))

        return "\n".join(output)


def main() -> None:
    orchestrator = Orchestrator()

    print("\nAgentic Orchestrator Ready!")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("Ask a question: ").strip()

        if query.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            break

        try:
            response = orchestrator.run(query)
            print()
            print(response)
        except Exception as exc:
            print("\nERROR")
            print(exc)


if __name__ == "__main__":
    main()
