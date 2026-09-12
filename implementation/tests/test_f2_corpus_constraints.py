"""
CI Tests for every frozen §5.1 assertion and §5.2 coverage requirement.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f2_corpus.constants import (
    PARAMETERS,
    NUM_BUNDLES,
    NUM_PARAMETERS,
    NUM_CELLS,
    APPLICABLE_SCOPES,
)
from f2_corpus.class_assignment import verify_class_constraints
from f2_corpus.scope_solver import generate_frozen_scope_table
from f2_corpus.coverage_verifier import verify_all_assertions


class TestF2CorpusConstraints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope_table = generate_frozen_scope_table()

    def test_class_constraints_closed_form(self):
        """Test §5.1 closed form class constraints."""
        res = verify_class_constraints()
        self.assertTrue(res["valid"], msg=res.get("reason"))

    def test_all_5_1_assertions(self):
        """Test all frozen §5.1 assertions across the entire corpus design."""
        res = verify_all_assertions(self.scope_table)
        self.assertTrue(res["valid"], msg=res.get("reason"))

    def test_dimensions(self):
        """Test exact CVD dimensions."""
        self.assertEqual(len(PARAMETERS), 11)
        self.assertEqual(NUM_BUNDLES, 30)
        self.assertEqual(NUM_BUNDLES * len(PARAMETERS), 330)

    def test_heterogeneous_scopes(self):
        """Verify scope vocabulary cardinalities from §4.2."""
        expected_s = {
            "E1": 2,
            "E2": 4,
            "E3": 4,
            "E4a": 4,
            "E4b": 4,
            "E5": 4,
            "E6": 4,
            "E7a": 3,
            "E7b": 1,
            "E8a": 2,
            "E8b": 8,
        }
        for param, s in expected_s.items():
            self.assertEqual(len(APPLICABLE_SCOPES[param]), s, f"{param} scope count != {s}")


if __name__ == "__main__":
    unittest.main()
