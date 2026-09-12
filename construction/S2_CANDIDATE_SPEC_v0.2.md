# S2 Candidate Specification v0.2 — Deposit Semantics Instrument Validation

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified by operator)
**Supersedes:** `S2_CANDIDATE_SPEC_v0.1.md` (retained unmodified)
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified, not gated
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items are listed in §12 and are not decided here.

---

## 0. Changelog from v0.1

| # | Change | Origin |
|---|---|---|
| 1 | `E4` split to `E4a`/`E4b`, `E8` split to `E8a`/`E8b`. Ten parameters. | Gate finding: v0.1 violated its own atomicity rule, and v0.1 §3.1 claimed a split the v0.1 §3 table had not made. |
| 2 | `INFERABLE` deleted. Five-value vocabulary. | Gate finding: an unbounded inference step reintroduces subjective semantics. |
| 3 | Corpus: 30 bundles, class assigned **per parameter** within a bundle, balanced. | Gate finding: v0.1's "minimum 36" did not follow from its own arithmetic. Constructor finding: bundle-level class assignment made the labels non-independent. |
| 4 | `K1` restated as zero-tolerance, with the bound a pass actually licenses. | Gate finding: "≥90%" at N=5 means zero errors and pretends to precision it lacks. |
| 5 | `K3` made executable: grouped CV by bundle, frozen features, permutation test. | Gate finding: "above chance" was a post-hoc judgement. Second gate finding: CV must be grouped by bundle. Constructor finding: the exact binomial proposed in reply is wrong for the same dependence reason. |
| 6 | `K5` tightened: corpus party must have no S1 and no S2-construction role. | Gate finding: accepted in full. |
| 7 | Unratified items marked. | Operator: only `instrument_validation_only` has been ratified. |

Unchanged from v0.1 and not restated in full: §1.1 (why ground truth precedes the artifact), §2 (documentary space strata), §5.2 (ecological check deferred), §9 (prohibited outputs), §10 (freeze order). Those sections of v0.1 remain the source of truth for their content; §2 and §4 below restate only what changed.

---

## 1. What S2 measures

Unchanged. S2 measures the instrument: whether it discriminates against known ground truth, is stable under adjudicator substitution, and is deterministic on re-run. It touches no real deposit and emits no statement about any dataset.

`PUBLICATION_STATUS` — operator has indicated that a public qualification artifact without a novelty claim is acceptable. **Not yet ratified in verbatim form; recorded here as pending.**

---

## 2. Parameters — ten, atomic

Atomicity rule (unchanged): exactly one interrogative per parameter; vocabulary expressive over every state the question can produce. Scope rule (unchanged): verdicts are emitted per `(unit, parameter, scope)`.

| ID | Interrogative |
|---|---|
| `E1` | For a signed quantity, which sign denotes charge and which denotes discharge? |
| `E2` | What does a zero value in a signal column denote — measured zero, rest, or unrecorded? |
| `E3` | At which boundary does a cumulative quantity reset to zero? |
| `E4a` | Does a reported interval's timestamp denote the interval's start, end, or midpoint? |
| `E4b` | Are interval endpoints inclusive or exclusive? |
| `E5` | What rule governs the interval between logged records? |
| `E6` | By what rule is the absence of unlogged gaps in a record sequence established? |
| `E7` | By what rule does a record map to an operation (cycle, step, test)? |
| `E8a` | In what physical unit is each quantity reported? |
| `E8b` | What scaling, if any, was applied to the reported values? |

The `E5`/`E6` provenance disclosure (v0.1 §3.1) stands and is now supported rather than undercut: the atomicity rule has been applied uniformly and has forced three splits, not one. That is what "uniform application" was supposed to mean, and v0.1 did not deliver it.

`E8a` and `E8b` are expected to resolve at ceiling and are retained as retrieval checks (v0.1 §3.2).

---

## 3. Verdict vocabulary — five values

| Value | Meaning | Evidence required |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | artifact SHA-256, locator, verbatim excerpt |
| `EXPLICIT_FILE` | Located `S-FILE` evidence determines it unambiguously | artifact SHA-256, locator, verbatim excerpt |
| `AMBIGUOUS` | Evidence located; more than one reading survives | all surviving readings, each with its evidence |
| `ABSENT` | Exhaustive traversal of `D` found no determining evidence | traversal record: every manifest entry, marked examined |
| `NOT_APPLICABLE` | The unit contains no data of the kind the parameter governs | located justification |

### 3.1 Why `INFERABLE` is gone, and what it costs

The measurand is whether documentation **determines** an interpretation. An inference step is the adjudicator supplying what the documentation did not. Bounding it would require a frozen whitelist of admissible inferential operations, and that whitelist would itself need validation — which S2 is not dimensioned to provide.

