from dataclasses import dataclass, field
from typing import Any


@dataclass
class Filter:

    field: str
    operator: str
    value: Any


@dataclass
class QueryPlan:

    metric: str | None = None

    dimensions: list[str] = field(default_factory=list)

    filters: list[Filter] = field(default_factory=list)

    group_by: list[str] = field(default_factory=list)

    order_by: str | None = None

    order: str = "DESC"

    limit: int | None = None

    time_grain: str | None = None