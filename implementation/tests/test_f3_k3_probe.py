"""
Unit tests for K3 Leakage Probe feature extraction and pipeline conformance.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§9.3).
"""

import sys
import os
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from f3_protocol.k3_leakage_probe import (
    extract_bundle_features,
    extract_62_features,
    run_k3_leakage_probe,
    check_marker_presence,
)
from f2_corpus.constants import PARAMETERS, NUM_BUNDLES, NUM_PARAMETERS


class TestF3K3Probe(unittest.TestCase):
    def test_feature_count_exact_62(self):
        """Verify feature extraction emits exactly 62 features."""
        article = "# Heading\nSome text with - bullet and `code` and (2021) ref [1]."
        readme = "## Section\nSome explanation.\n```\npython\n```"
        csv_header = "# Col1,Col2,Col3\n"

        bundle_feats = extract_bundle_features(article, readme, csv_header)
        self.assertEqual(len(bundle_feats), 39)

        full_feats = extract_62_features(bundle_feats, "E1", "current")
        self.assertEqual(len(full_feats), 62)

    def test_formatting_markers_presence(self):
        """Verify presence detection of formatting markers."""
        # ATX heading '#'
        self.assertEqual(check_marker_presence(1, "# Title\nText", "", ""), 1.0)
        # Table pipe '|'
        self.assertEqual(check_marker_presence(6, "Col1 | Col2", "", ""), 1.0)
        # Line initial '#' in CSV header
        self.assertEqual(check_marker_presence(20, "", "", "# Header\n"), 1.0)
        self.assertEqual(check_marker_presence(20, "", "", "Header,Col\n"), 0.0)

    def test_k3_synthetic_smoke_run(self):
        """Smoke test K3 permutation test with low permutation count for unit testing speed."""
        rng = np.random.RandomState(42)
        # Generate 330 synthetic feature vectors with 62 features
        X = rng.randn(330, 62)
        # Exact class balance: 5 of each of the 6 classes per parameter (30 per class across 330 cells)
        y = np.array([i % 6 for i in range(330)])

        # Run with N = 20 permutations as a fast smoke test
        res = run_k3_leakage_probe(X, y, n_permutations=20, seed=20260912)
        self.assertIn("A_obs", res)
        self.assertIn("p_value", res)
        self.assertIn("verdict", res)
        self.assertFalse(res["fires"])  # Uniform random features should not fire


if __name__ == "__main__":
    unittest.main()