**Declared direction of conservatism, mandatory in every S2 and S3 output:** this instrument will classify as `ABSENT` or `AMBIGUOUS` some cases in which a competent domain expert would reach a unique reading from the documentation. It therefore reports documentation as *less* determinate than a human reader might find it. Any prevalence figure derived from it is an upper bound on non-resolution, not a point estimate.

`[L2]` I judge this trade acceptable because the alternative error — an adjudicator quietly completing the documentation and reporting it as resolved — is the failure that destroyed confidence in the S1 execution record, and it is invisible in the output. The conservative error is visible and stated.

---

## 4. Validation corpus

### 4.1 Design

- **30 bundles.** Each bundle: an article-style excerpt, a README, a CSV header block.
- **Class assigned per parameter within a bundle**, not per bundle. A single bundle carries ten parameter-cells whose classes differ.
- **Balance, per parameter, across the corpus:**

```text
Each parameter:
  30 cells total
  5 cells in each of 6 classes

Across corpus:
  50 cells per class
  300 parameter-cells total
```

- **Adjudications:** 300 cells × 2 adjudicators = **600**, plus 300 for the determinism re-run (§6.1, metric 3) = 900 total adjudication events.
- **Within-bundle class cap:** no bundle may contain more than 3 cells of the same class. This prevents a bundle from acquiring a bundle-level class signature. Satisfied by the generation script and verified mechanically at `F2`; a corpus that cannot satisfy both the column balance and the cap is regenerated, not hand-patched.

### 4.2 Why per-parameter assignment, not per-bundle

Under v0.1's implicit bundle-level assignment, the five labels in a `(parameter, class)` cell came from five different documents, but every label within one document shared that document's generator, style and context. The effective independent unit was the bundle, not the label, and v0.1's arithmetic silently treated 240 labels as 240 units.

Per-parameter assignment fixes both problems at once: it restores the label as the unit of class variation, and it makes bundle-level style structurally unable to predict class — which is the property `K3` then tests empirically rather than assumes.

### 4.3 Item classes

Unchanged from v0.1 §5.1: `POS-EXPLICIT`, `POS-BURIED`, `NEG-ABSENT`, `NEG-ADJACENT`, `AMBIG-CONSTRUCTED`, `NA-CONSTRUCTED`. No real deposit, including Chung, is used as a template.

### 4.4 Statistical scope

Unchanged and reaffirmed: **failure-detection design, not estimation.** No confidence intervals, no rates presented as population estimates, no extrapolation to real deposits. The one bound that may be reported is the one stated in `K1`, and only with its interpretation attached.

---

## 5. Adjudication protocol

Unchanged from v0.1 §6: two primary adjudicators, one disclosed reserve; blinding to ground truth, item class, corpus composition and each other; **disagreements are recorded, never resolved.**

The §6.2 frozen text ("what agreement does not prove") stands verbatim from v0.1 and must be reproduced in any S2 output.

---

## 6. Metrics

### 6.1 Precedence order

1. **Discrimination (primary).** Per-class, per-parameter accuracy against sealed ground truth. Never pooled into a single figure.
2. **Stability (secondary, conditional).** Adjudicator agreement per parameter and per class, every disagreement enumerated by location. **Withheld entirely if discrimination fails** — not reported with a caveat.
3. **Determinism (independent).** Rename output, rerun, file must be *recreated* byte-identical.

---

## 7. Kill conditions — frozen and executable

### `K1` — fabrication

**Zero tolerance, stated literally.** Any `EXPLICIT_DOC` or `EXPLICIT_FILE` verdict on a cell whose sealed ground truth is `NEG-ABSENT` fires `K1`. The permitted count is 0 out of 50 per adjudicator. There is no percentage threshold.

**What a pass licenses, mandatory alongside any report of it:** zero fabrications in 50 trials bounds the per-cell fabrication rate at approximately 5.8% (95%, one-sided; exact value computed by the `F3` script, not by this approximation). A pass does not establish that the instrument does not fabricate. It establishes that it did not fabricate 50 times.

### `K2` — determinism

A re-run of the same adjudicator on the same bytes produces a non-identical verdict record.

### `K3` — corpus leakage

Executable decision rule, frozen at `F2`/`F3`:

