"""
Unit tests for F3 Serialization: §6.6 canonical numerics and §6.1 adjudication records.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f3_protocol.canonical_serializer import (
    serialize_canonical_numeric,
    serialize_canonical_semantic_value,
    serialize_adjudication_record,
)
from f3_protocol.adjudication_schema import validate_adjudication_record


class TestF3Serialization(unittest.TestCase):
    def test_canonical_numeric_frozen_examples(self):
        """Test §6.6 exact canonical numeric serialization rules."""
        # 10, 10.0 and 1e1 must be identical byte value "10"
        self.assertEqual(serialize_canonical_numeric("10"), "10")
        self.assertEqual(serialize_canonical_numeric("10.0"), "10")
        self.assertEqual(serialize_canonical_numeric("1e1"), "10")
        self.assertEqual(serialize_canonical_numeric(10), "10")
        self.assertEqual(serialize_canonical_numeric(10.0), "10")

        # No leading plus
        self.assertEqual(serialize_canonical_numeric("+10"), "10")
        self.assertEqual(serialize_canonical_numeric("+5.2"), "5.2")

        # Single leading minus preserved
        self.assertEqual(serialize_canonical_numeric("-10"), "-10")
        self.assertEqual(serialize_canonical_numeric("-5.2"), "-5.2")

        # Non-integers to 6 significant digits, trailing zeros stripped
        self.assertEqual(serialize_canonical_numeric("1.500000"), "1.5")
        self.assertEqual(serialize_canonical_numeric("0.123456"), "0.123456")

    def test_adjudication_record_prohibitions(self):
        """Test that note_text is strictly prohibited."""
        record_with_note = {
            "parameter_id": "E1",
            "scope": "current",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [],
            "note_text": "This note should trigger an error.",
        }
        with self.assertRaises(ValueError):
            serialize_adjudication_record(record_with_note)

        val_res = validate_adjudication_record(record_with_note)
        self.assertFalse(val_res["valid"])

    def test_adjudication_record_determinism(self):
        """Test deterministic field ordering and readings sorting."""
        record = {
            "scope": "current",
            "parameter_id": "E1",
            "verdict_class": "AMBIGUOUS",
            "readings": [
                {
                    "semantic_value": "discharge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "a" * 64,
                    "locator": "line 10",
                    "verbatim_excerpt": "Discharge is positive.",
                },
                {
                    "semantic_value": "charge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "b" * 64,
                    "locator": "line 20",
                    "verbatim_excerpt": "Charge is positive.",
                },
            ],
        }
        s1 = serialize_adjudication_record(record)
        s2 = serialize_adjudication_record(record)
        self.assertEqual(s1, s2)

        # Ensure readings were sorted: charge_positive before discharge_positive
        parsed = json.loads(s1)
        self.assertEqual(parsed["readings"][0]["semantic_value"], "charge_positive")
        self.assertEqual(parsed["readings"][1]["semantic_value"], "discharge_positive")


if __name__ == "__main__":
    unittest.main()
