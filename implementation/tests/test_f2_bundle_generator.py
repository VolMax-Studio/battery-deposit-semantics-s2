"""
Regression tests for F2 Bundle Generator and Corpus Fidelity.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.1, §5.8, §11).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f2_corpus.template_generator import (
    search_bundle_bytes_for_bank_entries,
    reconstruct_derived_ground_truth,
    serialize_ground_truth_canonically,
    check_fidelity,
)
from f2_corpus.bundle_generator import (
    load_bank_from_jsonl,
    generate_single_bundle,
    generate_all_corpus_bundles,
)
from f2_corpus.class_assignment import get_class_name
from f2_corpus.constants import PARAMETERS, NUM_BUNDLES


class TestF2BundleGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.bank_path = os.path.join(base_dir, "corpus", "f5_bank", "F5_BANK_ATTEMPT_03.jsonl")
        cls.scope_path = os.path.join(base_dir, "implementation", "f2_corpus", "frozen_scope_table.json")
        cls.bank_entries = load_bank_from_jsonl(cls.bank_path)

    def test_bundle_generation_and_fidelity_all_30_bundles(self):
        """
        Verify that all 30 bundles are generated, all 330 bank entries are placed,
        and check_fidelity passes 100% on every bundle against its independently
        reconstructed location-independent ground truth.
        """
        corpus = generate_all_corpus_bundles(self.bank_path, self.scope_path)
        self.assertEqual(len(corpus), NUM_BUNDLES)

        total_realization_records = 0

        # Load scope table
        import json
        with open(self.scope_path, "r", encoding="utf-8") as f:
            scope_table = json.load(f)

        for b_idx, (artifacts, manifest, records) in enumerate(corpus):
            total_realization_records += len(records)

            # Build bundle_slots for this bundle
            bundle_slots = {}
            for p_idx, param in enumerate(PARAMETERS):
                scope = scope_table[param]["scopes"][b_idx]
                cls_name = get_class_name(b_idx, p_idx)
                bundle_slots[param] = {
                    "scope": scope,
                    "class": cls_name,
                }

            # 1. Search bundle bytes
            discovered = search_bundle_bytes_for_bank_entries(artifacts, self.bank_entries)

            # 2. Reconstruct derived ground truth
            derived_gt = reconstruct_derived_ground_truth(
                discovered=discovered,
                bundle_slots=bundle_slots,
                artifacts=artifacts,
                bundle_idx=b_idx,
            )

            # Check that all 11 parameter cells are present in derived GT
            self.assertEqual(len(derived_gt), 11, f"Bundle {b_idx} must have 11 cells")

            # Check that class matches frozen closed form
            for p_idx, param in enumerate(PARAMETERS):
                expected_class = get_class_name(b_idx, p_idx)
                actual_class = derived_gt[param]["class"]
                self.assertEqual(
                    actual_class,
                    expected_class,
                    f"Bundle {b_idx} param {param}: derived class {actual_class} != expected {expected_class}",
                )

                # Check location independence (no component, byte_start, byte_end in readings)
                for r in derived_gt[param]["readings"]:
                    self.assertNotIn("component", r)
                    self.assertNotIn("byte_start", r)
                    self.assertNotIn("byte_end", r)

            # 3. Canonical serialization
            sealed_bytes = serialize_ground_truth_canonically(derived_gt)

            # 4. Check fidelity (including realization_index cross-check)
            res = check_fidelity(
                artifacts=artifacts,
                frozen_bank=self.bank_entries,
                sealed_ground_truth_bytes=sealed_bytes,
                bundle_slots=bundle_slots,
                bundle_manifest=manifest,
                realization_index=records,
            )
            self.assertTrue(res["valid"], msg=f"Bundle {b_idx} fidelity failed: {res.get('error')}")

        # Invariant: exactly 330 bank entries realized across the corpus
        self.assertEqual(total_realization_records, 330)


if __name__ == "__main__":
    unittest.main()
