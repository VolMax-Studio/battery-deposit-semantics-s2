# S2 Candidate Specification — Deposit Semantics Instrument Validation

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INSTRUMENT_VALIDATION_ONLY`
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `construction/S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified, not gated
**Layer convention:** P10_LAYER_SEPARATION v1.0.1. Unmarked = L1. `[L2]` = inference. L3 decisions are listed in §11 and are not made here.

This document is written to be frozen. Where a choice was available, it is made and justified, not offered. No prospective target has been inspected.

---

## 1. What S2 measures

S2 measures **the instrument**, not any deposit.

> Does the deposit-semantics adjudication instrument produce verdicts that are (a) discriminating against known ground truth, (b) stable under adjudicator substitution, and (c) deterministic on re-run?

S2 emits no statement about any real dataset, no prevalence figure about documentation quality in the literature, and no confirmatory finding. Those belong to a later instance and are prohibited outputs here (§9).

### 1.1 The governing constraint that shapes everything below

An adjudication instrument cannot be validated on material whose labels are themselves produced by adjudication. If the reference label for "does deposit X document its sign convention?" is obtained by having someone adjudicate deposit X, the validation is circular: it measures agreement between two applications of the same unproven procedure.

Therefore the primary validation corpus is **constructed, with ground truth written before the documentary artifact**, not discovered. This is the single most consequential design decision in this specification and it is derived, not inherited: it follows from the definition of validation, independently of anything S1 observed.

---

## 2. Documentary space (`D`)

`RESOLVED_IN_PINNED_SPACE` was never fully defined in S1: the space was pinned by hash, but its *strata* were not distinguished, so one evidence type could be argued for or against a verdict with no rule governing which.

For each unit, `D` is an exhaustive, ordered manifest. Every entry carries: URI or generation ID, retrieval or generation timestamp, SHA-256, media type, and a stratum tag.

| Stratum | Contents | Proposition it can support |
|---|---|---|
| `S-DOC` | Article of record, supplementary information, landing-page prose, README, codebook, data dictionary | *The depositor stated a rule.* |
| `S-FILE` | File-intrinsic evidence: column names, header rows, declared units, value patterns | *This file exhibits a property.* |

These are different propositions and they are not interchangeable. A file that happens to contain no gaps does not establish that the depositor applied a gap-verification rule; a stated rule does not establish that the shipped file obeys it.

**The instrument does not rank the strata.** It records which stratum carried the verdict. Ranking them would be a judgement about what counts as adequate documentation — that is a finding for a later instance to produce, not an assumption to freeze into the instrument.

---

## 3. Parameters (`E1`–`E8`)

New namespace. S1 parameter text is not inherited: it was authored by a party who is excluded from S2 construction, and inheriting it would import both its authorship and its compound structure.

**Atomicity rule (frozen):** a parameter is admissible only if its evaluation question contains exactly one interrogative, and its verdict vocabulary can express every state that question can produce. Applied uniformly to all eight below.

**Scope rule (frozen):** a verdict is emitted per `(unit, parameter, scope)`, where scope is the declared set of columns or signals the verdict governs. A deposit that documents sign for current but not for power yields two scope rows with different verdicts. This keeps parameters atomic without collapsing partial coverage into a single value.

| ID | Interrogative |
|---|---|
| `E1` | For a signed quantity, which sign denotes charge and which denotes discharge? |
| `E2` | What does a zero value in a signal column denote — measured zero, rest, or unrecorded? |
| `E3` | At which boundary does a cumulative quantity reset to zero? |
| `E4` | Does a reported interval's timestamp denote the interval's start, end, or midpoint, and are endpoints inclusive? |
| `E5` | What rule governs the interval between logged records? |
| `E6` | By what rule is the absence of unlogged gaps in a record sequence established? |
| `E7` | By what rule does a record map to an operation (cycle, step, test)? |
| `E8` | In what physical units is each quantity reported, and what scaling, if any, was applied? |

### 3.1 Mandatory provenance disclosure for `E5`/`E6`

`E5` and `E6` correspond to the two interrogatives that S1 carried in one compound parameter. The distinction between logging cadence and coverage verification was first named by the S1 reviewer **after** the S1 outcome was known, and that reviewer is the constructor of this document.

Both of the following are recorded facts and both must appear in the frozen preregistration:

1. The distinction is outcome-informed in origin.
2. In S2 it is re-derived by applying the atomicity rule uniformly to all eight parameters — `E1` splits by scope, `E4` splits endpoint-position from endpoint-inclusivity by the same test, and `E5`/`E6` split by the same test. It is not a targeted repair.

`[L2]` My assessment is that (2) makes the split admissible. That is the constructor's inference about his own work and is the first thing a gate should attack.

### 3.2 Note on `E8`

`E8` is expected to resolve almost everywhere and therefore carries little discriminative information about deposits. It is retained deliberately as a ceiling check: an adjudicator that fails `E8` has a retrieval or application defect, not a hard case.

---

## 4. Verdict vocabulary (`V`)

