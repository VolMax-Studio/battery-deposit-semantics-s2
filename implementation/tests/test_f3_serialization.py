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

    def test_canonical_logical_gt_serializer_invariance(self):
        """
        Claude Regression: serialize_ground_truth_canonically must emit byte-identical output
        for logically identical records regardless of:
        - dict key insertion order
        - set/list order of semantic values
        - equivalent numeric representations (e.g. 10 vs 10.0, factor(2) vs factor(2.0))
        """
        from f2_corpus.template_generator import serialize_ground_truth_canonically

        record_a = {
            "verdict_class": "EXPLICIT_DOC",
            "scope": "voltage",
            "bundle_idx": 0,
            "parameter": "E5",
            "class": "POS-EXPLICIT",
            "support_entry_ids": ["id_1"],
            "readings": [
                {
                    "verbatim_excerpt": "Fixed interval.",
                    "exclusive_assertion": False,
                    "evidence_stratum": "S-DOC",
                    "semantic_value": ["event_driven(delta_voltage)", "fixed(10 s)"],
                    "entry_id": "id_1",
                }
            ],
        }

        # record_b has different key insertion order, equivalent numeric representation (10.0 s),
        # reversed set/list order
        record_b = {
            "parameter": "E5",
            "class": "POS-EXPLICIT",
            "readings": [
                {
                    "entry_id": "id_1",
                    "semantic_value": ["fixed(10.0 s)", "event_driven(delta_voltage)"],
                    "evidence_stratum": "S-DOC",
                    "verbatim_excerpt": "Fixed interval.",
                    "exclusive_assertion": False,
                }
            ],
            "support_entry_ids": ["id_1"],
            "verdict_class": "EXPLICIT_DOC",
            "bundle_idx": 0,
            "scope": "voltage",
        }

        bytes_a = serialize_ground_truth_canonically(record_a)
        bytes_b = serialize_ground_truth_canonically(record_b)

        self.assertEqual(bytes_a, bytes_b, "Logical GT A and B must emit byte-identical canonical bytes!")

    def test_reading_canonicalization_total_order(self):
        """
        Regression: when two readings share identical semantic_value, canonical serialization
        must enforce a total sort order across entry_id, evidence_stratum, exclusive_assertion,
        and verbatim_excerpt so that input insertion order does not affect emitted bytes.
        """
        from f2_corpus.template_generator import serialize_ground_truth_canonically

        reading_1 = {
            "entry_id": "entry_aaa",
            "semantic_value": "charge_positive",
            "evidence_stratum": "S-DOC",
            "exclusive_assertion": False,
            "verbatim_excerpt": "Charge is positive.",
        }
        reading_2 = {
            "entry_id": "entry_zzz",
            "semantic_value": "charge_positive",
            "evidence_stratum": "S-DOC",
            "exclusive_assertion": False,
            "verbatim_excerpt": "Charge is positive.",
        }

        # Order 1: reading_1 before reading_2
        record_order_1 = {
            "parameter": "E1",
            "scope": "current",
            "class": "AMBIG-CONSTRUCTED",
            "verdict_class": "AMBIGUOUS",
            "readings": [reading_1, reading_2],
            "support_entry_ids": ["entry_aaa", "entry_zzz"],
            "bundle_idx": 0,
        }

        # Order 2: reading_2 before reading_1 (reversed)
        record_order_2 = {
            "parameter": "E1",
            "scope": "current",
            "class": "AMBIG-CONSTRUCTED",
            "verdict_class": "AMBIGUOUS",
            "readings": [reading_2, reading_1],
            "support_entry_ids": ["entry_aaa", "entry_zzz"],
            "bundle_idx": 0,
        }

        bytes_1 = serialize_ground_truth_canonically(record_order_1)
        bytes_2 = serialize_ground_truth_canonically(record_order_2)

        self.assertEqual(
            bytes_1,
            bytes_2,
            "Readings with identical semantic_value must serialize identically regardless of input order",
        )

        # Also verify in serialize_adjudication_record
        adj_rec_1 = {
            "parameter_id": "E1",
            "scope": "current",
            "verdict_class": "AMBIGUOUS",
            "readings": [
                {
                    "semantic_value": "charge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "0" * 64,
                    "locator": "line 10",
                    "verbatim_excerpt": "Charge is positive.",
                },
                {
                    "semantic_value": "charge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "0" * 64,
                    "locator": "line 20",
                    "verbatim_excerpt": "Charge is positive.",
                },
            ],
        }
        adj_rec_2 = {
            "parameter_id": "E1",
            "scope": "current",
            "verdict_class": "AMBIGUOUS",
            "readings": [
                {
                    "semantic_value": "charge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "0" * 64,
                    "locator": "line 20",
                    "verbatim_excerpt": "Charge is positive.",
                },
                {
                    "semantic_value": "charge_positive",
                    "evidence_stratum": "S-DOC",
                    "artifact_sha256": "0" * 64,
                    "locator": "line 10",
                    "verbatim_excerpt": "Charge is positive.",
                },
            ],
        }
        self.assertEqual(
            serialize_adjudication_record(adj_rec_1),
            serialize_adjudication_record(adj_rec_2),
            "Adjudication records with identical semantic_value must serialize identically regardless of input order",
        )


if __name__ == "__main__":
    unittest.main()
