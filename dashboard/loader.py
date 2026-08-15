# # """
# # loader.py
# # =========
# # Optional helper: loads the raw Amazon Sale Report CSV and applies the
# # cleanup/derivation rules described in schema.py (state normalization,
# # has_promotion flag, is_cancelled flag).

# # Kept separate from schema.py so that schema.py itself has zero third-party
# # dependencies (no pandas) and can be imported by any lightweight agent.
# # Only import loader.py where pandas is already a dependency (e.g. data_agent.py).
# # """

# # from typing import Optional

# # try:
# #     import pandas as pd
# # except ImportError as e:
# #     raise ImportError(
# #         "loader.py requires pandas. Install with: pip install pandas --break-system-packages"
# #     ) from e

# # from .schema import normalize_state


# # def load_dataset(csv_path: str) -> "pd.DataFrame":
# #     """
# #     Load the Amazon Sale Report CSV and apply semantic-layer-driven cleanup:
# #       - ship-state_clean: normalized state names (see schema.STATE_NORMALIZATION)
# #       - has_promotion: bool, True if promotion-ids is not null
# #       - is_cancelled: bool, True if Status == 'Cancelled'
# #     """
# #     df = pd.read_csv(csv_path, low_memory=False)

# #     if "ship-state" in df.columns:
# #         df["ship-state_clean"] = df["ship-state"].map(normalize_state)

# #     if "promotion-ids" in df.columns:
# #         df["has_promotion"] = df["promotion-ids"].notna()

# #     if "Status" in df.columns:
# #         df["is_cancelled"] = df["Status"] == "Cancelled"

# #     return df
# from pyspark.sql import SparkSession
# from schema import normalize_state, add_flags  # assuming these functions exist

# spark = SparkSession.builder.getOrCreate()

# def load_data():
#     df = spark.table("amazon_sales")

#     # Apply semantic transformations
#     df = df.withColumn("ship_state", normalize_state(df["ship_state"]))
#     df = add_flags(df)

#     return df

