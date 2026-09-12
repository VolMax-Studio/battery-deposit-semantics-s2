# S2 Admissibility Assessment — Battery Deposit Semantics

**Instance under consideration:** successor to `VolMax-Studio/battery-deposit-semantics-s1`
**Author of this document:** Claude ("Fable")
**Date:** 2026-09-12
**Status:** `CONSTRUCTION_ARTIFACT` — `AUTHOR_CONFLICT_DISCLOSED` — `NOT_RATIFIED` — `NOT_GATED`
**Layer convention:** P10_LAYER_SEPARATION v1.0.1. Unmarked sentences are L1. L2 sentences are marked `[L2]`. No L3 selections are made in this document.

---

## 0. Conflict declaration — read before anything else

The handoff (§10) asks the incoming constructor to independently interpret the independence rule and assign S2 roles. I must first declare that I am not a neutral party to this instance.

**I was the S1 gate reviewer.** The `INSTRUMENT_INVALID` disposition in §2 of the handoff is mine. I issued it in session `be957953-f0ff-4df1-b089-d7e13891714d` against `REVIEWED_SHA: 34d4afa6259f9f1c4f062ca34bf431887f508098`, in the block reading `CALIBRATION_GATE: FAIL — 2/3 pre-asserted parameters fully resolved`. In that same message I also wrote that a future S2 "would have to separate `P5a cadence` from `P5b coverage verification` in advance, or restrict the calibration expectation for Chung to what was actually recognised before the freeze."

Two consequences follow, and they are not symmetric:

1. Under the RB0 v1.0.3 adjudicator-independence rule (which disqualifies authors, specifiers, implementers of decision rules, and contributing reviewers from independent evaluation), I am disqualified from serving as the **S2 gate** and from serving as an **S2 adjudicator** on any parameter whose decomposition I proposed.
2. The P5a/P5b split named in handoff §5 is **my** post-outcome suggestion. The handoff correctly flags it as outcome-informed. It is also, specifically, *the incoming constructor's own prior proposal presented back to him as a neutral option*. I therefore treat §5 as evidence of contamination, not as a design candidate.

I can construct S2 methodology. I cannot certify it, and I cannot assign my own role. **Role assignment is L3 and belongs to Ivan.**

---

## 1. Conclusion, stated first

An S2-class instance is justified. **It is not justified as a confirmatory study.**

The instrument has never once completed a valid semantic adjudication of any deposit — not one unit, not one parameter set, in either the Sandia instance or S1. Running a confirmatory sample through an instrument with zero demonstrated valid runs is not a study; it is a first run with a verdict attached to it.

The defensible next instance is an **instrument-validation instance** whose only permitted output is a statement about the instrument: whether it produces determinate, reproducible, inter-adjudicator-consistent verdicts on control material. Confirmatory sampling on unexposed deposits is a *subsequent* instance, admissible only after the instrument is frozen on the strength of validation results.

Calling that instance "S2" is fine. Letting it carry confirmatory verdicts is not.

---

## 2. Finding 1 — S1's terminal defect is visible in the frozen text without knowing the outcome

This is the most important finding in this document, because it determines which S2 design changes are admissible.

P5's frozen evaluation question contains **two interrogatives**: what rule governs logging cadence, and how complete temporal coverage of an operation is verified. Its verdict vocabulary contains **one enum slot**. A parameter that asks two independent documentary questions and accepts one resolution value cannot express the state "one half resolved". The enum is not expressive enough to describe the evidence space the parameter defines.

This defect is readable in the frozen artifact `4f168f79…` by anyone who never learns how Chung resolved. It is therefore **not outcome-informed**, and a rule derived from it is admissible in an S2 preregistration:

> **A parameter is admissible only if its evaluation question contains exactly one interrogative and its verdict vocabulary can express every state that question can produce.**

The same test must be applied to P1, P2, P3, P4 and P6. I have not applied it — I would be applying it to text I helped adjudicate. It should be applied by a party with no S1 role, against the frozen text only.

The second half of the defect is the **pre-assertion scope mismatch**: the calibration expectation for P5 was formed from knowledge of the cadence half and asserted over the whole parameter. This too is auditable without the outcome — it requires only comparing the pre-freeze justification against the parameter's own scope. It yields a second admissible rule:

