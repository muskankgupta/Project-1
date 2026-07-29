# semantics

The semantic layer for the Amazon Sales chatbot. This is a self-contained
Python package -- it describes what every column in the dataset means, how
to normalize messy values, and what business rules to apply (e.g. "exclude
cancelled orders from revenue"). Any other part of the pipeline
(`parser_agent.py`, `data_agent.py`, `orchestrator.py`, etc.) imports this
package rather than re-deriving that knowledge.

## Folder structure

```
semantics_module/
├── semantics/              <- the actual package: `import semantics`
│   ├── __init__.py         <- public API, re-exports everything below
│   ├── schema.py           <- field definitions, business rules, helpers (no pandas dependency)
│   └── loader.py           <- load_dataset(): reads the CSV + applies cleanup (needs pandas)
├── data/
│   └── amazon_sale_report.csv
├── examples/
│   ├── basic_usage.py      <- schema-only usage, no pandas needed
│   └── with_data.py        <- loads real data and applies business rules
├── tests/
│   └── test_semantics.py   <- unit tests, no external test framework required
└── requirements.txt
```

## Install / setup

```bash
pip install -r requirements.txt --break-system-packages
```

No install step needed for the package itself -- just make sure the
`semantics_module/` folder (or its parent) is on your `PYTHONPATH`, or copy
the `semantics/` folder directly next to your other agent files
(`data.py`, `data_agent.py`, `parser_agent.py`, `orchestrator.py`, `state.py`).

## Quick start

```python
from semantics import SEMANTIC_LAYER, resolve_synonym, normalize_state, status_bucket

resolve_synonym("revenue")          # -> "Amount"
normalize_state("RAJSHTHAN")        # -> "Rajasthan"
status_bucket("Cancelled")          # -> "cancelled"

# Give the whole schema to an LLM as context:
system_prompt = f"Here is the dataset schema:\n{SEMANTIC_LAYER}"
```

To load and clean the actual CSV:

```python
from semantics import load_dataset

df = load_dataset("data/amazon_sale_report.csv")
# df now has extra columns: ship-state_clean, has_promotion, is_cancelled
```

## Running the examples

```bash
python3 examples/basic_usage.py     # no pandas needed
python3 examples/with_data.py       # needs pandas + the CSV in data/
```

## Running the tests

```bash
python3 -m unittest discover tests
# or, if pytest is installed:
python3 -m pytest tests/
```

## What's covered

- **`FIELDS`** -- every raw CSV column: type, description, natural-language
  synonyms ("revenue" -> `Amount`), and allowed values where categorical.
- **`STATUS_GROUPS`** -- the 13 raw `Status` values bucketed into
  `cancelled` / `successfully_delivered` / `returned` / `pending` /
  `in_transit_or_shipped_generic` / `failed_delivery`, since real questions
  are usually about the bucket, not the exact string.
- **`STATE_NORMALIZATION`** / **`normalize_state()`** -- collapses messy
  `ship-state` values (abbreviations, misspellings, casing, old names like
  "Orissa") into one canonical name per state.
- **`BUSINESS_RULES`** -- named definitions for revenue, average order
  value, cancellation rate, return rate, and how to treat missing
  Amount/currency values.
- **`DERIVED_FLAGS`** -- boolean flags (`is_cancelled`, `has_promotion`,
  `is_fba`, `is_b2b`) derivable from raw columns.
- **`RESPONSE_GUIDELINES`** / **`UNANSWERABLE_TOPICS`** -- how the chatbot
  should phrase answers (state the data's date range, clarify orders vs.
  line items) and what it should say it can't answer (no cost/profit data,
  no customer ID, nothing outside Mar 31-Jun 29 2022).

## Notes for whoever wires this into the agent pipeline

- `schema.py` has **zero third-party dependencies** on purpose, so any
  lightweight agent (e.g. a pure LLM-prompting `parser_agent.py`) can import
  it without pulling in pandas.
- `loader.py` is separated out specifically because it needs pandas --
  only import it from agents that already depend on pandas (e.g.
  `data_agent.py`).
- The CSV column `Sales Channel ` has a trailing space in the real file
  header -- this is preserved intentionally in `FIELDS`, not a typo.
- This package does not call any LLM itself and has no knowledge of
  `orchestrator.py`'s control flow -- it's pure metadata + small pure-Python
  helpers, meant to be imported, not run as a service.
