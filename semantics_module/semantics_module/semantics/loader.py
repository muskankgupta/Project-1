"""
loader.py
=========
Optional helper: loads the raw Amazon Sale Report CSV and applies the
cleanup/derivation rules described in schema.py (state normalization,
has_promotion flag, is_cancelled flag).

Kept separate from schema.py so that schema.py itself has zero third-party
dependencies (no pandas) and can be imported by any lightweight agent.
Only import loader.py where pandas is already a dependency (e.g. data_agent.py).
"""

from typing import Optional

try:
    import pandas as pd
except ImportError as e:
    raise ImportError(
        "loader.py requires pandas. Install with: pip install pandas --break-system-packages"
    ) from e

from .schema import normalize_state


def load_dataset(csv_path: str) -> "pd.DataFrame":
    """
    Load the Amazon Sale Report CSV and apply semantic-layer-driven cleanup:
      - ship-state_clean: normalized state names (see schema.STATE_NORMALIZATION)
      - has_promotion: bool, True if promotion-ids is not null
      - is_cancelled: bool, True if Status == 'Cancelled'
    """
    df = pd.read_csv(csv_path, low_memory=False)

    if "ship-state" in df.columns:
        df["ship-state_clean"] = df["ship-state"].map(normalize_state)

    if "promotion-ids" in df.columns:
        df["has_promotion"] = df["promotion-ids"].notna()

    if "Status" in df.columns:
        df["is_cancelled"] = df["Status"] == "Cancelled"

    return df
