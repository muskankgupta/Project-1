"""
query_rewrite_agent.py

Normalizes natural-language queries using the shared semantic layer.
"""

from __future__ import annotations

import re
from typing import Iterable

from loader import SemanticLoader, get_semantic_loader


class QueryRewriteAgent:
    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()

    def rewrite(self, query: str) -> str:
        rewritten = query.strip().lower()

        metric_aliases = set(self.semantic.metric_aliases)

        for alias, canonical in self._ordered_metric_terms():
            if alias == canonical:
                continue

            rewritten = re.sub(rf"\b{re.escape(alias)}\b", canonical, rewritten)

        for alias, canonical in self._ordered_field_terms(metric_aliases):
            if alias == canonical:
                continue

            rewritten = re.sub(rf"\b{re.escape(alias)}\b", canonical, rewritten)

        rewritten = self._normalize_state_mentions(rewritten)
        rewritten = self._normalize_metric_phrasing(rewritten)
        rewritten = re.sub(r"\s+", " ", rewritten).strip()

        return rewritten

    def _ordered_metric_terms(self) -> Iterable[tuple[str, str]]:
        return sorted(
            self.semantic.metric_aliases.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

    def _ordered_field_terms(self, blocked_aliases: set[str]) -> Iterable[tuple[str, str]]:
        return sorted(
            (
                (alias, canonical)
                for alias, canonical in self.semantic.field_aliases.items()
                if alias not in blocked_aliases
            ),
            key=lambda item: len(item[0]),
            reverse=True,
        )

    def _normalize_state_mentions(self, query: str) -> str:
        for alias, canonical in sorted(self.semantic.state_normalization.items(), key=lambda item: len(item[0]), reverse=True):
            pattern = rf"\b{re.escape(alias.lower())}\b"
            if re.search(pattern, query):
                query = re.sub(pattern, canonical.lower(), query)

        return query

    def _normalize_metric_phrasing(self, query: str) -> str:
        if any(metric in query for metric in ("revenue", "units sold", "order count")):
            if "total" not in query and "by" not in query and not query.startswith(("top", "bottom")):
                for term in ("revenue", "units sold", "order count"):
                    if term in query:
                        query = query.replace(term, f"total {term}", 1)
                        break

        return query
