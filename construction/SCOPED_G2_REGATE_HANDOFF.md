# Scoped G2 Artifact-Conformity Re-Gate Handoff

Instance: `battery-deposit-semantics-s2`  
Target Gate: Scoped G2 Artifact-Conformity Re-Gate  
Governing Specification: `construction/S2_CANDIDATE_SPEC_v0.11.md` (Freeze Commit: `97410ca512d0c87571b4f321712c4c7c564a6a82`)  
Authorizing Operator Decision: `construction/F7_F8_BOUNDARY_CORRECTION_RATIFICATION_001.md`  
Designated Gate Party: Party 7 (`GEMINI-GATE-01`)  
Package status: `READY_FOR_SCOPED_G2_ARTIFACT_CONFORMITY_REVIEW`  
Instance status: `F7_BLOCKED_PENDING_SCOPED_G2_REGATE`  

---

## 1. Context & Scope

Stage F6 (Role-Aware Back-Translation) concluded with a formal PASS (`330/330` slots validated, cumulative $R_{\text{total}} = 53 \le 99$, `F6_BANK_INTEGRITY = ESTABLISHED`, recorded in `corpus/f6_backtranslation/F6_CLOSURE_RECORD.md`).

Prior to authorizing Stage F7 (Sealed Ground Truth authoring by Party 2), an implementation-conformance review of the F7→F8 boundary identified three defects in the previously gated F2 implementation:
1. **IC-1 (F7 Sealed-GT Location Coupling)**: `reconstruct_derived_ground_truth()` erroneously placed F8 bundle-internal offsets (`component`, `byte_start`, `byte_end`) inside the canonical ground truth record. Because F7 is frozen to occur before F8 bundle generation (§11), the canonical sealed ground truth must be strictly location-independent.
2. **IC-2 (POS Placement Class Borrowed from Metadata)**: `reconstruct_derived_ground_truth()` previously derived `POS-EXPLICIT` vs `POS-BURIED` from `slot_info.get("placement", "prominent")` rather than from the actual byte location of the bank entry occurrence in generated bundle bytes under mechanically invertible placement rules.
3. **IC-3 (Executable F2 Bundle Generator Absent)**: Frozen §11 Stage F2 mandates *"generator and validator scripts"*, but the repository previously lacked an executable bundle-generation routine implementing frozen placement across all 30 bundles.

Operator Ratification 001 authorized a scoped implementation-conformance correction strictly limited to these three items. The frozen specification v0.11 was NOT amended, no v0.12 was opened, and Stages F5 and F6 remain valid and closed.

---

## 2. Artifacts Under Review

Party 7 is requested to evaluate the following corrected/new implementation artifacts against `S2_CANDIDATE_SPEC_v0.11.md`:

| Artifact Path | Role & Remediation |
|---|---|
| `construction/F7_F8_BOUNDARY_CORRECTION_RATIFICATION_001.md` | Operator ratification defining IC-1, IC-2, IC-3 and normative constraints. |
| `implementation/f2_corpus/template_generator.py` | Location-independent GT schema, `support_entry_ids`, XOR multi-structural placement derivation (`get_placement_in_component`), canonical serializer invariance, and preserved 330-cell layout iteration. |
| `implementation/f2_corpus/bundle_generator.py` | [NEW] Executable CVD bundle generator implementing frozen placement across 30 bundles, natural document formatting, and realization index generation. |
| `implementation/f2_corpus/__init__.py` | Exporting bundle generator and template generator routines. |
| `implementation/tests/test_f2_fidelity.py` | Regression tests verifying IC-1, IC-2 (all 4 XOR quadrants), and preserved invariants. |
| `implementation/tests/test_f2_bundle_generator.py` | [NEW] Non-circular expected GT verification, downstream bank consumption check, and 100% fidelity verification across all 30 bundles. |
| `implementation/tests/test_f3_serialization.py` | Serializer invariance regression test (byte-identical canonical output across representations). |
| `implementation/generate_and_verify_all.py` | Master test runner and manifest builder updating `MANIFEST_F2_F3.json`. |

---

## 3. Party 7 Verification Criteria

Party 7 should verify that:

### 3.1 Completeness-First Gate Rule (§8.1)
Before examining content conformity, Party 7 must first establish that every required artifact in the table above is present in the submitted package. The gate record must explicitly record:
- `REQUIRED_ARTIFACT_PRESENT`
- `REQUIRED_ARTIFACT_ABSENT`
- `ARTIFACT_CONTENT_CONFORMANT`
- `ARTIFACT_CONTENT_NONCONFORMANT`

### 3.2 Downstream Bank Consumption Verification (§8)
Party 7 must verify that the new bundle generator correctly consumes `F5_BANK_ATTEMPT_03.jsonl` (without reopening F5/F6 results):
- Consumes all 330 required bank entries.
- Every entry is used exactly once (single-use invariant §5.5).
- Bank entry text is inserted verbatim and without paraphrase.
- Zero silent duplication, omission, replacement, mutation, or re-keying.

### 3.3 Location Independence (IC-1)
- Canonical ground truth cells and reading objects do NOT contain `component`, `byte_start`, `byte_end`, `placement`, or `realization_index`.
- `readings` contains only `entry_id`, `semantic_value`, `evidence_stratum`, `exclusive_assertion`, and `verbatim_excerpt`.
- `support_entry_ids` provides exact bank entry ID provenance (sorted): cardinality 1 for `POS-*`, 2 for `AMBIG-CONSTRUCTED`, 1 for `NEG-ADJACENT`, 1 for `NA-CONSTRUCTED`, and 0 for `NEG-ABSENT`.
- `readings` is empty (`[]`) for `ABSENT` and `NOT_APPLICABLE`.

### 3.4 Invertible Multi-Structural Placement Derivation (IC-2, §5)
- In single-determining occurrences, `POS-EXPLICIT` vs `POS-BURIED` is derived mechanically from document structure via the XOR rule:
  `section depth (level 2 shallow vs level 3 deep) x ordinal block position (early vs late)`.
- Neither depth nor ordinal position alone discloses the class.
- Both `POS-EXPLICIT` and `POS-BURIED` have multiple structural realizations (1-to-many mapping).
- Zero class-bearing tokens or global structural shortcuts exist for the adjudicator.
- The checker does NOT read expected placement or class metadata to decide placement class.

### 3.5 Executable Bundle Generator (IC-3)
- `bundle_generator.py` can generate all 30 bundles from `F5_BANK_ATTEMPT_03.jsonl`.
- Generated bundles declare valid E3 cycle/step structure (§4.3) and positive E4 duration.
- `check_fidelity()` passes 100% on all 30 generated bundles against pre-F8 expected logical GT (strictly non-circular).

### 3.6 Preserved Complete-Layout Invariant & Test Suite Baseline (§10)
- `reconstruct_derived_ground_truth()` iterates over all 11 parameter cells for every bundle, ensuring `NEG-ABSENT` cells are always emitted.
- The entire pre-existing test suite (inherited 31 clean G2 tests) plus all newly added tests passes with 0 failures and 0 errors.
- No previously passing test has been deleted, disabled, narrowed, or weakened.

---

## 4. Expected Gate Output

Party 7 should return a formal verdict document:
- Record location: `construction/SCOPED_G2_REGATE_RECORD.md`
- Verdict: `ARTIFACT_CONFORMITY_PASS` (or `BLOCK` with specific findings)
- Upon `ARTIFACT_CONFORMITY_PASS`, Stage F7 is unblocked for Party 2 (`GROK-CLEAN-P2-01`) to author and seal `F7_SEALED_GROUND_TRUTH.json`.