> **A pre-asserted calibration expectation must be scoped identically to the parameter it asserts over, and must cite the located documentary passage that grounds it.**

`[L2]` My inference is that these two rules, applied before freeze, would have prevented S1's terminal state without any reference to Chung's outcome. That inference is testable: apply them retrospectively to the frozen S1 text and see whether P5 survives as written. It should not. Next run, not next sentence.

---

## 3. Finding 2 — calibration-as-gate conflates two causes that cannot be distinguished

S1's validity rule read: if the designated calibration-positive case fails to resolve on all pre-asserted parameters, the instrument is invalid.

When that rule fired, there were two candidate causes, and the rule could not tell them apart:

- **(a)** the instrument is too strict, or misapplies its own standard — the instrument is broken;
- **(b)** the documentation genuinely does not contain what the parameter demands — the instrument is working correctly, and the *designation of the case as calibration-positive on that parameter* was wrong.

S1 collapsed both into `INSTRUMENT_INVALID`. `[L2]` On the evidence in the record, cause (b) is the better-supported reading: Chung explicitly documents a 10 s cadence and documents nothing meeting the frozen coverage-verification standard, and the adjudication of that fact appears correct. Under that reading the instrument did its job and the pre-freeze *designation* failed. This is inference, not a finding, and it **does not reopen S1** — the frozen rule fired, the verdict stands, and the handoff is right that S1 must not be repaired retrospectively.

But it changes what S2 must fix. A calibration architecture that cannot separate "instrument broken" from "case mis-designated" measures the specifier's reading, not the instrument.

The structural correction is to make designation carry its own evidence:

> A case may be designated `CALIBRATION_POSITIVE` **per parameter**, never per case, and only on the basis of a verbatim documentary passage, located and pinned in the preregistration before freeze. A parameter with no pre-located passage is not calibration material.

This raises an obvious objection, and the objection is correct: if you pin the exact passage, calibration only tests **rule application**, not **search**. That is the right scope for one control type, and it exposes that S1 had only one control type where it needed three:

| Control | Tests | Failure it detects |
|---|---|---|
| Positive, passage pre-located | rule application | adjudicator cannot apply its own standard to explicit text |
| Negative, pre-located absence | rule discrimination | adjudicator returns RESOLVED on documentation that does not contain the fact |
| Search-sensitivity, passage exists but is not pointed at | retrieval | adjudicator fails to find documented facts, producing false NOT_RESOLVED |

`[L2]` The negative control is the one S1 most conspicuously lacked and the one that matters most for this research question, because the question's headline finding will be "deposits do not document X". An instrument that has never been shown to return `RESOLVED` and `NOT_RESOLVED` correctly on pre-located material cannot support that finding.

---

## 4. Finding 3 — the largest validity threat was never in S1 at all

`RESOLVED_IN_PINNED_SPACE` is a judgement about whether a documentary space unambiguously specifies a fact. S1 produced that judgement from a **single adjudicator**, subject to review. Review catches fabrication and transcription defects; it does not convert one reader's judgement into a measurement.

The measurable property of a semantic-adjudication instrument is **inter-adjudicator agreement on identical pinned bytes**. Under P10's own standard — Justification: Bounded by Reproducibility — a verdict that a second independent adjudicator would not reproduce is not L1.

This project has an unusual asset here: multiple genuinely independent agents with no shared context. Two adjudicators, blind to each other, working from the same pinned custody package, with disagreement rate and disagreement location as the instrument's primary reported metric, is achievable at ordinary cost.

`[L2]` My assessment is that this single change does more for the defensibility of the eventual confirmatory result than any repair to the calibration architecture, and that an instrument-validation instance built around it is worth running even if every other question in this document is left open.

---

## 5. Finding 4 — the handoff is not as neutral as it states

The handoff declares (§12) that it deliberately abstains from specifying the S2 design. Two places depart from that:

