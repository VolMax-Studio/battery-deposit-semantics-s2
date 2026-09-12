# Party-7 Gate Handoff — `battery-deposit-semantics-s2` (v0.10 Re-Gate)

**Candidate under gate:** `construction/S2_CANDIDATE_SPEC_v0.10.md`, verbatim, unmodified
**Handoff authored by:** Claude ("Fable"), the candidate's constructor — see §1
**Date:** 2026-09-12
**Status of the candidate:** `SPREMNO ZA GEJT` — requires G1 re-gate following `G1-BLOCK-001`
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items are listed and not decided here.

---

## 0. What this document is

A cover note for the independent gate performing the **G1 Specification Gate** on `S2_CANDIDATE_SPEC_v0.10.md`.

Candidate v0.10 was created under the amended §12.2 process rule specifically authorized by `G1-BLOCK-001` (returned by an external, unexposed G1 gate on v0.9). It addresses the structural flaw in `E8a` (scopes without legal units, leading to answer derivability from scope) via the new `SCOPE-2` constraint and narrows `E8a` to `current` (`A`, `mA`) and `voltage` (`V`, `mV`).

---

## 1. Conflict-of-role disclosures

| Party | S1 role | S2 role | Consequence |
|---|---|---|---|
| **Fable** (Claude) | S1 gate reviewer; issued the `INSTRUMENT_INVALID` disposition; originated the `E5`/`E6` decomposition suggestion after the S1 outcome was known | Constructor of the candidate and author of this handoff | Excluded from gate, adjudication, corpus authorship, bank validation, fidelity checking |
| **Sol** | S1 instrument, sampling, calibration and decision-rule construction | Adversarial pre-gate reviewer only | Excluded from gate and all execution roles |
| **Ivan** | S1 construction, specification and ratification | Operator; L3 ratification | Excluded from all evaluative and execution roles; retains ratification, which is not evaluation |
| **Any agent that materially encoded S1 classifier or decision logic** | Implementer | — | Excluded from parties 2–8 |

---

## 2. Lineage & Exposure Constraints

S1 terminated at `INSTRUMENT_INVALID` due to compound interrogatives under a single verdict slot. S2 is strictly an internal qualification on a Constructed Validation Domain (CVD) touching no real deposits.

- Chung 2021 is permanently excluded.
- `E5`/`E6` provenance is disclosed.
- Prospective target battery deposits remain uninspected.

---

## 3. Prior-Art Status

Governed by `construction/PRIOR_ART_ELIMINATION_v0.2.md`:
- `RESEARCH_QUESTION: NOT_SHOWN_TO_BE_ALREADY_ANSWERED`
- `PRIOR_ART_ELIMINATION: INCOMPLETE` (BatteryLake curation manifests uninspected, pending L3 ratification).
- `METHOD_STATUS: CORE_COMPONENTS_ANTICIPATED` (Reverse generation, verbatim extraction, abstention are published prior art; no methodological novelty claimed).

---

## 4. What Party 7 is asked to decide (G1 Re-Gate)

Does `S2_CANDIDATE_SPEC_v0.10.md` specify an instrument-qualification instance that could be executed exactly as written, without requiring post-result invention of rules?

Key areas to scrutinize:
- **`SCOPE-2` (§3.2):** Does requiring $\ge 2$ legal values per scope fully prevent answers being implied by scopes?
- **`E8a` Narrowing (§4.1, §4.2):** Does restricting `E8a` to current (`A`, `mA`) and voltage (`V`, `mV`) maintain qualification value while ensuring `AMBIG-CONSTRUCTED` remains constructible?
- **Terminology (§8):** Does the separation between `parameter-cell` (individual instance) and `class score` (count out of 5) cleanly resolve earlier scoring ambiguities?
- **Pre-existing open items:** §5.1 constraint script (deferred to G2), §5.2.3 numeric diversity gap (open L3 decision), §5.4 / §13.3 bank meaning limitations.

---

## 5. Unratified Items (Candidate §15)

1. Stage 2 class-score floor $\ge 3/5$, parameter floor $\ge 25/30$, semantic stability $\ge 24/30$.
2. Global $K1$ fabrication kill condition (0 tolerance across 660 adjudications).
3. Bank loop limits: 3 attempts per slot, cumulative rejection ceiling 99.
4. Coverage contract levels: $\ge 2$ parameter-cells per coverage category, $\ge 2$ composition, $\ge 2$ per stratum.
5. Numeric-payload coverage diversity (open by construction).
6. Staffing of 7 separated parties ($K5$).
7. Corpus budget: 330 single-use bank entries, 30 bundles, 1320 adjudication events.
8. Publication status.
9. BatteryLake manifest review (output: `PRIOR_ART_ELIMINATION_v0.3.md` if ratified).
10. Paywalled / non-English literature sweep.

---

## 6. Package Manifest for Party 7

1. `construction/S2_CANDIDATE_SPEC_v0.10.md` (verbatim)
2. `construction/PRIOR_ART_ELIMINATION_v0.2.md`
3. `construction/S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
4. `construction/PARTY7_GATE_HANDOFF.md` (this document)
