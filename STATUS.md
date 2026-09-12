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

construction_status: candidate_v0.2_pending_gating
current_methodology_drafter: Claude/Fable
drafter_conflict_disclosed: true
corpus_reference_label_party: pending_fresh_unconflicted_party (strictly not Sol, K5)

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

S2 is formally categorized as an **`INTERNAL_QUALIFICATION`** instance (instrument qualification only; prerequisite for potential S3 confirmatory work). Core validation architecture components are acknowledged as anticipated in published prior art (RIKER, VAREX, DTBench, PSEBench); the battery-domain documentation resolvability measurand remains unoccupied.

### Phase 0 Prior-Art Elimination v0.2 Registered
- Artifacts:
  - `construction/PRIOR_ART_ELIMINATION_v0.1.md` (historical baseline)
  - `construction/PRIOR_ART_ELIMINATION_v0.2.md` (active v0.2)
- **Status:**
  - `RESEARCH_QUESTION: NOT_SHOWN_TO_BE_ALREADY_ANSWERED`
  - `PRIOR_ART_ELIMINATION: INCOMPLETE`
  - `METHOD_STATUS: CORE_COMPONENTS_ANTICIPATED (no novelty claim)`
  - `OPEN_PRIOR_ART_ITEM: BatteryLake public curation / processing manifests pending L3 ratification`

### Candidate Specification v0.2 Registered
- Artifacts:
  - `construction/S2_CANDIDATE_SPECIFICATION_FABLE_v0.1.md` (historical baseline)
  - `construction/S2_CANDIDATE_SPEC_v0.2.md` (active v0.2 candidate)
- **Key Architectural Refinements:**
  1. **Ten Atomic Parameters:** `E4` split to `E4a`/`E4b` (timestamp position vs endpoint inclusivity); `E8` split to `E8a`/`E8b` (unit vs scaling).
  2. **Five-Value Vocabulary:** Deleted `INFERABLE` to eliminate unbounded subjective model completion; declared conservative direction of error.
  3. **Grouped Permutation Leakage Probe (`K3`):** 30 bundles, 300 parameter-cells (10/bundle), balanced per-parameter (5 cells/class across 6 classes), within-bundle cap $\le 3$ cells/class. Grouped CV by bundle; permutation unit is full 10-cell bundle vector.
  4. **Strict Zero-Tolerance Fabrication Floor (`K1`):** Exactly 0 fabrications out of 50 `NEG-ABSENT` cells per adjudicator (bounds fabrication rate to $\le 5.8\%$, 95% one-sided).
  5. **Rigorous Four-Party Independence (`K5`):** Corpus & ground truth generator MUST be a fresh unconflicted party (explicitly excluding Sol, Claude, Gemini/Ananke, Codex, Ivan). If not staffed, `K5` terminates S2.

### Ratified & Pending L3 Decisions
1. **Reclassification [RATIFIED]:** S2 is `INTERNAL_QUALIFICATION`.
2. **Publication Policy [RATIFIED]:** Public qualification artifact permitted without methodological novelty claim.
3. **Four-Party Separation [RATIFIED]:** Constructor (Claude/Fable) $\ne$ Corpus Party (Fresh $\ne$ Sol) $\ne$ Adjudicator A $\ne$ Adjudicator B $\ne$ Gate (Fresh 4th party).
4. **Corpus Budget [PENDING L3]:** 30 bundles / 300 cells / 600 primary adjudications (900 total with determinism re-run).
5. **BatteryLake Manifest Review [PENDING L3]:** Review of published curation records as `PRIOR_ART_EXPOSURE` (with permanent exclusion of exposed units from prospective S3 pool).
6. **S3 Frame [DEFERRED]:** dos Reis Table 2 vs BatteryLake registry deferred until prior-art item closes.

### Governance Invariants
- Project ownership, governance decisions, and final freeze ratification reside exclusively with Ivan / VolMax Studio Lab.
- Drafter is an artifact-level methodology author; unratified drafts carry zero governing authority until certified by an independent Gate and ratified by the Operator.
- Confirmatory claims and prospective target inspections are strictly prohibited in S2.