- **§2 and §3** identify the terminal cause as *the frozen calibration-validity construction*. That is one of two readings available on the same facts (see Finding 2). Presenting it as the cause steers the reader toward adjusting the validity rule or the threshold — which §12 then lists as a prohibited assumption. The document forecloses in §2 what it declines to decide in §12.
- **§5** presents the P5a/P5b decomposition as something "participants began referring to". It originated as a specific recommendation from the S1 reviewer, in the same message as the terminal disposition. Naming it in a neutral handoff makes it the salient option regardless of the disclaimer attached.

This is not an accusation of bad faith; it is a finding of the exact kind the project asks for, with its location named. Any independent constructor should read §2 as *a* causal reading and derive their own.

---

## 6. Exposure ledger — what is spent and cannot be recovered

| Item | State | Consequence for S2 |
|---|---|---|
| Chung 2021 (`10.1038/s41597-021-00954-3`), P1/P3/P5-cadence/P5-coverage | Outcome known | Cannot serve as blind or prospective calibration positive. Reusable only as a *closed-book* rule-application control, with full exposure disclosed. |
| P5a/P5b split | Outcome-informed, reviewer-originated | Adoptable only with provenance disclosed in the preregistration, and only if independently re-derivable from the atomicity rule in Finding 1. |
| High-Doc control `10.1038/s41597-024-03831-x` | L0 accession exposure only; no semantic verdict | Semantically unexposed. `[L2]` Probably still usable, but the accession step is spent and the unit is no longer a clean measure of end-to-end acquisition cost. |
| TRI `[72]` / Paper Ref `[71]`, KIT `[8]` / `[86]` | Identities known; L0 exposure; no semantic verdict | Not confirmatory material for S2. Semantic content unexposed, so admissible as *development* material if never verdict-bearing. |
| TRI `[6]` (collision with `[72]`) | Known collision | The frame's top-of-ranking structure is exposed. New draws from the same ranking are "known-adjacent" and must disclose it. |
| dos Reis Table 2 frame | Pre-existing, external, only partially traversed | Frame remains valid. Unexposed rows remain prospective. |
| Validity threshold (3/3) | Failure mode known | Changing the threshold is the single most outcome-informed move available. See §7. |
| S1 design defects (§9 of handoff: DOI error, keyword collision, zinc admission, cell/pack drift, stale checksums) | Documented before freeze | These are known-exposure. They constrain nothing; they are free lessons. |

`[L2]` Net: the frame is not spent, the calibration slot is spent, and the confirmatory slot for three specific units is spent. That is a recoverable position.

---

## 7. The admissibility test for every S2 design change

A change to the S1 architecture is admissible in an S2 preregistration **if and only if** its justification can be written using only the frozen S1 text and general methodology — never the S1 outcome.

| Proposed change | Justifiable from frozen text alone? | Disposition |
|---|---|---|
| Parameters must be atomic (one interrogative) | Yes — P5's two interrogatives are visible in `4f168f79…` | **Admissible** |
| Pre-assertion scope must match parameter scope | Yes — comparison of justification against parameter text | **Admissible** |
| Calibration designated per parameter, with pre-located passage | Yes — general measurement methodology | **Admissible** |
| Negative and search-sensitivity controls added | Yes — general control design | **Admissible** |
| Dual blind adjudication | Yes — reproducibility standard | **Admissible** |
| Splitting P5 specifically into P5a/P5b | No — the split's salience comes from the outcome | **Admissible only as a consequence of the atomicity rule applied uniformly to P1–P6, with §5 provenance disclosed. Not admissible as a targeted repair of P5.** |
| Lowering the validity threshold (3/3 → 2/3, or per-parameter) | No | **Inadmissible as a first move — this is threshold-shopping and will be read as such** |
| Replacing Chung with another calibration positive | Depends entirely on whether the replacement is designated by the new per-parameter rule | Conditional |
| Retaining S1 confirmatory targets | No | **Inadmissible for confirmatory use** |

The asymmetry in row 6 is the discipline worth keeping: fix the *class* of defect uniformly, and let P5 fall out of it. Fixing P5 alone, because P5 is what broke, is the post-hoc move.

---

## 8. What remains prospectively testable

The underlying research question is undamaged:

> Can the export semantics required to interpret a public battery dataset be resolved from that deposit's pinned public documentation alone?

