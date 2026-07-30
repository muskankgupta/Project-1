"""
tests/test_semantics.py
========================
Run with: python3 -m pytest tests/  (or just: python3 tests/test_semantics.py)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantics import (
    FIELDS,
    STATUS_GROUPS,
    SEMANTIC_LAYER,
    get_field,
    resolve_synonym,
    status_bucket,
    normalize_state,
)


class TestFieldLookup(unittest.TestCase):
    def test_get_field_known_column(self):
        spec = get_field("Amount")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.dtype, "float")

    def test_get_field_unknown_column(self):
        self.assertIsNone(get_field("not_a_real_column"))

    def test_resolve_synonym_revenue_maps_to_amount(self):
        self.assertEqual(resolve_synonym("revenue"), "Amount")

    def test_resolve_synonym_case_insensitive(self):
        self.assertEqual(resolve_synonym("REVENUE"), "Amount")

    def test_resolve_synonym_unknown_term(self):
        self.assertIsNone(resolve_synonym("banana"))

    def test_resolve_synonym_exact_column_name(self):
        self.assertEqual(resolve_synonym("Qty"), "Qty")


class TestStatusBuckets(unittest.TestCase):
    def test_cancelled_bucket(self):
        self.assertEqual(status_bucket("Cancelled"), "cancelled")

    def test_returned_bucket(self):
        self.assertEqual(status_bucket("Shipped - Returned to Seller"), "returned")

    def test_unknown_status_returns_none(self):
        self.assertIsNone(status_bucket("Not A Real Status"))

    def test_every_status_value_has_a_bucket(self):
        all_bucketed = {s for members in STATUS_GROUPS.values() for s in members}
        status_field = FIELDS["Status"]
        for value in status_field.values:
            self.assertIn(value, all_bucketed, f"{value!r} is not in any STATUS_GROUPS bucket")


class TestStateNormalization(unittest.TestCase):
    def test_abbreviation(self):
        self.assertEqual(normalize_state("RJ"), "Rajasthan")

    def test_misspelling(self):
        self.assertEqual(normalize_state("RAJSHTHAN"), "Rajasthan")

    def test_whitespace_and_case(self):
        self.assertEqual(normalize_state("  bihar "), "Bihar")

    def test_none_input(self):
        self.assertIsNone(normalize_state(None))

    def test_empty_string(self):
        self.assertIsNone(normalize_state(""))

    def test_unmapped_state_still_title_cased(self):
        self.assertEqual(normalize_state("kerala"), "Kerala")


class TestSemanticLayerBundle(unittest.TestCase):
    def test_bundle_has_expected_top_level_keys(self):
        for key in ("dataset", "fields", "status_groups", "business_rules"):
            self.assertIn(key, SEMANTIC_LAYER)

    def test_bundle_fields_match_FIELDS(self):
        self.assertEqual(set(SEMANTIC_LAYER["fields"].keys()), set(FIELDS.keys()))


if __name__ == "__main__":
    unittest.main()
