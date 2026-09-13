# Stage F8 Closure Record

- **Instance:** `battery-deposit-semantics-s2`
- **Stage:** F8 Bundle Generation & Independent Fidelity Verification
- **Governing Specification:** `construction/S2_CANDIDATE_SPEC_v0.11.md` (§5.8)
- **Operator:** Ivan (VolMax Studio Lab)
- **Closure Date:** 2026-09-13
- **Final Stage Disposition:** `CLOSED & RATIFIED`

---

## 1. Multi-Party Execution & Review Roster

| Party | Role | Actor | Mandate / Action | Disposition |
|---|---|---|---|---|
| **Party 2** | Bundle Generator | `GROK-CLEAN-P2-01` | Generate 30 CVD bundles & realization index | `COMPLETED` |
| **Party 4** | Fidelity Checker | `GEMINI-CLEAN-P4-01` | Independent mechanical §5.8 fidelity execution | `PASS` |
| **Party 1** | Constructor / Reviewer | `Fable / Claude` | Post-F8 adversarial implementation review | `PASS / NO DEFECT` |
| **Operator** | Governance / Ratifier | `Ivan / VolMax` | Boundary control, limitation ratification & stage closure | `RATIFIED & CLOSED` |

---

## 2. Key Verified Evidence & Hashes

- **Generated Bundles ZIP:** `ea91206950f1f422ccfda0d0800f324e2c7dac69b8d7427484e27413ad22624e`
- **Sealed F7 Logical GT:** `10205cce67b71f9dca90e8a052c6f5e5dc3498c993f8fc2c7a54e8a392b52965`
- **Party-4 Reconstructed GT:** `10205cce67b71f9dca90e8a052c6f5e5dc3498c993f8fc2c7a54e8a392b52965` (100% Byte-Identical)
- **Party-1 Reconstructed GT:** `10205cce67b71f9dca90e8a052c6f5e5dc3498c993f8fc2c7a54e8a392b52965` (100% Byte-Identical)
- **Frozen F5 Bank:** `22fa12f14cbd0fda08293fd7c7886b7793d80bf7ec9dfa9cf2330e3b26e62859`
- **F8 Repository Commit:** `84c6293904290e648067cef4eeb7f937632de40f`

---

## 3. Adversarial Review Findings (Party 1)

Party 1 performed independent verification on actual bytes and confirmed:
- Zero leakage tokens in text visible to adjudicators (`POS_*`, `NEG_*`, `AMBIG`, `GROUND_TRUTH`, `determining`, `entry_id`, `F5-E*`).
- Manifest contains no class/placement leaks (only `bundle_idx`, `e3_structure`, `interval_duration_seconds`).
- Realization index is cleanly segregated from bundles.
- Finding: **No constructor or execution defect invalidating F8 closure.**

---

## 4. Ratified Limitation & F11 Reporting Obligation

### F8-LIMITATION-PLACEMENT-STRATUM-001

Post-F8 adversarial review identified a non-blocking realized-corpus confound between evidence stratum, component, and POS placement class.

Observed on the frozen realized corpus:

* all determining `S-DOC` POS evidence occurs in the article component;
* all determining `S-FILE` POS evidence occurs in the CSV-header component;
* among POS cells, article/component membership is therefore associated with `POS-EXPLICIT` versus `POS-BURIED`, with approximately 73% class predictability from component alone.

This does not invalidate F8 fidelity. The generated bundles remain byte-faithful to the sealed F7 ground truth and satisfy the frozen placement construction requirements.

The observation is retained as an interpretation limitation because POS placement class is not independent of evidence stratum/component in the realized corpus.

The frozen K3 probe is not modified. Its feature set does not include the determining occurrence's per-cell component/location or evidence stratum directly. Therefore a non-firing K3 result must not be interpreted as ruling out this occurrence-level placement–stratum confound. K3 remains interpreted only according to its frozen claim: no leakage detectable by the frozen K3 probe.

**F11 reporting obligation:**

Any comparison involving `POS-EXPLICIT` versus `POS-BURIED` must state that the observed difference may combine retrieval/placement difficulty with evidence-stratum/component effects. `POS-BURIED` performance must not be interpreted as a pure estimate of retrieval difficulty.

Where descriptive diagnostics are reported, results may additionally be cross-tabulated by evidence stratum/component, provided such analyses are clearly marked as non-gating descriptive diagnostics and do not modify the frozen decision function.

**Status:** NON-BLOCKING LIMITATION. Carry forward to F11.

---

## 5. Stage Transition

- **Prior State:** `f8_fidelity_pass_pending_post_f8_review`
- **New State:** `f9_k3_probe_authorized`
- **Authorized Next Action:** Execution of Stage F9 K3 Leakage Probe (`implementation/f3_protocol/k3_leakage_probe.py`) in its frozen form without modification.
