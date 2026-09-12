---
project: battery-deposit-semantics-s2
phase: internal_qualification_pending_gate
instance_type: INTERNAL_QUALIFICATION
publication_status: public_qualification_artifact_permitted_no_novelty_claim
predecessor: VolMax-Studio/battery-deposit-semantics-s1
predecessor_terminal_state: INSTRUMENT_INVALID
predecessor_terminal_commit: "8812111d77e3526ec07a6d613fa4e82594496b9d"

# Governance & Provenance
project_owner: Ivan / VolMax Studio Lab
operator: Ivan
final_ratifier: Ivan

construction_status: candidate_v0.4_self_contained_pending_gating
current_methodology_drafter: Claude/Fable
drafter_conflict_disclosed: true
corpus_reference_label_party: pending_fresh_unconflicted_party (strictly not Sol, K5)
fidelity_checker_party: pending_unconflicted_party (distinct from corpus party)

# Scope & Methodology Boundaries
authorized_successor_scope: instrument_validation_only
confirmatory_claims_authorized: false
prospective_target_inspection: prohibited
dual_adjudication_budget_authorized: true

independent_gate: pending_external_unconflicted_party
prereg_frozen: false
execution_authorized: false
verdict: null
---

## Current State

S2 is formally categorized as an **`INTERNAL_QUALIFICATION`** instance (instrument qualification only; prerequisite for potential S3 confirmatory work). 

### Phase 0 Prior-Art Elimination v0.2 Registered
- Artifacts:
  - `construction/PRIOR_ART_ELIMINATION_v0.1.md` (historical baseline)
  - `construction/PRIOR_ART_ELIMINATION_v0.2.md` (active v0.2)
- **Status:**
  - `RESEARCH_QUESTION: NOT_SHOWN_TO_BE_ALREADY_ANSWERED`
  - `PRIOR_ART_ELIMINATION: INCOMPLETE`
  - `METHOD_STATUS: CORE_COMPONENTS_ANTICIPATED (no novelty claim)`
  - `OPEN_PRIOR_ART_ITEM: BatteryLake public curation / processing manifests pending L3 ratification`

### Candidate Specification v0.4 Registered (Self-Contained)
- Artifact: `construction/S2_CANDIDATE_SPEC_v0.4.md` (self-contained normative candidate; earlier versions retained as history).
- **Core Resolutions & Hardening in v0.4:**
  1. **Eleven Atomic Parameters (`B7`):** Split `E7` into `E7a` (operation indexing rule) and `E7b` (operational state encoding); `E3` asks for *finest* reset boundary; `E4b` canonical answer space encodes exact orientation.
  2. **Closed-by-Construction Semantic Values (`B8`):** All gold semantic values are frozen enums or typed fields; free text (`note_text`) is recorded and never scored. `AMBIGUOUS` uses canonically sorted set comparison.
  3. **Parameter-Scoped Qualification (`B9`):** Qualification emits `QUALIFIED_FOR` / `NOT_QUALIFIED_FOR` lists; S3 may only use qualified parameters. Hardened with the **dead-cell rule** (no cell 0/5) and a per-parameter stability floor.
  4. **Strict Byte-Level Fidelity Verification (`B10`):** Checker independently parses emitted bundle bytes against sentence bank (100% check; realization index is cross-check only).
  5. **Fabrication Hardened (`F1`):** `AMBIGUOUS` on `NEG-ABSENT` is classified as fabrication (`K1`). Mechanical `EVIDENCE_INVALID` byte-exact check applied to every verdict.
  6. **Model-Free Error Decomposition (`F2`):** Removed unverified independence model; replaced with direct 4-way empirical joint error breakdown.
  7. **Exact Permutation Leakage Probe (`K3`, `F3`):** 50 features (incl. 20 enumerated formatting markers), exact permutation p-value formula frozen on 330 parameter-cells.
  8. **Corpus Volume:** 30 bundles $\times$ 11 parameters = 330 cells (55/class); 1320 total adjudication events.

### Governance & L3 Status
1. **Reclassification [RATIFIED]:** S2 is `INTERNAL_QUALIFICATION`.
2. **Publication Policy [RATIFIED]:** Public qualification artifact permitted without methodological novelty claim.
3. **Five-Party Separation [RATIFIED]:** Constructor $\ne$ Corpus Party $\ne$ Fidelity Checker $\ne$ Adjudicator A $\ne$ Adjudicator B $\ne$ Gate.
4. **Discrimination Thresholds & Stability Floor [PENDING L3 RATIFICATION]:** §8.2 per-parameter conditions, §8.3 class minima, 80% instrument stability floor.
5. **Corpus Budget [PENDING L3 RATIFICATION]:** 30 bundles / 330 cells / 1320 adjudication events.
6. **BatteryLake Manifest Review [PENDING L3 RATIFICATION]:** Open prior-art review under §4.3 constraints.
7. **S3 Frame [DEFERRED]:** Frame selection deferred until prior-art item closes.

### Governance Invariants
- Project ownership, governance decisions, and final freeze ratification reside exclusively with Ivan / VolMax Studio Lab.
- Drafter is an artifact-level methodology author; unratified drafts carry zero governing authority until certified by an independent Gate and ratified by the Operator.
- Confirmatory claims and prospective target inspections are strictly prohibited in S2.