```text
K3 PROBE TASK:
  predict the class of each (bundle, parameter) cell from
  frozen surface features only

FEATURES (frozen at F2, no additions after):
  bundle-level document surface statistics (length, section
  count, token distribution, formatting markers) + parameter ID

CV UNIT:
  bundle

  All parameter-cells from the same bundle MUST remain in the
  same fold.

  5 folds x 6 bundles/fold = 30 bundles = 300 parameter-cells

NULL:
  no association between surface features and class
  (marginal class distribution is uniform, p0 = 1/6, by the
  balanced design of §4.1)

TEST:
  permutation test, 2000 permutations, frozen seed.
  Permutation unit: the bundle's whole 10-cell class-assignment
  vector, permuted across bundles. Cell-level permutation is
  PROHIBITED.

FIRES IF:
  one-sided permutation p < 0.01
```

**Constructor correction, raised against my own prior reply.** I previously proposed an exact binomial test against `p0 = 1/6` over 300 cells. That is wrong for exactly the reason the grouped-CV requirement is right: cells within a bundle are not independent, so under the null a classifier that assigns one class to a whole bundle produces correlated errors, the binomial variance is understated, and the test is anti-conservative — it would fire on noise. Accepting grouped CV while keeping a cell-level binomial would have fixed the training leak and left the inference leak in place. The permutation test respects the same grouping in both halves.

**On using parameter ID as a feature.** Admissible **only because** §4.1 balances classes within every parameter, making the marginal class distribution uniform for each parameter ID. If the balance constraint is ever relaxed, parameter ID must be dropped from the feature set, or the probe will learn the class-by-parameter distribution and report it as stylistic leakage. This dependency is frozen: the `F2` verification script checks the balance and refuses to emit the corpus if it fails.

### `K4` — atomicity

A parameter fails the one-interrogative test on pre-freeze re-inspection by the gate. v0.1 failed this on two parameters; the gate should assume v0.2 may still fail it on one.

### `K5` — independence of the reference-label party

The corpus and its ground truth cannot be produced by a party with no S1 role **and** no S2-construction role.

Tightened per operator's cut: **not Sol.** The required configuration is four separated parties — constructor (defines the generation protocol), corpus/reference-label party (new, selects and seals ground truth, generates bundles under frozen rules), two blind adjudicators, and a gate party (new). If this cannot be staffed, `K5` fires and S2 does not run. That is the correct outcome, not an argument for relaxing the rule.

`K5` is a **resourcing** condition, not a specification defect. Specification defects are mine to fix; this one is not.

---

## 8. Exposure ledger

Unchanged from v0.1 §8, including the verbatim `PREDECESSOR_EXPOSURE_ONLY` block, the total exclusion of Chung, and the `GATE_BLOCKED / NON_GOVERNING / KNOWN_EXPOSURE` record for the rejected analytical document.

Added: the BatteryLake manifest review, if ratified, is recorded as `PRIOR_ART_EXPOSURE` under `PRIOR_ART_ELIMINATION_v0.2.md` §4.3, and cannot be cited as S2 data.

---

## 9. Prohibited outputs

Unchanged from v0.1 §9. Added:

- No claim that the S2 architecture is methodologically novel. See `PRIOR_ART_ELIMINATION_v0.2.md` §2.2.
- No prevalence figure presented as a point estimate rather than an upper bound (§3.1).

---

## 10. Freeze and execution order

Unchanged from v0.1 §10 (`F1`–`F8`), with two additions inside existing stages:

- `F2` additionally freezes: the class-assignment design, the within-bundle cap, the `K3` feature set, and the balance-verification script.
- `F3` additionally freezes: the `K3` permutation seed and test script, and the exact `K1` bound computation.

---

## 11. Items not ratified

Recorded so that no downstream document treats them as settled. Only `instrument_validation_only` has been ratified by the operator in verbatim form.

| Item | State |
|---|---|
| Public qualification artifact without novelty claim | Indicated, not ratified verbatim |
| BatteryLake manifest review | Pending L3 |
| 30-bundle / 600-adjudication budget | Pending L3 |
| S3 frame (dos Reis vs BatteryLake registry) | Deferred |
| Paywalled / non-English sweep | Pending L3 |
| `K5` party assignments | Pending L3, and binding on whether S2 runs |

---

## 12. L3 decisions

1. Staffing for the four separated parties (`K5`).
2. Corpus budget: 30 bundles as derived, or a reduced qualification.
3. Publication status of the qualification artifact, in verbatim form.
4. BatteryLake manifest review (see `PRIOR_ART_ELIMINATION_v0.2.md` §6).
5. Paywalled sweep.

---

**Status:** `SPREMNO ZA GEJT`. Written by a constructor with a declared S1 conflict, whose v0.1 failed its own atomicity rule on two parameters and whose first corpus arithmetic did not follow from its own premises. A gate should assume a third such error remains and should start with §4.1's balance-and-cap feasibility and §7 `K3`'s feature set.
