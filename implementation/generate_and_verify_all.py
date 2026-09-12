#!/usr/bin/env python3
"""
F2/F3 Artifact Generator, Test Runner, and Provenance Manifest Builder.
Governing freeze commit: 97410ca512d0c87571b4f321712c4c7c564a6a82
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md
"""

import os
import sys
import json
import hashlib
import unittest
from datetime import datetime, timezone

# Add parent directory to path
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, base_dir)

from f2_corpus.scope_solver import generate_frozen_scope_table
from f2_corpus.coverage_verifier import verify_all_assertions


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("================================================================")
    print("BATTERY-DEPOSIT-SEMANTICS-S2: F2/F3 ARTIFACT GENERATION & AUDIT")
    print("================================================================")
    print("Governing freeze commit: 97410ca512d0c87571b4f321712c4c7c564a6a82")
    print("Governing spec: construction/S2_CANDIDATE_SPEC_v0.11.md")
    print("----------------------------------------------------------------")

    # 1. Generate frozen scope table
    print("\n[1/4] Generating frozen scope table...")
    table = generate_frozen_scope_table()
    table_path = os.path.join(base_dir, "f2_corpus", "frozen_scope_table.json")
    with open(table_path, "w", encoding="utf-8") as f:
        json.dump(table, f, indent=2)
    print(f"-> Written to {table_path}")

    # 2. Verify all assertions
    print("\n[2/4] Verifying all §5.1 assertions and §5.2 coverage contracts...")
    res = verify_all_assertions(table)
    if not res["valid"]:
        print(f"FAILED: {res.get('reason')}")
        sys.exit(1)
    print(f"-> SUCCESS: {res['reason']}")

    # 3. Run all unit tests
    print("\n[3/4] Running F2/F3 test suite...")
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(base_dir, "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    if not test_result.wasSuccessful():
        print("FAILED: Some tests failed!")
        sys.exit(1)
    print(f"-> SUCCESS: Ran {test_result.testsRun} tests, 0 failures, 0 errors.")

    # 4. Generate Provenance Manifest
    print("\n[4/4] Building MANIFEST_F2_F3.json...")
    artifact_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".py") or f.endswith(".json"):
                if f != "MANIFEST_F2_F3.json":
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, base_dir)
                    artifact_files.append((rel_p, full_p))

    artifact_files.sort()
    artifacts_manifest = {}
    for rel_p, full_p in artifact_files:
        artifacts_manifest[rel_p] = {
            "sha256": compute_sha256(full_p),
            "size_bytes": os.path.getsize(full_p),
        }

    manifest = {
        "manifest_type": "S2_F2_F3_IMPLEMENTATION_PROVENANCE",
        "status": "READY_FOR_G2_ARTIFACT_CONFORMITY_GATE",
        "governing_freeze_commit": "97410ca512d0c87571b4f321712c4c7c564a6a82",
        "governing_specification": "construction/S2_CANDIDATE_SPEC_v0.11.md",
        "generation_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "test_command": "python3 implementation/generate_and_verify_all.py",
        "test_summary": {
            "tests_run": test_result.testsRun,
            "failures": len(test_result.failures),
            "errors": len(test_result.errors),
            "verdict": "ALL_TESTS_PASS",
        },
        "assertions_verified": [
            "30 parameter-cells per parameter (330 total)",
            "six classes, exactly five each (exact balance)",
            "scope marginals differ by at most 1",
            "class x scope table: max cell - min cell <= 1",
            "every scope spans >= 2 classes where s > 1",
            "every class spans >= 2 scopes where s > 1",
            "bundle max class count <= 3",
            "every (parameter, fold) has one item from each class",
            "exactly one admissible scope per (bundle, parameter)",
            "every (parameter, scope) has >= 2 legal semantic values (SCOPE-2)",
            "E8a joint scope and unit satisfiability for 4/6, 5/5, and 6/4 cases",
            "E8a standalone determining cells: current >= 4, voltage >= 4",
            "E8a within current: A >= 2, mA >= 2",
            "E8a within voltage: V >= 2, mV >= 2",
            "K3 62-feature design and 20 formatting markers",
            "Canonical numeric serialization (§6.6)",
            "Prohibition of note_text in adjudication output (§6.1)",
        ],
        "artifacts": artifacts_manifest,
    }

    manifest_path = os.path.join(base_dir, "MANIFEST_F2_F3.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"-> Written to {manifest_path}")

    print("\n================================================================")
    print("STATE TRANSITION: READY_FOR_G2_ARTIFACT_CONFORMITY_GATE")
    print("================================================================")


if __name__ == "__main__":
    main()
