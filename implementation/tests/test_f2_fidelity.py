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

    def test_pos_class_derived_from_actual_placement_not_metadata(self):
        """Regression IC-2: POS-EXPLICIT vs POS-BURIED is derived strictly from actual byte position, not metadata."""
        # 1. Prominent placement: before ## Supplementary Appendix
        prominent_text = f"Intro.\n## Overview and Experimental Specification\n{self.entry_pos.entry_text}\n## Supplementary Appendix\nOutro."
        artifacts_prominent = BundleArtifacts(0, prominent_text.encode("utf-8"), b"", b"")
        discovered_p = search_bundle_bytes_for_bank_entries(artifacts_prominent, self.frozen_bank)

        # Even if slot metadata claimed 'buried', actual bytes are prominent -> MUST derive POS-EXPLICIT!
        slots_claiming_buried = dict(self.bundle_slots)
        slots_claiming_buried["E1"] = {"scope": "current", "class": "POS-BURIED", "placement": "buried"}
        derived_p = reconstruct_derived_ground_truth(discovered_p, slots_claiming_buried, artifacts_prominent)
        self.assertEqual(derived_p["E1"]["class"], "POS-EXPLICIT")

        # 2. Buried placement: at or after ## Supplementary Appendix
        buried_text = f"Intro.\n## Overview and Experimental Specification\nMain text.\n## Supplementary Appendix\n{self.entry_pos.entry_text}\nOutro."
        artifacts_buried = BundleArtifacts(0, buried_text.encode("utf-8"), b"", b"")
        discovered_b = search_bundle_bytes_for_bank_entries(artifacts_buried, self.frozen_bank)

        # Even if slot metadata claimed 'prominent', actual bytes are buried -> MUST derive POS-BURIED!
        slots_claiming_prominent = dict(self.bundle_slots)
        slots_claiming_prominent["E1"] = {"scope": "current", "class": "POS-EXPLICIT", "placement": "prominent"}
        derived_b = reconstruct_derived_ground_truth(discovered_b, slots_claiming_prominent, artifacts_buried)
        self.assertEqual(derived_b["E1"]["class"], "POS-BURIED")

    def test_location_independence_and_support_entry_ids(self):
        """Regression IC-1: Ground truth record is strictly location-independent and carries support_entry_ids."""
        article_text = f"Intro.\n{self.entry_pos.entry_text}\n{self.entry_adj_keyed.entry_text}\nOutro."
        artifacts = BundleArtifacts(0, article_text.encode("utf-8"), b"", b"")
        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived = reconstruct_derived_ground_truth(discovered, self.bundle_slots, artifacts)

        # Check POS-EXPLICIT cell
        e1_cell = derived["E1"]
        self.assertEqual(e1_cell["class"], "POS-EXPLICIT")
        self.assertEqual(e1_cell["support_entry_ids"], ["e_e1_det"])
        self.assertEqual(len(e1_cell["readings"]), 1)
        r = e1_cell["readings"][0]
        self.assertNotIn("component", r)
        self.assertNotIn("byte_start", r)
        self.assertNotIn("byte_end", r)
        self.assertEqual(r["entry_id"], "e_e1_det")
        self.assertEqual(r["verbatim_excerpt"], self.entry_pos.entry_text)

        # Check NEG-ADJACENT cell
        e2_cell = derived["E2"]
        self.assertEqual(e2_cell["class"], "NEG-ADJACENT")
        self.assertEqual(e2_cell["support_entry_ids"], ["e_e2_adj_correct"])
        self.assertEqual(e2_cell["readings"], [])

        # Check NEG-ABSENT cell (E3)
        e3_cell = derived["E3"]
        self.assertEqual(e3_cell["class"], "NEG-ABSENT")
        self.assertEqual(e3_cell["support_entry_ids"], [])
        self.assertEqual(e3_cell["readings"], [])

    def test_all_cells_emitted_including_neg_absent(self):
        """Regression Preserved Invariant: all cells in layout are emitted, even zero-occurrence cells."""
        artifacts = BundleArtifacts(0, b"No bank entries here at all.", b"", b"")
        discovered = search_bundle_bytes_for_bank_entries(artifacts, self.frozen_bank)
        derived = reconstruct_derived_ground_truth(discovered, self.bundle_slots, artifacts)

        # All 4 parameters in bundle_slots must be emitted as NEG-ABSENT
        self.assertEqual(len(derived), len(self.bundle_slots))
        for p in self.bundle_slots:
            self.assertIn(p, derived)
            self.assertEqual(derived[p]["class"], "NEG-ABSENT")
            self.assertEqual(derived[p]["verdict_class"], "ABSENT")
            self.assertEqual(derived[p]["readings"], [])
            self.assertEqual(derived[p]["support_entry_ids"], [])


if __name__ == "__main__":
    unittest.main()

