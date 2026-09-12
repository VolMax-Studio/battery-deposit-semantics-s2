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

construction_status: candidate_v0.3_self_contained_pending_gating
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

### Candidate Specification v0.3 Registered (Self-Contained)
- Artifact: `construction/S2_CANDIDATE_SPEC_v0.3.md` (self-contained normative candidate; v0.1 and v0.2 retained as history).
- **Core Resolutions & Hardening:**
  1. **Semantic Value Scoring (`B2`):** Correctness requires joint match on `(verdict_class, semantic_value)`. Output schema explicitly tracks factual determinations and isolates `value error`.
  2. **Explicit Qualification Decision Function (`B1`):** Complete deterministic mapping to `QUALIFIED` / `NOT_QUALIFIED` across discrimination, stability, determinism, fidelity, leakage, and staffing.
  3. **Cluster-Honest `K1` (`B3`):** Deleted unjustified Bernoulli rate bounds; strict literal zero-tolerance (0 of 50 per adjudicator).
  4. **Fully Executable `K3` Probe (`B4`):** Fixed multinomial logistic regression on 49 frozen surface features + one-hot parameter ID; grouped 5-fold CV by bundle; 2000-iteration bundle-vector permutation test ($\alpha=0.01$).
  5. **Deterministic Template Generator & Fidelity Proof (`B5`):** Bundles generated from sentence bank via frozen seed; mechanical 100% byte-identical re-derivation check required.
  6. **Corrected Freeze Order (`B6`):** Ground truth authored and sealed at `F5` *before* bundle generation (`F6`) and leakage probe (`F7`).
  7. **Strictly Delimited `EXPLICIT_FILE`:** Text/header/units declarations only; value patterns explicitly prohibited.
  8. **Deterministic Re-Run on Both Adjudicators:** Canonical serialization; 1200 total adjudication events.
  9. **Declared Ecological Gap:** Passing `QUALIFIED` does not license S3; prevents starting S3 with a broken instrument.

### Governance & L3 Status
1. **Reclassification [RATIFIED]:** S2 is `INTERNAL_QUALIFICATION`.
2. **Publication Policy [RATIFIED]:** Public qualification artifact permitted without methodological novelty claim.
3. **Five-Party Separation [RATIFIED]:** Constructor $\ne$ Corpus Party $\ne$ Fidelity Checker $\ne$ Adjudicator A $\ne$ Adjudicator B $\ne$ Gate.
4. **Discrimination Thresholds & Stability Floor [PENDING L3 RATIFICATION]:** §8.1 thresholds and 80% stability floor.
5. **Corpus Budget [PENDING L3 RATIFICATION]:** 30 bundles / 300 cells / 1200 adjudication events.
6. **BatteryLake Manifest Review [PENDING L3 RATIFICATION]:** Open prior-art review under §4.3 constraints.
7. **S3 Frame [DEFERRED]:** Frame selection deferred until prior-art item closes.

### Governance Invariants
- Project ownership, governance decisions, and final freeze ratification reside exclusively with Ivan / VolMax Studio Lab.
- Drafter is an artifact-level methodology author; unratified drafts carry zero governing authority until certified by an independent Gate and ratified by the Operator.
- Confirmatory claims and prospective target inspections are strictly prohibited in S2.

