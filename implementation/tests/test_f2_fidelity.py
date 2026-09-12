"""
Regression tests for Finding 1: §5.8 Fidelity Checker.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f2_corpus.template_generator import (
    BankEntry,
    BundleArtifacts,
    RealizationRecord,
    check_fidelity,
    serialize_ground_truth_canonically,
    reconstruct_derived_ground_truth,
    search_bundle_bytes_for_bank_entries,
)


class TestF2FidelityChecker(unittest.TestCase):
    def setUp(self):
        self.entry_pos = BankEntry(
            entry_id="e_e1_det",
            parameter="E1",
            scope="current",
            evidence_stratum="S-DOC",
            semantic_role="determining",
            semantic_value="charge_positive",
            entry_text="Positive current indicates charging mode.",
        )
        self.entry_adj_keyed = BankEntry(
            entry_id="e_e2_adj_correct",
            parameter="E2",
            scope="voltage",
            evidence_stratum="S-DOC",
            semantic_role="non_determining_adjacent",
            semantic_value=None,
            entry_text="Voltage readings may occasionally drop near zero.",
        )
        self.entry_adj_wrong = BankEntry(
            entry_id="e_e2_adj_wrong",
            parameter="E2",
            scope="voltage",
            evidence_stratum="S-DOC",
            semantic_role="non_determining_adjacent",
            semantic_value=None,
            entry_text="A completely different adjacent voltage comment.",
        )
        self.entry_e2_det = BankEntry(
            entry_id="e_e2_det",
            parameter="E2",
            scope="voltage",
            evidence_stratum="S-DOC",
            semantic_role="determining",
            semantic_value="measured",
            entry_text="Zero voltage represents a measured physical zero.",
        )
        self.frozen_bank = [
            self.entry_pos,
            self.entry_adj_keyed,
            self.entry_adj_wrong,
            self.entry_e2_det,
        ]

        self.valid_manifest = {
            "e3_structure": {
                "num_tests": 2,
                "cycles_per_test": [2, 1],
                "steps_per_cycle": [3, 1, 1],
            },
            "interval_duration_seconds": 1.0,
        }

        self.bundle_slots = {
            "E1": {
                "scope": "current",
                "class": "POS-EXPLICIT",
                "placement": "prominent",
            },
            "E2": {
                "scope": "voltage",
                "class": "NEG-ADJACENT",
                "placement": "absent",
                "keyed_adjacent_entry_id": "e_e2_adj_correct",
            },
            "E3": {
                "scope": "energy",
                "class": "NEG-ABSENT",
                "placement": "absent",
            },
            "E4a": {
                "scope": "current",
                "class": "NEG-ABSENT",
                "placement": "absent",
            },
        }

    def test_fidelity_success_clean_bundle(self):
        """Test happy path: derived GT matches sealed GT exactly, E3 and E4 pass."""
        article_text = f"Intro.\n{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}\nOutro."
        article_bytes = article_text.encode("utf-8")
        readme_bytes = b"Readme content."
        csv_header_bytes = b"time,current,voltage\n"

        artifacts = BundleArtifacts(0, article_bytes, readme_bytes, csv_header_bytes)

        pos_start = article_text.find(self.entry_pos.entry_text)
        pos_end = pos_start + len(self.entry_pos.entry_text.encode("utf-8"))
        adj_start = article_text.find(self.entry_adj_keyed.entry_text)
        adj_end = adj_start + len(self.entry_adj_keyed.entry_text.encode("utf-8"))

        # Reconstruct canonical derived ground truth
        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived_gt = reconstruct_derived_ground_truth(discovered, self.bundle_slots)
        sealed_bytes = serialize_ground_truth_canonically(derived_gt)

        realization_index = [
            RealizationRecord(0, "e_e1_det", "E1", "current", "POS-EXPLICIT", self.entry_pos.entry_text, "article", pos_start, pos_end),
            RealizationRecord(0, "e_e2_adj_correct", "E2", "voltage", "NEG-ADJACENT", self.entry_adj_keyed.entry_text, "article", adj_start, adj_end),
        ]

        res = check_fidelity(artifacts, self.frozen_bank, sealed_bytes, self.bundle_slots, self.valid_manifest, realization_index)
        self.assertTrue(res["valid"], msg=res.get("error"))

    def test_derived_reconstruction_cannot_borrow_class_from_sealed_record(self):
        """Regression: reconstruct_derived_ground_truth does not read or take expected class from sealed record."""
        # Bundle has NO determining statement for E1, but bundle_slots claims POS-EXPLICIT
        artifacts = BundleArtifacts(0, b"Empty article", b"", b"")
        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived = reconstruct_derived_ground_truth(discovered, self.bundle_slots)

        # E1 MUST be derived as NEG-ABSENT from discovered evidence, NOT borrowed as POS-EXPLICIT!
        self.assertEqual(derived["E1"]["class"], "NEG-ABSENT")
        self.assertEqual(derived["E1"]["verdict_class"], "ABSENT")

    def test_wrong_adjacent_entry_for_same_parameter_scope_fails(self):
        """Regression: NEG-ADJACENT fails if bundle contains an adjacent entry other than the specifically keyed one."""
        # Insert entry_adj_wrong instead of entry_adj_keyed!
        article_text = f"Intro.\n{self.entry_pos.entry_text}\n{self.entry_adj_wrong.entry_text}\nOutro."
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived_gt = reconstruct_derived_ground_truth(discovered, self.bundle_slots)
        sealed_bytes = serialize_ground_truth_canonically(derived_gt)

        res = check_fidelity(artifacts, self.frozen_bank, sealed_bytes, self.bundle_slots, self.valid_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("specifically keyed adjacent entry 'e_e2_adj_correct' not found", res["error"])

    def test_neg_absent_determining_occurrence_returns_neg_absent_violation(self):
        """Regression: NEG-ABSENT determining occurrence returns observable NEG-ABSENT violation."""
        # E3 is NEG-ABSENT in bundle_slots, but bundle contains a determining statement for E2
        # Let's mark E2 as NEG-ABSENT and inject e_e2_det
        slots = dict(self.bundle_slots)
        slots["E2"] = {"scope": "voltage", "class": "NEG-ABSENT", "placement": "absent"}

        article_text = f"Intro.\n{self.entry_e2_det.entry_text}\nOutro."
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        # Even if someone crafted dummy sealed bytes, check_fidelity MUST catch the invariant first
        dummy_sealed_bytes = b"{}"
        res = check_fidelity(artifacts, self.frozen_bank, dummy_sealed_bytes, slots, self.valid_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("NEG-ABSENT violation for E2", res["error"])

    def test_neg_adjacent_determining_occurrence_returns_neg_adjacent_violation(self):
        """Regression: NEG-ADJACENT bundle carrying a determining occurrence returns NEG-ADJACENT violation."""
        # E2 is NEG-ADJACENT, but bundle contains BOTH adjacent and determining entry!
        article_text = f"{self.entry_adj_keyed.entry_text}\n{self.entry_e2_det.entry_text}"
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        dummy_sealed_bytes = b"{}"
        res = check_fidelity(artifacts, self.frozen_bank, dummy_sealed_bytes, self.bundle_slots, self.valid_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("NEG-ADJACENT violation for E2", res["error"])

    def test_derived_bytes_not_equal_sealed_bytes_fails(self):
        """Regression: derived bytes != sealed bytes fails with byte mismatch error."""
        article_text = f"Intro.\n{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}\nOutro."
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived_gt = reconstruct_derived_ground_truth(discovered, self.bundle_slots)
        correct_sealed_bytes = serialize_ground_truth_canonically(derived_gt)

        # Corrupt sealed bytes by 1 byte
        corrupted_bytes = correct_sealed_bytes.replace(b"charge_positive", b"discharge_pos")

        res = check_fidelity(artifacts, self.frozen_bank, corrupted_bytes, self.bundle_slots, self.valid_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("Derived ground truth bytes do not equal sealed ground truth bytes", res["error"])

    def test_realization_index_disagreement_fails(self):
        """Regression: realization index disagreement fails."""
        article_text = f"Intro.\n{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}\nOutro."
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived_gt = reconstruct_derived_ground_truth(discovered, self.bundle_slots)
        sealed_bytes = serialize_ground_truth_canonically(derived_gt)

        pos_start = article_text.find(self.entry_pos.entry_text)
        pos_end = pos_start + len(self.entry_pos.entry_text.encode("utf-8"))

        # Realization index with offset mismatch
        bad_index = [
            RealizationRecord(0, "e_e1_det", "E1", "current", "POS-EXPLICIT", self.entry_pos.entry_text, "article", pos_start + 10, pos_end + 10),
        ]
        res = check_fidelity(artifacts, self.frozen_bank, sealed_bytes, self.bundle_slots, self.valid_manifest, bad_index)
        self.assertFalse(res["valid"])
        self.assertIn("Realization index disagreement", res["error"])

    def test_e3_validator_invoked_and_fails(self):
        """Regression: E3 structural validator is invoked and invalid structure halts fidelity."""
        article_text = f"{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}"
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        bad_e3_manifest = {
            "e3_structure": {"num_tests": 1, "cycles_per_test": [1], "steps_per_cycle": [1]},
            "interval_duration_seconds": 1.0,
        }
        res = check_fidelity(artifacts, self.frozen_bank, b"{}", self.bundle_slots, bad_e3_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("E3 structural validation failed", res["error"])

    def test_e4_validator_invoked_and_fails(self):
        """Regression: E4 positive duration validator is invoked and non-positive duration halts fidelity."""
        article_text = f"{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}"
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")

        zero_duration_manifest = {
            "e3_structure": self.valid_manifest["e3_structure"],
            "interval_duration_seconds": 0.0,
        }
        res = check_fidelity(artifacts, self.frozen_bank, b"{}", self.bundle_slots, zero_duration_manifest)
        self.assertFalse(res["valid"])
        self.assertIn("E4 positive-duration validation failed", res["error"])


if __name__ == "__main__":
    unittest.main()
