"""
Unit and regression tests for F3 Serialization:
- §6.6 canonical numerics
- §6.1 adjudication records with pre-emission canonicalization
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f3_protocol.canonical_serializer import (
    serialize_canonical_numeric,
    canonicalize_semantic_value,
    serialize_adjudication_record,
)
from f3_protocol.adjudication_schema import validate_adjudication_record


class TestF3Serialization(unittest.TestCase):
    def test_canonical_numeric_frozen_examples(self):
        """Test §6.6 exact canonical numeric serialization rules."""
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

    def test_finding_2_unsorted_set_becomes_sorted_in_output(self):
        """Finding 2 Regression: unsorted set/list input produces sorted list in emitted JSON."""
        raw_set_1 = ["event_driven(step_transition)", "fixed(10 s)", "completeness_counter"]
        raw_set_2 = ["fixed(10 s)", "completeness_counter", "event_driven(step_transition)"]

        rec_1 = {
            "parameter_id": "E5",
            "scope": "voltage",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [{
                "semantic_value": raw_set_1,
                "evidence_stratum": "S-DOC",
                "artifact_sha256": "0" * 64,
                "locator": "p. 2",
                "verbatim_excerpt": "Voltage interval rule.",
            }],
        }
        rec_2 = {
            "parameter_id": "E5",
            "scope": "voltage",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [{
                "semantic_value": raw_set_2,
                "evidence_stratum": "S-DOC",
                "artifact_sha256": "0" * 64,
                "locator": "p. 2",
                "verbatim_excerpt": "Voltage interval rule.",
            }],
        }

        s1 = serialize_adjudication_record(rec_1)
        s2 = serialize_adjudication_record(rec_2)

        # Both must emit byte-identical output with sorted semantic_value
        self.assertEqual(s1, s2)
        parsed = json.loads(s1)
        emitted_set = parsed["readings"][0]["semantic_value"]
        self.assertEqual(emitted_set, sorted(raw_set_1))

    def test_finding_2_numeric_payload_canonicalization_in_output(self):
        """Finding 2 Regression: 10 / 10.0 / 1e1 numeric payloads produce same canonical bytes in output."""
        rec_int = {
            "parameter_id": "E5",
            "scope": "voltage",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [{
                "semantic_value": "fixed(10 s)",
                "evidence_stratum": "S-DOC",
                "artifact_sha256": "0" * 64,
                "locator": "p. 1",
                "verbatim_excerpt": "Fixed 10 s.",
            }],
        }
        rec_float = {
            "parameter_id": "E5",
            "scope": "voltage",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [{
                "semantic_value": "fixed(10.0 s)",
                "evidence_stratum": "S-DOC",
                "artifact_sha256": "0" * 64,
                "locator": "p. 1",
                "verbatim_excerpt": "Fixed 10 s.",
            }],
        }
        rec_exp = {
            "parameter_id": "E5",
            "scope": "voltage",
            "verdict_class": "EXPLICIT_DOC",
            "readings": [{
                "semantic_value": "fixed(1e1 s)",
                "evidence_stratum": "S-DOC",
                "artifact_sha256": "0" * 64,
                "locator": "p. 1",
                "verbatim_excerpt": "Fixed 10 s.",
            }],
        }

        s_int = serialize_adjudication_record(rec_int)
        s_float = serialize_adjudication_record(rec_float)
        s_exp = serialize_adjudication_record(rec_exp)

        self.assertEqual(s_int, s_float)
        self.assertEqual(s_int, s_exp)
        parsed = json.loads(s_int)
        self.assertEqual(parsed["readings"][0]["semantic_value"], "fixed(10 s)")

    def test_finding_2_factor_and_affine_payload_byte_identity(self):
        """Regression: factor(2.0) == factor(2) and affine(2.0, 1.0) == affine(2, 1)."""
        self.assertEqual(canonicalize_semantic_value("factor(2.0)"), "factor(2)")
        self.assertEqual(canonicalize_semantic_value("factor(1e1)"), "factor(10)")
        self.assertEqual(canonicalize_semantic_value("affine(2.0, 1.0)"), "affine(2, 1)")
        self.assertEqual(canonicalize_semantic_value("affine(+2.500000, -0.123456)"), "affine(2.5, -0.123456)")

        # Arbitrary strings remain untouched
        self.assertEqual(canonicalize_semantic_value("charge_positive"), "charge_positive")
        self.assertEqual(canonicalize_semantic_value("step"), "step")

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
        """Test deterministic field ordering and readings sorting (retained)."""
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