"""
loader.py
=========

Semantic-layer loader for the Amazon sales backend.

This module loads amazon_sales_semantic_layer.json, builds typed schema objects,
and exposes lookup helpers so agents can resolve metrics, dimensions, aliases,
status groups, and business terms from one shared instance.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Optional

from schema import (
    BUSINESS_RULES,
    DERIVED_FLAGS,
    FIELDS,
    METRICS,
    MetricSpec,
    QUERY_SCHEMA,
    RESPONSE_GUIDELINES,
    STATE_NORMALIZATION,
    STATUS_GROUPS,
    TIME_INTELLIGENCE,
    UNANSWERABLE_TOPICS,
    FieldSpec,
    get_field,
    get_metric,
    normalize_state,
    resolve_metric_synonym,
    resolve_synonym,
    status_bucket,
    validate_query_plan,
)


logger = logging.getLogger(__name__)

DEFAULT_SEMANTIC_LAYER_PATH = Path(__file__).with_name("amazon_sales_semantic_layer.json")


def _canonicalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.casefold())).strip()


@dataclass(frozen=True)
class SemanticMatch:
    kind: str
    canonical_name: str
    matched_term: str
    value: Any | None = None


class SemanticLoader:
    """Load and index the semantic layer once for the whole backend."""

    def __init__(self, semantic_layer_path: str | Path | None = None) -> None:
        self.semantic_layer_path = Path(semantic_layer_path or DEFAULT_SEMANTIC_LAYER_PATH)
        self.semantic_layer = self._load_semantic_layer()

        self.dataset = self.semantic_layer.get("dataset", {})
        self.field_entries = self.semantic_layer.get("fields", [])
        self.status_groups = self.semantic_layer.get("status_groups", STATUS_GROUPS)
        self.business_rules = self.semantic_layer.get("business_rules", {})
        self.derived_flags = self.semantic_layer.get("derived_flags", {})
        self.response_guidelines = self.semantic_layer.get("response_guidelines", {})
        self.unanswerable_topics = self.semantic_layer.get("unanswerable_topics", [])
        self.common_questions = self.semantic_layer.get("common_questions_to_query_map", [])
        self.query_schema = self.semantic_layer.get("query_schema", QUERY_SCHEMA)
        self.time_intelligence = self.semantic_layer.get("time_intelligence", TIME_INTELLIGENCE)
        self.state_normalization = dict(STATE_NORMALIZATION)

        self.field_specs: dict[str, FieldSpec] = self._build_field_specs()
        self.metric_specs: dict[str, MetricSpec] = self._build_metric_specs()

        self._field_alias_index = self._build_field_alias_index()
        self._metric_alias_index = self._build_metric_alias_index()
        self._value_alias_index = self._build_value_alias_index()
        self._status_alias_index = self._build_status_alias_index()
        self._rewrite_terms = self._build_rewrite_terms()

        self._validate_against_schema_helpers()

    def _load_semantic_layer(self) -> dict[str, Any]:
        if not self.semantic_layer_path.exists():
            raise FileNotFoundError(
                f"Semantic layer JSON not found: {self.semantic_layer_path}"
            )

        with self.semantic_layer_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        if not isinstance(payload, dict):
            raise ValueError("Semantic layer JSON must contain a top-level object.")

        return payload

    def _build_field_specs(self) -> dict[str, FieldSpec]:
        specs: dict[str, FieldSpec] = {}

        for payload in self.field_entries:
            name = payload.get("name")
            if not name:
                continue

            specs[name] = FieldSpec(
                name=name,
                dtype=payload.get("type", "string"),
                role=payload.get("role", "dimension"),
                description=payload.get("description", ""),
                synonyms=list(payload.get("synonyms", [])),
                values=payload.get("values"),
                notes=payload.get("note") or payload.get("notes") or payload.get("instruction_for_chatbot"),
            )

        return specs

    def _build_metric_specs(self) -> dict[str, MetricSpec]:
        metrics = self.semantic_layer.get("metrics", {})
        specs: dict[str, MetricSpec] = {}

        for name, payload in metrics.items():
            specs[name] = MetricSpec(
                name=name,
                label=payload.get("label", name.replace("_", " ").title()),
                description=payload.get("description", ""),
                formula=payload.get("formula", ""),
                base_fields=list(payload.get("base_fields", [])),
                table=payload.get("table", ""),
                schema=payload.get("schema", ""),
                catalog=payload.get("catalog", ""),
                default_filters=list(payload.get("default_filters", [])),
                synonyms=list(payload.get("synonyms", [])),
                unit=payload.get("unit"),
                related_business_rule=payload.get("related_business_rule"),
                notes=payload.get("notes"),
            )

        return specs

    def _build_field_alias_index(self) -> dict[str, str]:
        alias_index: dict[str, str] = {}

        for spec in self.field_specs.values():
            aliases = {spec.name, spec.name.strip(), *spec.synonyms}

            for alias in aliases:
                normalized = _canonicalize(alias)
                if normalized:
                    alias_index[normalized] = spec.name

        return alias_index

    def _build_metric_alias_index(self) -> dict[str, str]:
        alias_index: dict[str, str] = {}

        for spec in self.metric_specs.values():
            aliases = {spec.name, spec.label, *spec.synonyms}

            for alias in aliases:
                normalized = _canonicalize(alias)
                if normalized:
                    alias_index[normalized] = spec.name

        return alias_index

    def _build_value_alias_index(self) -> dict[str, tuple[str, Any]]:
        alias_index: dict[str, tuple[str, Any]] = {}

        for field_name, spec in self.field_specs.items():
            values = spec.values

            if isinstance(values, dict):
                for raw_value, display_value in values.items():
                    for candidate in (raw_value, display_value):
                        if candidate is None:
                            continue

                        normalized = _canonicalize(str(candidate))
                        if normalized:
                            alias_index[normalized] = (field_name, raw_value)

            elif isinstance(values, list):
                for candidate in values:
                    if candidate is None:
                        continue

                    normalized = _canonicalize(str(candidate))
                    if normalized:
                        alias_index[normalized] = (field_name, candidate)

        return alias_index

    def _build_status_alias_index(self) -> dict[str, list[str]]:
        alias_index: dict[str, list[str]] = {}

        for bucket, values in self.status_groups.items():
            alias_index[_canonicalize(bucket)] = list(values)

            for value in values:
                alias_index[_canonicalize(str(value))] = list(values)

        return alias_index

    def _build_rewrite_terms(self) -> list[tuple[str, str]]:
        pairs: list[tuple[str, str]] = []

        for alias, canonical in self._metric_alias_index.items():
            pairs.append((alias, canonical))

        for alias, canonical in self._field_alias_index.items():
            pairs.append((alias, canonical))

        pairs.sort(key=lambda item: len(item[0]), reverse=True)

        return pairs

    def _validate_against_schema_helpers(self) -> None:
        """Log a compact warning if the JSON payload drifts from schema.py helpers."""

        missing_metrics = [name for name in self.metric_specs if name not in METRICS]
        if missing_metrics:
            logger.debug("Semantic JSON defines metrics not present in schema.py: %s", missing_metrics)

        field_names = {
            entry.get("name")
            for entry in self.field_entries
            if isinstance(entry, dict) and entry.get("name")
        }
        missing_fields = [name for name in self.field_specs if name not in field_names]
        if missing_fields:
            logger.debug("Semantic JSON defines fields not tracked in loader index: %s", missing_fields)

    def get_field(self, name: str) -> FieldSpec | None:
        return self.field_specs.get(name) or get_field(name)

    def get_metric(self, name: str) -> MetricSpec | None:
        return self.metric_specs.get(name) or get_metric(name)

    def resolve_field(self, term: str) -> str | None:
        normalized = _canonicalize(term)
        return self._field_alias_index.get(normalized)

    def resolve_metric(self, term: str) -> str | None:
        normalized = _canonicalize(term)
        return self._metric_alias_index.get(normalized) or resolve_metric_synonym(term)

    def resolve_term(self, term: str) -> str | None:
        return self.resolve_metric(term) or self.resolve_field(term)

    def resolve_field_value(self, term: str) -> tuple[str, Any] | None:
        return self._value_alias_index.get(_canonicalize(term))

    def find_field_matches(self, text: str) -> list[str]:
        normalized_text = _canonicalize(text)
        matches: list[str] = []

        for alias, canonical in sorted(self._field_alias_index.items(), key=lambda item: len(item[0]), reverse=True):
            if re.search(rf"(?<!\\w){re.escape(alias)}(?!\\w)", normalized_text):
                matches.append(canonical)

        return list(dict.fromkeys(matches))

    def find_metric_matches(self, text: str) -> list[str]:
        normalized_text = _canonicalize(text)
        matches: list[str] = []

        for alias, canonical in sorted(self._metric_alias_index.items(), key=lambda item: len(item[0]), reverse=True):
            if re.search(rf"(?<!\\w){re.escape(alias)}(?!\\w)", normalized_text):
                matches.append(canonical)

        return list(dict.fromkeys(matches))

    def find_value_matches(self, text: str) -> list[SemanticMatch]:
        normalized_text = _canonicalize(text)
        matches: list[SemanticMatch] = []
        ranking_context = any(term in normalized_text for term in ("top", "bottom", "highest", "lowest", "most", "least"))

        for alias, (field_name, value) in sorted(self._value_alias_index.items(), key=lambda item: len(item[0]), reverse=True):
            if len(alias) <= 2:
                field_spec = self.field_specs.get(field_name)
                field_aliases = [
                    _canonicalize(field_name),
                    *(_canonicalize(s) for s in (field_spec.synonyms if field_spec else [])),
                ]

                if not any(field_alias and field_alias in normalized_text for field_alias in field_aliases):
                    continue

            if ranking_context and field_name in {"Category", "Size"} and alias.lower() in {"top", "bottom", "highest", "lowest", "most", "least"}:
                continue

            if re.search(rf"(?<!\\w){re.escape(alias)}(?!\\w)", normalized_text):
                matches.append(
                    SemanticMatch(
                        kind="field_value",
                        canonical_name=field_name,
                        matched_term=alias,
                        value=value,
                    )
                )

        return matches

    def infer_metric_from_question(self, text: str) -> str | None:
        matches = self.find_metric_matches(text)
        if matches:
            return matches[0]

        normalized_text = _canonicalize(text)

        for question in self.common_questions:
            pattern = re.escape(_canonicalize(question.get("user_asks", "")))
            pattern = pattern.replace(r"\[month\]", r".+?")
            pattern = pattern.replace(r"\[category\]", r".+?")
            pattern = pattern.replace(r"\[style\]", r".+?")
            pattern = pattern.replace(r"\[sku\]", r".+?")

            if pattern and re.search(pattern, normalized_text):
                logic = question.get("logic", "").lower()

                if "sum(qty)" in logic:
                    return "units_sold"

                if "sum(amount)" in logic:
                    return "revenue"

                if "average order value" in logic or "sum(amount) / count(distinct order id)" in logic:
                    return "average_order_value"

                if "count(distinct order id)" in logic and "cancel" in logic:
                    return "order_count"

        if any(term in normalized_text for term in ("how many orders", "order count", "number of orders")):
            return "order_count"

        if any(term in normalized_text for term in ("units sold", "quantity sold", "best-selling", "best selling", "most sold", "top performing", "performs best", "performs worst", "best performing", "worst performing")):
            return "units_sold"

        if any(term in normalized_text for term in ("average order value", "aov")):
            return "average_order_value"

        if any(term in normalized_text for term in ("revenue", "sales", "gmv", "amount")):
            return "revenue"

        return None

    def resolve_status_group(self, term: str) -> list[str] | None:
        return self._status_alias_index.get(_canonicalize(term))

    def iter_rewrite_terms(self) -> Iterable[tuple[str, str]]:
        for alias, canonical in self._rewrite_terms:
            yield alias, canonical

    def resolve_state(self, raw: str | None) -> str | None:
        return normalize_state(raw)

    def resolve_state_term(self, term: str) -> str | None:
        return self.state_normalization.get(term.strip().upper())

    def to_sql_column(self, field_name: str) -> str:
        normalized = re.sub(r"[^A-Za-z0-9]+", "_", field_name.strip()).strip("_")
        return normalized or field_name.strip()

    @property
    def field_aliases(self) -> dict[str, str]:
        return dict(self._field_alias_index)

    @property
    def metric_aliases(self) -> dict[str, str]:
        return dict(self._metric_alias_index)

    @property
    def value_aliases(self) -> dict[str, tuple[str, Any]]:
        return dict(self._value_alias_index)

    @property
    def status_aliases(self) -> dict[str, list[str]]:
        return dict(self._status_alias_index)

    def describe(self) -> dict[str, Any]:
        return {
            "dataset": self.dataset,
            "fields": list(self.field_specs),
            "metrics": list(self.metric_specs),
            "status_groups": list(self.status_groups),
            "business_rules": list(self.business_rules),
            "derived_flags": list(self.derived_flags),
            "time_intelligence": self.time_intelligence,
        }

    def validate_query_plan(self, plan: dict[str, Any]) -> list[str]:
        return validate_query_plan(plan)


@lru_cache(maxsize=1)
def get_semantic_loader(semantic_layer_path: str | Path | None = None) -> SemanticLoader:
    return SemanticLoader(semantic_layer_path)


def load_semantic_layer(semantic_layer_path: str | Path | None = None) -> dict[str, Any]:
    return get_semantic_loader(semantic_layer_path).semantic_layer


__all__ = [
    "SemanticLoader",
    "SemanticMatch",
    "get_semantic_loader",
    "load_semantic_layer",
    "DEFAULT_SEMANTIC_LAYER_PATH",
    "FIELDS",
    "METRICS",
    "STATE_NORMALIZATION",
    "STATUS_GROUPS",
    "BUSINESS_RULES",
    "DERIVED_FLAGS",
    "RESPONSE_GUIDELINES",
    "UNANSWERABLE_TOPICS",
    "QUERY_SCHEMA",
]