Nothing S1 did leaked into the contents of unexposed deposits. The question's origin is also solid and external: it arose from the Sandia instance, where six export-semantics parameters were `UNESTABLISHED` and a 1,032-record baseline consequently became `NOT_EVALUABLE`. That is a real, independently observed failure of reproducibility, not a hypothesis constructed to be interesting.

What is *not* yet established, and must be established before any S2 freeze:

- **Prior-art elimination.** Whether this question is already answered by existing FAIR-assessment work, by dos Reis et al. themselves, or by battery-data-standards literature. If it is answered, S2 is not justified as a research instance — it becomes at most a replication. This check must precede freeze and must be done by a party willing to return "already answered".
- **Whether a null result is publishable in this project's terms.** If the finding is "most deposits do not document export semantics", the instrument must be trusted enough to carry a negative. That is exactly what the controls in Finding 2 buy.

---

## 9. Role analysis (analysis only — assignment is L3)

| Party | S1 role | Conflicted for S2 as… | Eligible for S2 as… |
|---|---|---|---|
| Ivan | Construction, specification, ratification | Semantic adjudicator | Ratifier (L3), unchanged |
| Claude / Fable | S1 gate reviewer; originator of the P5a/P5b suggestion | S2 gate; S2 adjudicator on Chung or on P5 decomposition | Methodology constructor, with output submitted to a non-conflicted gate |
| Sol | S1 instrument, sampling, calibration, decision-rule construction | S2 instrument constructor | S2 gate **only if** S2's parameter text is not substantially inherited from S1 |
| Implementation agent(s) that encoded S1 classifier logic | Implementer | Adjudicator | Implementer of S2, non-adjudicating |
| Any agent with no S1 exposure | — | — | Adjudicator; negative-control designation |

The proposal raised earlier — Claude constructs, Sol gates — is **formally admissible under a per-artifact reading of the independence rule** (neither party evaluates its own S2 work), but it has a specific failure mode that must be closed explicitly: if S2 reuses S1 parameter definitions authored by Sol, Sol gating S2 is Sol reviewing Sol's own frozen text. Either S2's parameters are re-derived from the underlying semantic questions by a different party, or the gate is a third agent.

`[L2]` My view is that the atomicity rule in Finding 1 forces a full parameter re-derivation anyway, which incidentally resolves this. But that is a consequence I would be asserting about my own eligibility, so it is stated as inference and left to Ivan.

---

## 10. Conditions under which prospective target inspection becomes admissible

I have inspected no prospective S2 target. Inspection becomes admissible only after all of the following are frozen in Git, in this order:

1. Prior-art elimination complete and recorded, with the "already answered" outcome genuinely available.
2. Parameter set re-derived under the atomicity rule; every parameter passes the one-interrogative test; verdict vocabulary expressive over the full state space of each question.
3. Per-parameter calibration designations made, each citing a pre-located verbatim passage, for positive, negative, and search-sensitivity controls.
4. Adjudication protocol frozen: number of adjudicators, blinding, disagreement-resolution rule (resolution rule frozen *before* any disagreement is observed).
5. Sampling frame draw rule frozen, with the exposed rows (`[72]`, `[6]`, `[8]`, High-Doc) excluded **by name** and the ranking-adjacency exposure disclosed.
6. Instance scope declared as instrument-validation, with an explicit statement that no confirmatory verdict may be emitted from it.
7. Kill conditions frozen: the states in which S2 itself terminates without a verdict.

Item 7 is not decoration. S1's single greatest asset is that it terminated honestly on its own calibration case. S2 must be capable of the same, and must say in advance what that would look like.

---

## 11. Open questions for Ivan (L3 — not selected here)

1. Does this instance proceed as instrument-validation only, with confirmatory sampling deferred to a later instance?
2. Who gates S2, given that both Claude and Sol carry S1 roles?
3. Is prior-art elimination run before any construction work, with a real willingness to conclude that no S2 is warranted?
4. Is the project prepared to fund two independent adjudicators per unit, which roughly doubles per-unit adjudication cost?

---

**Status:** `SPREMNO ZA GEJT`. This document is a construction artifact authored by a party with a declared S1 conflict. It must not be treated as ratified, and it must not be gated by its author.
