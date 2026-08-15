"""
time_intelligence_agent.py

Detects natural-language time expressions and
adds date filters to the QueryPlan.
"""

import re
from datetime import datetime, timedelta

from parser_agent import QueryPlan


class TimeIntelligenceAgent:

    def __init__(self):
        self.date_column = "Date"

    def enhance(self, query: str, plan: QueryPlan) -> QueryPlan:

        q = query.lower()

        today = datetime.today().date()

        # ---------------------------------
        # Today
        # ---------------------------------

        if "today" in q:

            plan.filters.append({
                "field": self.date_column,
                "operator": "=",
                "value": today.isoformat()
            })

            return plan

        # ---------------------------------
        # Yesterday
        # ---------------------------------

        if "yesterday" in q:

            d = today - timedelta(days=1)

            plan.filters.append({
                "field": self.date_column,
                "operator": "=",
                "value": d.isoformat()
            })

            return plan

        # ---------------------------------
        # Last N Days
        # ---------------------------------

        m = re.search(r"last\s+(\d+)\s+days?", q)

        if m:

            days = int(m.group(1))

            start = today - timedelta(days=days)

            plan.filters.append({
                "field": self.date_column,
                "operator": ">=",
                "value": start.isoformat()
            })

            plan.filters.append({
                "field": self.date_column,
                "operator": "<=",
                "value": today.isoformat()
            })

            return plan

        # ---------------------------------
        # This Month
        # ---------------------------------

        if "this month" in q:

            start = today.replace(day=1)

            plan.filters.append({
                "field": self.date_column,
                "operator": ">=",
                "value": start.isoformat()
            })

            return plan

        # ---------------------------------
        # Last Month
        # ---------------------------------

        if "last month" in q:

            first_this_month = today.replace(day=1)

            last_day_prev_month = first_this_month - timedelta(days=1)

            first_prev_month = last_day_prev_month.replace(day=1)

            plan.filters.append({
                "field": self.date_column,
                "operator": ">=",
                "value": first_prev_month.isoformat()
            })

            plan.filters.append({
                "field": self.date_column,
                "operator": "<=",
                "value": last_day_prev_month.isoformat()
            })

            return plan

        # ---------------------------------
        # This Year
        # ---------------------------------

        if "this year" in q:

            start = today.replace(month=1, day=1)

            plan.filters.append({
                "field": self.date_column,
                "operator": ">=",
                "value": start.isoformat()
            })

            return plan

        # ---------------------------------
        # Last Year
        # ---------------------------------

        if "last year" in q:

            start = datetime(today.year - 1, 1, 1).date()
            end = datetime(today.year - 1, 12, 31).date()

            plan.filters.append({
                "field": self.date_column,
                "operator": ">=",
                "value": start.isoformat()
            })

            plan.filters.append({
                "field": self.date_column,
                "operator": "<=",
                "value": end.isoformat()
            })

            return plan

        return plan