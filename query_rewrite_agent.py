"""
query_rewrite_agent.py

Normalizes natural language before parsing.
"""

import re
from semantics import STATE_NORMALIZATION


class QueryRewriteAgent:

    def __init__(self):

        self.replacements = {

            # ------------------------
            # Revenue
            # ------------------------

            "gmv": "revenue",
            "gvm": "revenue",
            "gross merchandise value": "revenue",
            "gross sales": "revenue",
            "sales": "revenue",
            "income": "revenue",
            "turnover": "revenue",
            "sale amount": "revenue",
            "order value": "revenue",
            "net revenue": "revenue",

            # ------------------------
            # Units
            # ------------------------

            "qty": "units sold",
            "quantity": "units sold",
            "quantity sold": "units sold",
            "qty sold": "units sold",
            "items sold": "units sold",

            # ------------------------
            # Orders
            # ------------------------

            "orders count": "order count",
            "number of orders": "order count",
            "how many orders": "order count",
            "cancelled order": "cancelled orders",
            "returned order": "returned orders",

            # ------------------------
            # Dimensions
            # ------------------------

            "state": "ship_state",
            "states": "ship_state",

            "city": "ship_city",
            "cities": "ship_city",

            "platform": "sales channel",
            "channel": "sales channel",

            "product type": "category",
            "product": "category"
        }

    def rewrite(self, query: str) -> str:

        q = query.lower().strip()

        # ----------------------------------------
        # Replace business synonyms
        # ----------------------------------------

        for old, new in sorted(
            self.replacements.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            q = re.sub(
                rf"\b{re.escape(old)}\b",
                new,
                q
            )

        # ----------------------------------------
        # Insert "in" before state names
        # ----------------------------------------

        for state in STATE_NORMALIZATION.keys():

            pattern = rf"\b{re.escape(state.lower())}\b"

            if (
                re.search(pattern, q)
                and f"in {state.lower()}" not in q
                and "by" not in q
            ):

                q = re.sub(
                    pattern,
                    f"in {state.lower()}",
                    q,
                    count=1
                )

        # ----------------------------------------
        # Automatically prepend TOTAL
        # ----------------------------------------

        if (
            "revenue" in q
            and "total" not in q
            and "by" not in q
            and "top" not in q
            and "bottom" not in q
        ):
            q = q.replace("revenue", "total revenue", 1)

        if (
            "units sold" in q
            and "total" not in q
            and "by" not in q
            and "top" not in q
            and "bottom" not in q
        ):
            q = q.replace("units sold", "total units sold", 1)

        if (
            "order count" in q
            and "total" not in q
            and "by" not in q
            and "top" not in q
            and "bottom" not in q
        ):
            q = q.replace("order count", "total order count", 1)

        # ----------------------------------------
        # Complete incomplete Top/Bottom queries
        # ----------------------------------------

        if (
            q.startswith("top")
            and "by" not in q
            and (
                "category" in q
                or "ship_state" in q
                or "ship_city" in q
            )
        ):
            q += " by revenue"

        if (
            q.startswith("bottom")
            and "by" not in q
            and (
                "category" in q
                or "ship_state" in q
                or "ship_city" in q
            )
        ):
            q += " by revenue"

        # Remove duplicate spaces

        q = re.sub(r"\s+", " ", q).strip()

        return q