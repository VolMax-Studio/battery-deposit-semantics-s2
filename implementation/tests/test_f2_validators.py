"""
Unit tests for F2 Bank Schemas, Incompatibility, and E3/E4 structural validators.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f2_corpus.bank_schema import validate_semantic_bank_metadata, validate_placement_metadata
from f2_corpus.structural_validators import (
    check_incompatibility,
    validate_e3_structure,
    validate_e4_positive_duration,
)


class TestF2Validators(unittest.TestCase):
    def test_semantic_bank_metadata_determining(self):
        """Test valid and invalid determining bank entries."""
        valid_entry = {
            "parameter": "E1",
            "scope": "current",
            "evidence_stratum": "S-DOC",
            "semantic_role": "determining",
            "semantic_value": "charge_positive",
            "exclusive_assertion": False,
            "entry_text": "Positive current denotes battery charging mode.",
        }
        res = validate_semantic_bank_metadata(valid_entry)
        self.assertTrue(res["valid"], msg=res.get("error"))

        # Missing semantic_value for determining entry
        invalid_entry = dict(valid_entry)
        invalid_entry["semantic_value"] = None
        res_inv = validate_semantic_bank_metadata(invalid_entry)
        self.assertFalse(res_inv["valid"])

    def test_exclusive_assertion_rule(self):
        """Exclusive assertion may be true ONLY for determining entries of set-valued parameters."""
        # Single-valued E1 with exclusive_assertion=True should fail
        entry_e1 = {
            "parameter": "E1",
            "scope": "current",
            "evidence_stratum": "S-DOC",
            "semantic_role": "determining",
            "semantic_value": "charge_positive",
            "exclusive_assertion": True,
            "entry_text": "Only positive current charges.",
        }
        res = validate_semantic_bank_metadata(entry_e1)
        self.assertFalse(res["valid"])

        # Set-valued E5 with exclusive_assertion=True should pass
        entry_e5 = {
            "parameter": "E5",
            "scope": "voltage",
            "evidence_stratum": "S-DOC",
            "semantic_role": "determining",
            "semantic_value": ["fixed"],
            "exclusive_assertion": True,
            "entry_text": "Voltage is logged exclusively at fixed 1s intervals.",
        }
        res_e5 = validate_semantic_bank_metadata(entry_e5)
        self.assertTrue(res_e5["valid"], msg=res_e5.get("error"))

    def test_incompatibility_single_valued(self):
        """Single-valued distinct values for same scope are incompatible."""
        e1 = {"semantic_role": "determining", "scope": "current", "semantic_value": "charge_positive"}
        e2 = {"semantic_role": "determining", "scope": "current", "semantic_value": "discharge_positive"}
        res = check_incompatibility("E1", "current", e1, e2)
        self.assertTrue(res["incompatible"])

        # Identical values are compatible
        res_ident = check_incompatibility("E1", "current", e1, e1)
        self.assertFalse(res_ident["incompatible"])

    def test_incompatibility_set_valued(self):
        """Set-valued parameters require BOTH exclusive=True and distinct sets to be incompatible."""
        s1 = {
            "semantic_role": "determining",
            "scope": "voltage",
            "semantic_value": ["fixed"],
            "exclusive_assertion": True,
        }
        s2 = {
            "semantic_role": "determining",
            "scope": "voltage",
            "semantic_value": ["event_driven(delta_voltage)"],
            "exclusive_assertion": True,
        }
        res = check_incompatibility("E5", "voltage", s1, s2)
        self.assertTrue(res["incompatible"])

        # Non-exclusive composition should NOT be incompatible
        s2_non_excl = dict(s2)
        s2_non_excl["exclusive_assertion"] = False
        res_comp = check_incompatibility("E5", "voltage", s1, s2_non_excl)
        self.assertFalse(res_comp["incompatible"])

    def test_e3_structural_validator(self):
        """Test E3 hierarchy validation: >=2 tests, >=2 cycles in a test, >=2 steps in a cycle."""
        valid_e3_manifest = {
            "e3_structure": {
                "num_tests": 2,
                "cycles_per_test": [2, 1],
                "steps_per_cycle": [3, 1, 1],
            }
        }
        res = validate_e3_structure(valid_e3_manifest)
        self.assertTrue(res["valid"])

        invalid_manifest = {
            "e3_structure": {
                "num_tests": 1,
                "cycles_per_test": [1],
                "steps_per_cycle": [1],
            }
        }
        self.assertFalse(validate_e3_structure(invalid_manifest)["valid"])

    def test_e4_positive_duration_validator(self):
        """Test E4 positive interval duration (> 0)."""
        valid_manifest = {"interval_duration_seconds": 1.0}
        self.assertTrue(validate_e4_positive_duration(valid_manifest)["valid"])

        zero_duration = {"interval_duration_seconds": 0.0}
        self.assertFalse(validate_e4_positive_duration(zero_duration)["valid"])


if __name__ == "__main__":
    unittest.main()
