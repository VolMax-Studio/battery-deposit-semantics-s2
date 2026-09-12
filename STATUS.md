---
project: battery-deposit-semantics-s2
phase: internal_qualification_pending_gate
instance_type: INTERNAL_QUALIFICATION
predecessor: VolMax-Studio/battery-deposit-semantics-s1
predecessor_terminal_state: INSTRUMENT_INVALID
predecessor_terminal_commit: "8812111d77e3526ec07a6d613fa4e82594496b9d"

# Governance & Provenance
project_owner: Ivan / VolMax Studio Lab
operator: Ivan
final_ratifier: Ivan

construction_status: candidate_gating_pending
current_methodology_drafter: Claude/Fable
drafter_conflict_disclosed: true
validation_corpus_author: Sol (satisfies K5 independence)

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

S2 is formally reclassified as an **`INTERNAL_QUALIFICATION`** instance (instrument validation only; precondition for potential S3 confirmatory work). Zero research novelty is claimed for the synthetic benchmark methodology; the measurand (export semantics documentation vs file-intrinsic data recovery) remains unoccupied.

### Phase 0 Prior-Art Elimination Delivered
- Report: `construction/PRIOR_ART_ELIMINATION_v0.1.md` (Fable v0.1).
- **Findings:**
  1. Synthetic grounding / "reverse annotation" paradigm is fully anticipated in published literature (RIKER, VAREX, DTBench, PSEBench).
  2. BatteryLake (arXiv:2607.09762, NTU July 2026) is the nearest neighbor; it normalizes export semantics away via physical plausibility rather than measuring documentation resolvability (`S-DOC` vs `S-FILE`).
  3. Research question on export-semantics resolvability survives within a narrow, defensible scope.

### Candidate Specification Registered
- Candidate specification: `construction/S2_CANDIDATE_SPECIFICATION_FABLE_v0.1.md` (Fable v0.1).
- 36-bundle synthetic validation corpus (288 labels, 576 adjudications).
- Atomic namespace `E1`–`E8` with scope rule.
- Strata distinction (`S-DOC` vs `S-FILE`) without ranking.
- Dual blind adjudicators; disagreements unforced; discrimination gates stability.

### Ratified L3 Decisions
1. **Reclassification:** S2 accepted as `INTERNAL_QUALIFICATION` (no novelty claim, prerequisite for S3).
2. **Corpus Author Independence:** Sol is designated author of synthetic validation corpus bundles & reference labels, satisfying Kill Condition `K5` (Sol carries zero S2 instrument drafting role).
3. **Dual Adjudicators:** Authorized budget for two fresh, independent model channels (e.g. GPT-4o + Gemini Pro), strictly blinded to each other and §5/§6/§7 rules.
4. **Negative Control Floor:** Ratified $\ge 90\%$ accuracy requirement on `NEG-ABSENT` items (`K1`).
5. **Ecological Check:** Ecological real-deposit check deferred out of S2.
6. **BatteryLake Records:** Curation manifests of BatteryLake's 41 datasets remain UNOPENED during S2 to preserve the prospective S3 sampling frame.

### Governance Invariants
- Project ownership, governance decisions, and final freeze ratification reside exclusively with Ivan / VolMax Studio Lab.
- Drafter is an artifact-level methodology author; unratified drafts carry zero governing authority until certified by an independent Gate and ratified by the Operator.
- Confirmatory claims and prospective target inspections are strictly prohibited in S2.

