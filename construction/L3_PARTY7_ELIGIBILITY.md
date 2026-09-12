# L3 — PARTY-7 ELIGIBILITY & TWO-PASS GATE PROTOCOL

**Project:** `battery-deposit-semantics-s2`  
**Status:** `RATIFICATION_CANDIDATE`  
**Final ratification belongs only to the human operator (Ivan / VolMax Studio Lab).**  
**Date:** 2026-09-12  

---

## 1. Party-7 Eligibility Criteria

Party 7 must satisfy both requirements:

### A. PROCEDURAL INDEPENDENCE
The reviewer must have:
* no S1 evaluative, specification, implementation, or decision-rule role;
* no S2 construction or internal adversarial-review role;
* no exposure to internal review transcripts or internal verdicts;
* no authorship of the artifact being gated.

This criterion is actor-specific. Prior exposure of one session does not automatically disqualify every fresh instance of an unconflicted model family.

### B. REDUCED_SHARED_SOURCE_CORRELATION
The reviewer must not be drawn from a model family whose output materially shaped the candidate or a normative doctrine artifact on which the candidate relies.

This requirement does **not** establish full epistemic or statistical independence. It only reduces an identifiable source of correlated review error.

Family exclusion requires positive provenance of material contribution; mere mention of a family as a potential project agent is not sufficient.

---

## 2. Current Eligibility on the Provenance Record

* **Claude / Anthropic family — NOT ELIGIBLE.**  
  The family directly authored the candidate specification (`S2_CANDIDATE_SPEC_v0.9.md`).
* **GPT / OpenAI family — NOT ELIGIBLE.**  
  Sol’s adversarial findings materially shaped multiple normative elements of the candidate across revisions.
* **Previously exposed Gemini actor/session — NOT ELIGIBLE.**  
  Actor-level procedural exposure.
* **Fresh, context-isolated Gemini-family instance — ELIGIBLE ON CURRENT RECORD**, unless positive provenance later shows material family contribution to the candidate or its normative doctrine.
* **Fresh, context-isolated Grok / xAI-family instance — ELIGIBLE ON CURRENT RECORD**, as no material Grok/xAI contribution to the candidate or governing P10 doctrine is established in the provenance record.

---

## 3. Human Reviewer Eligibility

A human reviewer is eligible only if both unexposed and competent in the relevant methodology, including enough expertise in:
* preregistration and audit reproducibility;
* validation / benchmark design;
* statistical leakage controls;
* scientific software verification;
* battery-data semantics or time-series documentation.

Being human alone does not establish suitability.

---

## 4. Frozen Gate Package

Party 7 receives strictly:
1. `construction/S2_CANDIDATE_SPEC_v0.9.md`
2. `construction/PRIOR_ART_ELIMINATION_v0.2.md`
3. `construction/S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
4. `construction/PARTY7_GATE_HANDOFF.md`

Excluded:
* internal review transcripts;
* internal verdicts;
* internal closure `PASS`;
* informal coaching or hints about expected findings.

---

## 5. Clarification Rule

Party 7 may ask clarification questions.

The operator may answer **only by pointing to an existing section of the frozen Gate package**.

No new interpretation, explanation, example, threshold, or methodological rule may be supplied.

If a question cannot be resolved strictly from the frozen text, that ambiguity is itself recorded as a G1 finding.

---

## 6. G1 Specification Gate Output

Party 7 returns findings under three distinct categories:

### A. METHOD ARCHITECTURE: `PASS` | `BLOCK`
Question:
> Does the frozen specification define an executable qualification instance without requiring post-result invention of rules?

### B. L3 POLICY VALUES: `ACCEPTABLE_AS_PROPOSED` | `REQUIRES_OPERATOR_DECISION` | `METHOD_BLOCKING`
Evaluated for each open L3 policy choice listed in §15 of the candidate specification.

### C. ARTIFACTS NOT YET PRODUCED: `DEFERRED_TO_ARTIFACT_GATE`
Identifies all F2/F3 executable scripts, schemas, tables, and sentence bank deferred to G2.

The Gate may also issue findings against the handoff document itself (including framing or disclosures).

For every `BLOCK`, Party 7 identifies:
* the exact section;
* the defect;
* the frozen rule or requirement violated.

A proposed repair may be supplied, but proposing a repair does not adopt it.

---

## 7. G2 Artifact-Conformity Gate

F2/F3 artifacts that do not exist at G1 are not treated as gated.

After they are produced, a **different, fresh eligible reviewer instance** performs G2.

G2 evaluates whether the produced artifacts faithfully implement:
* the frozen specification;
* ratified L3 decisions;
* the frozen G1 disposition boundary.

The G2 reviewer must not receive the G1 reasoning transcript. It receives only the frozen G1 disposition/findings.

G2 may return:
* `ARTIFACT_CONFORMITY_PASS`
* `ARTIFACT_CONFORMITY_BLOCK`
* `METHODOLOGY_DEFECT_DISCOVERED_AT_G2`

`METHODOLOGY_DEFECT_DISCOVERED_AT_G2` invalidates reliance on G1. The frozen instance terminates, requiring an explicit new methodology version/instance rather than in-flight silent patching.

---

## 8. Terminological Boundary

A different-vendor or otherwise eligible AI Gate provides **reduced shared-source correlation under the P10 role architecture**.

It is not equivalent to:
* human peer review;
* full epistemic independence;
* independent empirical replication.