S1 carried a single `RESOLVED_IN_PINNED_SPACE` value. That collapses five distinguishable states into a boolean.

| Value | Meaning | Evidence required |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | artifact SHA-256, locator, verbatim excerpt |
| `EXPLICIT_FILE` | Located `S-FILE` evidence determines it unambiguously | artifact SHA-256, locator, verbatim excerpt |
| `INFERABLE` | Not stated; one reading survives from located evidence plus a stated inference step | evidence as above **plus** the inference step written out |
| `AMBIGUOUS` | Evidence located; more than one reading survives | all surviving readings, each with its evidence |
| `ABSENT` | Exhaustive traversal of `D` found no bearing evidence | traversal record: every manifest entry, marked examined |
| `NOT_APPLICABLE` | The unit contains no data of the kind the parameter governs | located justification |

No free-text verdicts. No verdict without its evidence block. `ABSENT` is the only value requiring a negative traversal record, and it is the value most likely to be reached lazily — the traversal record exists to make laziness visible.

---

## 5. Validation corpus

### 5.1 Primary corpus — constructed

Documentary bundles written from a frozen generation specification, each consisting of an article-style excerpt, a README, and a CSV header block. Each bundle carries a ground-truth vector over `E1`–`E8`, written before the bundle text.

Six item classes, each targeting a distinct failure mode:

| Class | Construction | Failure it detects |
|---|---|---|
| `POS-EXPLICIT` | Fact stated plainly and prominently | Cannot apply own standard to clear text |
| `POS-BURIED` | Fact stated, but in supplementary material or a non-obvious section | Retrieval failure producing false `ABSENT` |
| `NEG-ABSENT` | Fact genuinely present nowhere in `D` | False `EXPLICIT` / `INFERABLE` — fabrication |
| `NEG-ADJACENT` | A related but non-determining statement present | Accepting a neighbouring fact as the asked-for fact |
| `AMBIG-CONSTRUCTED` | Two incompatible statements present | Picking one reading instead of returning `AMBIGUOUS` |
| `NA-CONSTRUCTED` | No data of the governed kind | Forcing a verdict where none applies |

`NEG-ADJACENT` is included as a general class, not as a reconstruction of any S1 case. No real deposit, including Chung, is used as a template, and no S1 evidence file enters the corpus.

**Size, derived:** each bundle yields one label per parameter, so N bundles yield N labels per parameter. Detecting gross per-class failure requires at least five labels per `(parameter, class)` cell; six classes gives a floor of 30, and a balanced assignment design requires a multiple of six. **Minimum 36 bundles** → 288 ground-truth labels → 576 adjudications at two adjudicators.

This is a **failure-detection design, not an estimation design.** Frozen consequence: no confidence intervals, no rates presented as population estimates, no extrapolation from corpus performance to expected performance on real deposits.

**Leakage control:** class membership must not be inferable from style, length, or structure. A frozen leakage probe runs before adjudication: a party with no adjudication role attempts to classify bundles by class from surface features alone. Above-chance classification is kill condition `K3`.

### 5.2 Ecological check — deferred by default

Real deposits give realism but cannot give non-circular ground truth (§1.1). A secondary check on real deposits drawn from outside the dos Reis frame is scientifically useful but can only ever report adjudicator *agreement*, never accuracy.

**Decision: deferred out of S2.** Including it would tempt the instance to report an accuracy-shaped number that is actually an agreement number. If an ecological check is run later, it is a separate instance with its own freeze.

---

## 6. Adjudication protocol

**Adjudicators:** two primary, working independently. One reserve, unused unless a primary becomes unavailable; any substitution is disclosed in the results record.

**Blinding:** each adjudicator receives the pinned bundle manifest and the frozen instrument text (§2–§4). Each receives nothing else: not the ground truth, not the item class, not the corpus composition, not the other adjudicator's output, not this section's metrics.

**Disagreement resolution rule, frozen before any disagreement is observed: disagreements are not resolved.** They are recorded, located, and reported. A tie-breaking third adjudicator would convert a measurement of verdict stability into a consensus procedure and destroy the quantity being measured. Recorded disagreement is the result, not a problem with the result.

### 6.1 Metrics, in strict precedence order

**1 — Discrimination (primary).** Per-class accuracy against sealed ground truth, reported separately per class and per parameter. Never pooled into a single accuracy figure: a pooled number is dominated by whichever class is most numerous and hides exactly the failures the classes exist to detect.

**2 — Stability (secondary, conditional).** Verdict agreement between adjudicators, per parameter and per class, with every disagreement enumerated by location. **Reported only if discrimination passes.** If it does not, the agreement number is withheld entirely — not reported with a caveat.

**3 — Determinism (independent).** Same adjudicator, same bytes, re-run. Per P10 determinism proof: rename the output, rerun, the file must be *recreated* byte-identical. Recreation plus identity, not identity alone.

### 6.2 What agreement does not prove — frozen text, to be reproduced verbatim in any S2 output

