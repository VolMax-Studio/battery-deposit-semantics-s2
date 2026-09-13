# F7 Ground Truth Seal Record

- **Instance:** `battery-deposit-semantics-s2`
- **Stage:** F7 Logical Ground-Truth Authoring and Sealing
- **Status:** SEALED & ACCEPTED
- **Target Artifact:** `corpus/f7_ground_truth/F7_SEALED_GROUND_TRUTH.json`
- **Canonical SHA-256:** `10205cce67b71f9dca90e8a052c6f5e5dc3498c993f8fc2c7a54e8a392b52965`

---

## 1. Governance & Role Roster

- **Authoring Party:** Party 2 (`GROK-CLEAN-P2-01`)
- **Adversarial Review Party:** Party 1 (`Fable / Claude`)
  - Finding Closed: Re-serialization under frozen `serialize_ground_truth_canonically()`.
  - Review Verdict: `PARTY_1_IMPLEMENTATION_CONFORMANT` / ADVERSARIAL_REVIEW PASS
- **Gate Party:** Party 7 (`GEMINI-GATE-01`)
  - Gate Reference: `construction/SCOPED_G2_REGATE_RECORD.md` (`ARTIFACT_CONFORMITY_PASS`)
- **Operator:** Ivan (VolMax Studio Lab)

---

## 2. Artifact Properties & Verification

- **Total Parameter Cells:** 330 (30 bundles × 11 parameters)
- **Cell Matrix:** 30 × 11 complete grid
- **Class Balance (Frozen Matrix):**
  - `POS-EXPLICIT`: 55 cells
  - `POS-BURIED`: 55 cells
  - `NEG-INVERTED`: 55 cells
  - `NEG-DISTRACTOR`: 55 cells
  - `NEG-CROSS`: 55 cells
  - `NEG-ABSENT`: 55 cells
- **Scope & Closed-Form Class Conformity:** 0 discrepancies with frozen scope table
- **Verdict Mapping:** 0 errors
- **Readings Canonical Ordering:** Verified across all 330 cells (including AMBIG reading sorting)
- **Support Entry IDs:** Sorted, validated cardinalities, 0 violations
- **Location Independence (IC-1):** Invariant under text relocation between prominent and buried strata
- **Serialization:** Exact byte output of frozen `serialize_ground_truth_canonically()`

---

## 3. Stage Transition

- **Prior Lifecycle State:** `f7_ground_truth_authoring_authorized`
- **New Lifecycle State:** `f7_sealed_accepted_pending_f8`
- **Authorized Next Stage:** Stage F8 Bundle Generation by Party 2 (`GROK-CLEAN-P2-01`)
