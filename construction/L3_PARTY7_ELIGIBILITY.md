# L3 — PARTY-7 ELIGIBILITY & GATE PROTOCOL

**Project:** `battery-deposit-semantics-s2`  
**Status:** `RATIFIED` by Operator (Ivan / VolMax Studio Lab)  
**Date:** 2026-09-12  

---

## 1. Two Independent Requirements

Party 7 must satisfy both criteria:

### A. PROCEDURAL INDEPENDENCE
The reviewing actor must have:
* no S1 evaluative, specification, implementation, or decision-rule role;
* no S2 construction or internal adversarial-review role;
* no exposure to internal review transcripts or internal verdicts;
* no authorship of the artifacts it is asked to gate.

Eligibility under this condition is actor-specific. Prior exposure of one session does not automatically disqualify every fresh instance of an unconflicted model family.

### B. REDUCED SHARED-SOURCE CORRELATION
The gate must not be drawn from a model family whose priors materially shaped the candidate being reviewed.

This requirement does **not** establish full epistemic or statistical independence. Its narrower purpose is to avoid the clearest source of correlated review error: asking a model family to independently gate a specification that was materially constructed through that same family's priors.

---

## 2. Model Family Eligibility

Under the record of `battery-deposit-semantics-s2`:

* **Claude / Anthropic family — NOT ELIGIBLE.**
  Claude/Fable authored the candidate and therefore materially shaped it.
* **GPT / OpenAI family — NOT ELIGIBLE.**
  Sol's adversarial reviews materially reshaped the candidate across multiple revisions.
* **Previously exposed Gemini session — NOT ELIGIBLE.**
  Procedurally exposed via prior analytical drafts.
* **Fresh, context-isolated third-party instance (e.g. xAI Grok / fresh Gemini) — ELIGIBLE.**
  Priors did not shape `S2_CANDIDATE_SPEC_v0.9`. Must receive only the frozen Gate package in a clean context with zero prior conversation history.

---

## 3. Human Reviewer Eligibility

A human reviewer is eligible only if both unexposed and sufficiently competent in:
* preregistration / reproducibility / audit methodology;
* experimental or benchmark validation design;
* statistical testing and leakage controls;
* battery-data semantics or time-series documentation.

A suitably qualified, unexposed human reviewer remains the strongest available Party-7 route when practically obtainable.

---

## 4. Frozen Gate Package

Party 7 receives strictly:
1. `construction/S2_CANDIDATE_SPEC_v0.9.md`
2. `construction/PRIOR_ART_ELIMINATION_v0.2.md`
3. `construction/S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
4. `construction/PARTY7_GATE_HANDOFF.md`

**Excluded:**
* Adversarial pre-gate transcripts.
* Internal reviewer verdicts / closure PASS.
* Informal coaching or leading prompts.

---

## 5. Three-Part Gate Disposition

Party 7 reports findings in three separate categories:

### A. METHOD ARCHITECTURE: `PASS` | `BLOCK`
> Does the frozen specification define an executable qualification instance without requiring post-result invention of rules?

### B. L3 POLICY VALUES: `ACCEPTABLE_AS_PROPOSED` | `REQUIRES_OPERATOR_DECISION` | `METHOD_BLOCKING`
For each unresolved L3 policy choice. (Architecture PASS does not silently ratify constructor policy numbers).

### C. ARTIFACTS NOT YET PRODUCED: `DEFERRED_TO_ARTIFACT_GATE`
For F2/F3 executable scripts, scope table, and sentence bank to be evaluated at G2.

---

## 6. Two-Pass Gate Rule

* **G1 — SPECIFICATION GATE:** Performed on `S2_CANDIDATE_SPEC_v0.9` and its handoff package. Evaluates method completeness and identifies open L3 decisions before freeze.
* **G2 — ARTIFACT-CONFORMITY GATE:** Performed after F2/F3 scripts and sentence bank exist, before execution. Verifies faithful implementation of frozen spec. G2 may not reopen methodology or tune thresholds.