1. **Agreement is not correctness.** Two adjudicators can agree and both be wrong. Correctness is measured only against ground truth written before the documentary artifact existed.
2. **Agreement is not independent replication.** LLM adjudicators share training-induced priors; agreement may be correlated error from a common source. This is already the project's standing rule and S2 does not relax it.
3. **Agreement is uninformative without demonstrated discriminative power.** An adjudicator returning a constant agrees perfectly with another returning the same constant. This is why discrimination gates stability rather than accompanying it.
4. **Agreement on constructed material does not transfer to real deposits.** No S2 number may be cited as evidence about real deposit documentation.

---

## 7. Kill conditions (frozen)

S2 terminates without an instrument-validated status if any of the following occurs. Termination is a legitimate outcome, not a failure of the instance.

| ID | Condition |
|---|---|
| `K1` | An adjudicator returns `EXPLICIT_DOC`, `EXPLICIT_FILE`, or `INFERABLE` on a `NEG-ABSENT` cell — fabrication. Any occurrence is reported; the frozen tolerance is zero for reporting, and the instrument is marked `DISCRIMINATION_NOT_DEMONSTRATED` if any adjudicator's `NEG-ABSENT` accuracy falls below 90%. |
| `K2` | Determinism fails: a re-run of the same adjudicator on the same bytes produces a non-identical verdict record. |
| `K3` | The leakage probe classifies bundles by class above chance. |
| `K4` | A parameter fails the atomicity test on pre-freeze re-inspection by the gate. |
| `K5` | Reference labels cannot be produced by a party with no construction and no adjudication role (see §11). |

`K5` is the binding constraint on whether S2 can run at all. Under the adjudicator-independence rule, the constructor of an instrument may not produce its reference labels — which disqualifies me from writing the corpus I have just specified.

---

## 8. Exposure ledger (constraints, frozen)

```text
PREDECESSOR_EXPOSURE_ONLY

S1 L0 assets:
- High-Doc control: accessioned in S1
- TRI [72]: accessioned in S1
- KIT [8]: accessioned in S1

These artifacts are not S2 prospective evidence.
They remain in the predecessor repository and are referenced only
to disclose prior exposure.
```

Additional frozen constraints:

- **Chung 2021** (`10.1038/s41597-021-00954-3`) is excluded from S2 in every role — not control material, not corpus template, not worked example.
- **The `E5`/`E6` provenance disclosure** in §3.1 is mandatory in the frozen preregistration.
- **No prospective target of any later confirmatory instance may be inspected** during S2. S2 needs no real deposit; this constraint costs nothing here and preserves the later instance's sampling.
- **The rejected Gemini analytical document** is recorded as `GATE_BLOCKED / NON_GOVERNING / KNOWN_EXPOSURE`. No element of its operational plan enters S2.

---

## 9. Prohibited outputs

S2 may not emit, in any artifact, post, or record:

- a verdict about any real deposit;
- any prevalence figure about documentation quality in the literature;
- a pooled single-number accuracy for the instrument;
- an agreement figure unaccompanied by the §6.2 text;
- an agreement figure at all, if discrimination has not passed;
- any confidence interval or population estimate.

---

## 10. Freeze and execution order

Nothing in stage `F5` or later may begin before every prior stage is committed to `main` by Ivan's merge.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §4 |
| `F2` | Corpus generation spec, item classes, class-assignment design, size |
| `F3` | Adjudication protocol, metrics, kill conditions, metric-computation script |
| `F4` | Role assignments ratified (§11) |
| `F5` | Corpus generated by reference-label party; leakage probe run |
| `F6` | Ground truth sealed by SHA-256 before any adjudicator sees any bundle |
| `F7` | Adjudication executed |
| `F8` | Metrics computed by the `F3` script; determinism proof run |

Preregistration precedes material. No bundle is written before `F2` is merged; no adjudication occurs before `F6` is sealed.

---

## 11. Unresolved L3 decisions

These are decisions, not options I am declining to make. Each requires an authority I do not have.

1. **Who produces the corpus and its reference labels.** Must have no construction role and no adjudication role in S2. I am disqualified as constructor; Sol is disqualified from constructing S2 rules but is not disqualified from corpus authorship, since S2's instrument is not Sol's work — this is a judgement about role separation that only you can make. If no such party exists, `K5` fires and S2 does not run.
2. **Adjudicator identities**, and confirmation that neither has seen this specification's §5, §6.1 or §7.
3. **Whether S2 results are published or held internal.** Bears on whether the corpus must itself be releasable.
4. **Ratification of the 90% `NEG-ABSENT` floor in `K1`.** I set it; a threshold that determines an instrument's fate should not rest solely on its constructor's choice.
5. **Whether the deferral of the ecological check (§5.2) is accepted**, or whether a later dedicated instance is planned now.

---

**Status:** `SPREMNO ZA GEJT`. Constructed by a party with a declared S1 conflict. Not to be gated by its author. §3.1 and §7 `K5` are the two places I would attack first.
