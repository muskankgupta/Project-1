"""
examples/basic_usage.py
========================
Shows how another agent (e.g. parser_agent.py) would use the semantics
package without needing pandas at all -- just the schema/metadata.

Run with: python3 examples/basic_usage.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantics import (
    SEMANTIC_LAYER,
    resolve_synonym,
    status_bucket,
    normalize_state,
)

if __name__ == "__main__":
    # 1. A parser agent turning a user question into a column reference
    user_terms = ["revenue", "shipping speed", "state", "units sold"]
    print("Synonym resolution:")
    for term in user_terms:
        print(f"  '{term}' -> {resolve_synonym(term)}")

    # 2. Bucketing a raw status value the way a business user thinks about it
    print("\nStatus bucketing:")
    for status in ["Cancelled", "Shipped - Returned to Seller", "Pending"]:
        print(f"  '{status}' -> {status_bucket(status)}")

    # 3. Cleaning a messy state value before grouping
    print("\nState normalization:")
    for raw in ["RJ", "rajasthan", "  BIHAR  ", "Orissa"]:
        print(f"  {raw!r} -> {normalize_state(raw)}")

    # 4. Dumping the full schema into an LLM system prompt
    print("\nDataset description for LLM prompt:")
    print(" ", SEMANTIC_LAYER["dataset"]["description"])
