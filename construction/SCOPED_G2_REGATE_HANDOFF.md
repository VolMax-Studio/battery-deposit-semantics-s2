# Scoped G2 Artifact-Conformity Re-Gate Handoff

Instance: `battery-deposit-semantics-s2`  
Target Gate: Scoped G2 Artifact-Conformity Re-Gate  
Governing Specification: `construction/S2_CANDIDATE_SPEC_v0.11.md` (Freeze Commit: `97410ca512d0c87571b4f321712c4c7c564a6a82`)  
Authorizing Operator Decision: `construction/F7_F8_BOUNDARY_CORRECTION_RATIFICATION_001.md`  
Designated Gate Party: Party 7 (`GEMINI-GATE-01`)  
Status: `READY_FOR_SCOPED_G2_REGATE`  

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
| `implementation/f2_corpus/template_generator.py` | Location-independent GT schema, `support_entry_ids`, placement derivation from byte offsets (`get_placement_in_component`), and preserved 330-cell layout iteration. |
| `implementation/f2_corpus/bundle_generator.py` | [NEW] Executable CVD bundle generator implementing frozen placement across 30 bundles, natural document formatting, and realization index generation. |
| `implementation/f2_corpus/__init__.py` | Exporting bundle generator and template generator routines. |
| `implementation/tests/test_f2_fidelity.py` | Regression tests verifying IC-1, IC-2, and preserved invariants. |
| `implementation/tests/test_f2_bundle_generator.py` | [NEW] Comprehensive 30-bundle generation and 100% fidelity verification against `F5_BANK_ATTEMPT_03.jsonl`. |
| `implementation/generate_and_verify_all.py` | Master test runner and manifest builder updating `MANIFEST_F2_F3.json`. |

---

## 3. Party 7 Verification Criteria

Party 7 should verify that:
1. **Location Independence (IC-1)**:
   - Canonical ground truth cells and reading objects do NOT contain `component`, `byte_start`, `byte_end`, `placement`, or `realization_index`.
   - `readings` contains only `entry_id`, `semantic_value`, `evidence_stratum`, `exclusive_assertion`, and `verbatim_excerpt`.
   - `support_entry_ids` provides exact bank entry ID provenance (sorted): cardinality 1 for `POS-*`, 2 for `AMBIG-CONSTRUCTED`, 1 for `NEG-ADJACENT`, 1 for `NA-CONSTRUCTED`, and 0 for `NEG-ABSENT`.
   - `readings` is empty (`[]`) for `ABSENT` and `NOT_APPLICABLE`.
2. **Invertible Placement Derivation (IC-2)**:
   - In single-determining occurrences, `POS-EXPLICIT` vs `POS-BURIED` is derived mechanically from byte offsets relative to natural section headings (`## Supplementary Appendix`, `## Supplemental Archive Notes`, `# --- Extended File Annotations ---`).
   - The checker does NOT read expected placement or class metadata to decide placement class.
   - Document sections use standard prose headings without class-bearing markers (`"BURIED_SECTION"`).
3. **Executable Bundle Generator (IC-3)**:
   - `bundle_generator.py` can generate all 30 bundles from `F5_BANK_ATTEMPT_03.jsonl`.
   - Exactly 330 bank entries are placed (each used exactly once).
   - Generated bundles declare valid E3 cycle/step structure (§4.3) and positive E4 duration.
   - `check_fidelity()` passes 100% on all 30 generated bundles.
4. **Preserved Invariants**:
   - `reconstruct_derived_ground_truth()` iterates over all 11 parameter cells for every bundle, ensuring `NEG-ABSENT` cells are always emitted.
   - Zero methodology changes: all interrogatives, answer spaces, scopes, class definitions, and decision thresholds remain identical to v0.11.
   - All regression tests pass cleanly.

---

## 4. Expected Gate Output

Party 7 should return a formal verdict document:
- Record location: `construction/SCOPED_G2_REGATE_RECORD.md`
- Verdict: `ARTIFACT_CONFORMITY_PASS` (or `BLOCK` with specific findings)
- Upon `ARTIFACT_CONFORMITY_PASS`, Stage F7 is unblocked for Party 2 (`GROK-CLEAN-P2-01`) to author and seal `F7_SEALED_GROUND_TRUTH.json`.
