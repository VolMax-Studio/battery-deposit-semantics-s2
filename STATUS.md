---
project: battery-deposit-semantics-s2
phase: phase_0_prior_art_pending
predecessor: VolMax-Studio/battery-deposit-semantics-s1
predecessor_terminal_state: INSTRUMENT_INVALID
predecessor_terminal_commit: "8812111d77e3526ec07a6d613fa4e82594496b9d"

# L3 Scope & Governance Authorization
authorized_successor_scope: instrument_validation_only
prior_art_elimination_required: true
prior_art_status: pending
confirmatory_claims_authorized: false
prospective_target_inspection: prohibited
dual_adjudication_budget_authorized: true

constructor: Claude/Fable
constructor_conflict_disclosed: true
independent_gate: pending_external_unconflicted_party
prereg_frozen: false
execution_authorized: false
verdict: null
---

## Current State

S2 is authorized exclusively as an `instrument_validation_only` candidate, with confirmatory claims deferred to a potential S3 instance.

### Active Phase: Phase 0 (Prior-Art Elimination)
- **Immediate Task:** Constructor (Claude/Fable) must produce `construction/PRIOR_ART_ELIMINATION_v0.1.md` evaluating whether existing FAIR literature, battery data standards, or prior surveys already answer the research question.
- **Terminal Exit Available:** If the research question is already answered, S2 terminates as `S2_NOT_JUSTIFIED_ALREADY_ANSWERED` without candidate construction.
- **Prospective Targets:** Pinned targets from S1 (High-Doc, TRI, KIT) remain historic exposure only; zero prospective target inspection is permitted.

### Successor Pipeline
1. Phase 0: Prior-Art Elimination (`construction/PRIOR_ART_ELIMINATION_v0.1.md`)
2. Phase 1: Full S2 Candidate Construction (if research gap confirmed)
3. Phase 2: Independent External Gate Evaluation (fresh party with zero S1/S2 construction roles)
4. Phase 3: Operator Freeze Ratification
5. Phase 4: Validation Evidence Acquisition & Dual Blind Adjudication
