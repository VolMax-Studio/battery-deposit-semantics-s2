# S2 Candidate Specification v0.3 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** `S2_CANDIDATE_SPEC_v0.1.md`, `S2_CANDIDATE_SPEC_v0.2.md` — both retained as history, **neither is normative**. This document is self-contained. No section of any earlier version is a source of truth for anything here.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`, not by this document
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items listed in §13.

---

## 0. Changelog from v0.2

| # | Change | Origin |
|---|---|---|
| B1 | `QUALIFIED` decision function added (§8). Frozen per-class thresholds, stability floor. | Gate: no function mapped results to a verdict. |
| B2 | `semantic_value` added to the output schema and to scoring (§5, §6). | Gate: the enum records evidence type, not the answer. An adjudicator could misread the fact and still score correct. |
| B3 | The "≈5.8% upper bound" deleted entirely. | Gate: the 50 cells are clustered; I invoked cluster dependence for `K3` and ignored it for `K1` in the same document. |
| B4 | `K3` fully specified: classifier, hyperparameters, exact feature list, preprocessing, fold rule, statistic, permutation procedure (§9.3). | Gate: "frozen surface features" was a description, not a list. |
| B5 | Corpus generated **deterministically from sealed ground truth** by a frozen template engine, with a mechanical fidelity re-derivation (§4.4). | Gate: label-before-artifact fixes circularity, not generator error. |
| B6 | Freeze order corrected: truth sealed **before** generation, probe after (§11). | Gate: `F5`/`F6` were inverted and `K3` used labels before they were sealed. |
| — | `EXPLICIT_FILE` narrowed: declared labels only; **value patterns excluded** (§5.2). | Gate: value-pattern evidence reintroduced the inference `INFERABLE` was deleted to remove. |
| — | `E2` narrowed to numeric encoding; operational-state semantics folded into `E7` (§3). | Gate: "measured zero, rest, unrecorded" are not mutually exclusive. |
| — | Determinism re-run applies to **both** adjudicators; canonical serializer specified (§7.3). | Gate: 900 vs 1200 ambiguity; byte-identity meaningless without canonical form. |
| — | `K5` party count corrected to five (six with independent reserve) (§9.5). | Gate: "four separated parties" then listed five. |
| — | "Upper bound on non-resolution" claim deleted, replaced with the gate's wording (§5.3). | Gate: not proven; errors run in both directions. |
| — | §4.2 "structurally unable to predict class" softened. | Gate: overclaim; that is what `K3` exists to test. |
| — | Ecological-transfer limitation declared (§12.2). | Constructor: not raised by the gate. |

---

## 1. What S2 measures

> Does the deposit-semantics adjudication instrument produce verdicts that are discriminating against known ground truth, stable under adjudicator substitution, and deterministic on re-run?

S2 measures the instrument. It touches no real deposit; its corpus is constructed. It emits no statement about any dataset, no prevalence figure, and no methodological novelty claim.

**Why the corpus is constructed.** An adjudication instrument cannot be validated on material whose labels are themselves produced by adjudication — that measures agreement between two applications of the same unproven procedure. Ground truth is therefore written before the documentary artifact. This is an established paradigm, not a contribution; see `PRIOR_ART_ELIMINATION_v0.2.md`.

---

## 2. Documentary space

For each unit, `D` is an exhaustive, ordered manifest. Each entry carries: generation ID, generation timestamp, SHA-256, media type, stratum tag.

| Stratum | Contents | Proposition it can support |
|---|---|---|
| `S-DOC` | Article-style text, README, data dictionary, declared prose | *The depositor stated a rule.* |
| `S-FILE` | Declared in-file labels: column names, header rows, declared unit strings, explicit legend or comment lines | *The file declares a property.* |

The instrument **does not rank the strata**. It records which stratum carried the verdict. Ranking would be a finding about what counts as adequate documentation, not an assumption to freeze.

---

## 3. Parameters — ten, atomic

**Atomicity rule (frozen):** exactly one interrogative; verdict vocabulary expressive over every state that interrogative can produce; the answer options must be mutually exclusive and exhaustive.

**Scope rule (frozen):** verdicts are emitted per `(unit, parameter, scope)`, where scope is the declared set of columns or signals governed.

| ID | Interrogative | Answer space |
|---|---|---|
| `E1` | For a signed quantity, which sign denotes charge and which denotes discharge? | `positive=charge` / `positive=discharge` |
| `E2` | Does a zero in a signal column denote a measured value or a placeholder for an unrecorded value? | `measured` / `placeholder` |
| `E3` | At which boundary does a cumulative quantity reset to zero? | `step` / `cycle` / `test` / `never` |
| `E4a` | Does a reported interval's timestamp denote the interval's start, end, or midpoint? | `start` / `end` / `midpoint` |
| `E4b` | Are interval endpoints inclusive or exclusive? | `inclusive` / `exclusive` / `half-open` |
| `E5` | What rule governs the interval between logged records? | free value (e.g. `fixed 10 s`, `event-driven on ΔV`) |
| `E6` | By what rule is the absence of unlogged gaps established? | free value |
| `E7` | By what rule does a record map to an operation, including how operational state (charge / discharge / rest) is encoded? | free value |
| `E8a` | In what physical unit is each quantity reported? | free value |
| `E8b` | What scaling, if any, was applied? | free value |

**On `E2`.** v0.2 offered "measured zero, rest, or unrecorded" — not mutually exclusive, since a rest interval can carry a genuinely measured zero current. That was two questions: numeric encoding, and operational state. `E2` now asks only the encoding question. Operational-state encoding belongs with record-to-operation association and is folded into `E7`'s single interrogative.

**On `E5`/`E6` provenance.** The cadence / coverage-verification distinction was first named by the S1 reviewer after the S1 outcome was known, and that reviewer is this document's author. It is retained here because the atomicity rule, applied uniformly, forces three splits — `E2`/`E7`, `E4a`/`E4b`, `E8a`/`E8b` — not one. Both facts must appear in the frozen preregistration.

---

## 4. Corpus

### 4.1 Design

- **30 bundles.** Each: an article-style excerpt, a README, a CSV header block.
- **Class assigned per parameter within a bundle**, not per bundle.

```text
Each parameter:
  30 cells total
  5 cells in each of 6 classes

Across corpus:
  50 cells per class
  300 parameter-cells total

Adjudications:
  300 cells x 2 adjudicators             = 600 primary
  300 cells x 2 adjudicators (re-run)    = 600 determinism
                                           1200 total
```

- **Within-bundle cap:** no bundle may contain more than 3 cells of the same class. Column balance and row cap are jointly satisfied by the generator and verified mechanically at `F4`; a corpus failing either is regenerated, never hand-patched.

### 4.2 Why per-parameter assignment

Under bundle-level assignment, five labels in a `(parameter, class)` cell came from five documents, but every label within one document shared that document's generator, style and context — the effective independent unit was the bundle, and earlier arithmetic treated labels as units.

Per-parameter assignment restores the label as the unit of class variation and **removes the direct bundle-level class assignment**. It does not guarantee the absence of other correlations between document surface and class; that is precisely what `K3` tests.

### 4.3 Item classes

| Class | Construction | Failure it detects |
|---|---|---|
| `POS-EXPLICIT` | Fact stated plainly and prominently | Cannot apply the standard to clear text |
| `POS-BURIED` | Fact stated, in a non-obvious location | Retrieval failure → false `ABSENT` |
| `NEG-ABSENT` | Fact present nowhere in `D` | Fabrication |
| `NEG-ADJACENT` | A related but non-determining statement present | Accepting a neighbouring fact as the asked-for fact |
| `AMBIG-CONSTRUCTED` | Two incompatible statements present | Picking one reading instead of `AMBIGUOUS` |
| `NA-CONSTRUCTED` | No data of the governed kind | Forcing a verdict where none applies |

No real deposit, including Chung 2021, is used as template or inspiration.

### 4.4 Generation fidelity

Label-before-artifact removes circularity but not generator error: a hand-written bundle can fail to realize its own label.

**Bundles are therefore generated, not written.** A frozen template engine instantiates each cell from a **sentence bank** keyed by `(parameter, class, semantic_value)`, with placement (prominent / buried / absent) controlled by frozen placement rules and a frozen seed. The generator emits a realization index recording which bank entry realized which cell.

**Fidelity check (mechanical, 100%, not sampled):** a checker party re-derives the ground-truth record from the generated bundle plus the realization index, and the re-derived record must match the sealed record byte-identically. Any mismatch halts at `F4`.

`[L2]` Declared tension: a sentence bank raises fidelity and lowers stylistic variety, which raises leakage risk. These pull against each other and `K3` is the arbiter. If `K3` fires because the bank is too templated, the correct response is a larger bank and full regeneration — never selective editing of the bundles the probe found.

---

## 5. Verdict vocabulary and output schema

### 5.1 Output record

Every adjudication emits exactly:

```text
parameter_id
scope
semantic_value        # null for ABSENT and NOT_APPLICABLE
verdict_class
evidence_stratum      # S-DOC | S-FILE | null
artifact_sha256
locator
verbatim_excerpt
traversal_record      # required when ABSENT
```

Example:

```text
E1
scope: Current(A)
semantic_value: positive=discharge
verdict_class: EXPLICIT_DOC
evidence_stratum: S-DOC
```

### 5.2 Verdict classes

| Value | Meaning | Evidence required |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | SHA-256, locator, verbatim excerpt |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | SHA-256, locator, verbatim excerpt |
| `AMBIGUOUS` | Evidence located; more than one reading survives | all surviving readings with evidence |
| `ABSENT` | Exhaustive traversal found no determining evidence | traversal record, every manifest entry marked |
| `NOT_APPLICABLE` | No data of the governed kind | located justification |

**`EXPLICIT_FILE` is narrow, by frozen definition.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines — text the file *declares*. **Inadmissible: value patterns.** Deriving a sign convention from the relationship between current sign and a state-of-charge trend is domain inference, not a declaration, and admitting it would restore through `S-FILE` exactly the inference deleted with `INFERABLE`.

This is also the sharpest point of difference from the published prior art, which permits value statistics to bind columns and resolves conventions by physical plausibility. That difference is deliberate and is the reason the two instruments answer different questions.

### 5.3 Declared direction of conservatism

The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. This sentence is frozen and must be reproduced in any S2 or S3 output that reports a non-resolution figure.

---

## 6. Scoring

A cell is **correct** only if `verdict_class` **and** `semantic_value` both match the sealed record. For `ABSENT` and `NOT_APPLICABLE`, `semantic_value` is null in both records and the class match alone decides.

Errors are recorded by direction, not only by count:

- **Over-claim:** instrument asserts determinacy the documentation does not support (`NEG-ABSENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`; `NEG-ADJACENT` → `EXPLICIT_*`).
- **Under-claim:** instrument fails to find or accept determinacy that exists (`POS-*` → `ABSENT` or `AMBIGUOUS`).
- **Value error:** correct `verdict_class`, wrong `semantic_value`. Scored as incorrect and reported separately, because it is invisible to any class-only metric.

Both directions matter, differently. Over-claim corrupts instrument integrity. **Under-claim is the direction that inflates the S3 headline**, since S3's expected finding is that documentation is missing — an instrument that fails to find stated facts manufactures exactly the result we would want to be true. §8 weights accordingly.

---

## 7. Adjudication protocol

### 7.1 Channels

Two primary adjudicators working independently; one reserve, unused unless a primary becomes unavailable, with any substitution disclosed.

**Blinding:** each receives the pinned bundle manifest and the frozen §2–§6 text. Each receives nothing else — not ground truth, not item class, not the realization index, not corpus composition, not the other's output, not §8 or §9.

### 7.2 Disagreement

**Frozen before any disagreement is observed: disagreements are not resolved.** They are recorded and located. A tie-breaking third adjudicator would convert a measurement of verdict stability into a consensus procedure and destroy the quantity being measured.

### 7.3 Determinism

**Both** adjudicators re-run all 300 cells. Determinism of one says nothing about the other, and the two channels exist because they may differ.

Byte-identity requires a canonical form, or the test measures formatting. Frozen:

- canonical serializer: fixed field order, fixed encoding, no timestamps, no run IDs, no model-version strings inside the verdict record;
- model identity, version, and sampling settings (temperature, seed, max tokens) frozen at `F3` and recorded in a **sidecar**, never in the record;
- proof procedure: rename the output, re-run, the file must be **recreated** byte-identical. Recreation plus identity, not identity alone.

### 7.4 What agreement does not prove — frozen text, reproduced verbatim in any S2 output

1. **Agreement is not correctness.** Two adjudicators can agree and both be wrong. Correctness is measured only against ground truth written before the documentary artifact existed.
2. **Agreement is not independent replication.** LLM adjudicators share training-induced priors; agreement may be correlated error from a common source.
3. **Agreement is uninformative without demonstrated discriminative power.** An adjudicator returning a constant agrees perfectly with another returning the same constant.
4. **Agreement on constructed material does not transfer to real deposits.** No S2 figure may be cited as evidence about real deposit documentation.
5. **High agreement is not a goal.** Agreement materially above what per-adjudicator accuracy predicts under independent errors is evidence of correlated behaviour, and is reported as such.

---

## 8. Qualification decision function

The instrument is `QUALIFIED` if and only if every condition below holds. Any failure yields `NOT_QUALIFIED`, with the failing condition named. There is no partial qualification and no remediation-and-retest without a new freeze.

### 8.1 Discrimination

Evaluated **per class across all parameters** (50 cells per class per adjudicator), because 5 cells per `(parameter, class)` cannot carry a threshold. Per-parameter results are computed and reported for **diagnosis only** and carry no pass/fail weight.

Both adjudicators must independently satisfy:

| Class | Minimum correct (of 50) | Reason for this level |
|---|---|---|
| `POS-EXPLICIT` | 49 | Ceiling check. A miss here is a defect, not a hard case. |
| `POS-BURIED` | 45 | Retrieval. Above ~10% false-`ABSENT`, instrument error becomes comparable to the effect sizes S3 would report, and the headline would be partly our own search failure. |
| `NEG-ABSENT` | 50, with **zero** over-claims (`K1`) | Fabrication is not traded off against anything. |
| `NEG-ADJACENT` | 45 | Same tolerance as retrieval, opposite direction. |
| `AMBIG-CONSTRUCTED` | 40 | Genuinely the hardest class; a lower bar is honest, and failures here are reported by direction. |
| `NA-CONSTRUCTED` | 45 | Applicability judgement. |

**These six numbers are the constructor's judgement about tolerable contamination of a future measurement. They are not statistical guarantees and not derived from any distribution.** They are listed in §13 for ratification, on the same principle by which `K1`'s threshold was sent back.

### 8.2 Stability

Cell-level agreement between the two primary adjudicators on `(verdict_class, semantic_value)` jointly must be **≥ 240 of 300 (80%)**.

Below that floor, S3 verdicts would be adjudicator-dependent artifacts rather than instrument outputs.

Agreement is **not** maximized. The observed agreement is additionally compared against the value predicted from the two measured accuracies under independent errors, and the comparison is reported descriptively. A large positive excess is evidence of correlated behaviour and is reported, but does not itself fail qualification — it qualifies how much the two channels are worth.

Stability is computed and reported **only if** §8.1 passes for both adjudicators. If §8.1 fails, the agreement figure is withheld entirely, not reported with a caveat.

### 8.3 Full condition table

```text
DISCRIMINATION   §8.1 thresholds met by BOTH adjudicators
FABRICATION      K1  — zero over-claims on NEG-ABSENT, both adjudicators
STABILITY        §8.2 floor met (computed only if DISCRIMINATION passes)
DETERMINISM      K2  — both adjudicators, canonical form, recreation proof
LEAKAGE          K3  — probe does not fire
ATOMICITY        K4  — all ten parameters pass pre-freeze re-inspection
FIDELITY         §4.4 — 100% mechanical re-derivation match
STAFFING         K5  — five separated parties staffed
```

---

## 9. Kill conditions

### `K1` — fabrication
Any `EXPLICIT_DOC` or `EXPLICIT_FILE` verdict on a cell whose sealed truth is `NEG-ABSENT`. Permitted count: **0 of 50 per adjudicator.** No percentage threshold, and **no rate bound is reported** — the 50 cells share bundles, parameters and a single adjudicator, so they are not independent trials and any Bernoulli bound computed from them would be unjustified.

### `K2` — determinism
Any re-run producing a non-identical canonical verdict record, for either adjudicator.

### `K3` — corpus leakage

Fully specified, frozen at `F3`:

```text
TASK
  predict the class of each (bundle, parameter) cell

CLASSIFIER
  multinomial logistic regression, L2, C = 1.0,
  scikit-learn, version pinned in F3, max_iter = 1000
  (A simple frozen probe is used deliberately: a tuned strong
   learner would introduce researcher degrees of freedom. A
   negative result therefore means "no leakage detectable by
   THIS probe", not "no leakage".)

FEATURES  (49 total, computed by the frozen F3 script)
  bundle-level, per component (article / README / CSV header):
    character count                                    3
    line count                                         3
    digit-to-character ratio                           3
    punctuation count                                  3
  bundle-level, other:
    article section-heading count                      1
    README section count                               1
    CSV header column count                            1
    mean sentence length (article, README)             2
    type-token ratio (article, README)                 2
      tokenization: whitespace, lowercased, no stemming
    frozen formatting-marker presence flags           20
  cell-level:
    parameter ID, one-hot                             10

PREPROCESSING
  numeric features standardized using training-fold
  statistics only; no imputation (all features defined)

FOLD ASSIGNMENT
  unit = bundle. All 10 cells of a bundle stay in one fold.
  bundles sorted by bundle ID; fold = index mod 5
  5 folds x 6 bundles = 30 bundles = 300 cells
  deterministic; no shuffling

NULL
  no association between surface features and class.
  p0 = 1/6, guaranteed uniform by the §4.1 balance

STATISTIC
  mean cross-validated multiclass accuracy over the 300
  held-out cell predictions

TEST
  permutation test, 2000 permutations, seed 20260912.
  Permutation unit: the bundle's whole 10-cell class-assignment
  vector, permuted across bundles. Full CV re-run per
  permutation. Cell-level permutation is PROHIBITED.

FIRES IF
  one-sided permutation p < 0.01
```

**On `parameter ID` as a feature.** Admissible **only because** §4.1 balances classes within every parameter, making the marginal class distribution uniform per parameter ID. If that balance is ever relaxed, parameter ID must be dropped or the probe learns the class-by-parameter distribution and reports it as stylistic leakage. The `F4` verification script checks the balance and refuses to emit the corpus if it fails.

**On the statistic.** A cell-level exact binomial against `p0 = 1/6` would be wrong here for the same reason cell-level CV would be: under the null, a probe assigning one class to a whole bundle produces correlated errors, understating variance and firing on noise. The permutation respects the same grouping in both halves.

### `K4` — atomicity
Any parameter fails the one-interrogative / mutually-exclusive-answers test on pre-freeze re-inspection by the gate. v0.1 failed this on two parameters and v0.2 on one; the gate should assume v0.3 fails on at least one.

### `K5` — party independence

**Five separated parties** (six if the reserve adjudicator must also be independent):

1. **Constructor** — defines the generation protocol, instrument, and this document. No adjudication, no gate, no corpus authorship.
2. **Corpus / reference-label party** — new. No S1 role and no S2-construction role. Authors and seals ground truth, builds the sentence bank, runs the generator.
3. **Fidelity checker** — may be the gate party or a separate one, but not the corpus party. Runs the §4.4 re-derivation.
4. **Adjudicator A** — blind.
5. **Adjudicator B** — blind, independent of A.
6. **Gate party** — new. No S1 role, no S2-construction role.

Explicitly excluded from parties 2–6: Fable (constructor), Sol (S1 instrument, sampling, calibration and decision-rule construction), and any agent that materially encoded S1 classifier logic.

`K5` fires if this cannot be staffed. **That is the correct outcome, not an argument for relaxing the rule.** `K5` is a resourcing condition, not a specification defect.

---

## 10. Exposure ledger

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

- Chung 2021 (`10.1038/s41597-021-00954-3`) excluded from S2 in every role.
- The `E5`/`E6` and `E2`/`E7` provenance disclosures of §3 are mandatory in the frozen preregistration.
- No prospective target of any later instance may be inspected during S2. S2 needs no real deposit.
- The rejected agent analytical document stands as `GATE_BLOCKED / NON_GOVERNING / KNOWN_EXPOSURE`.
- A BatteryLake manifest review, if ratified, is recorded as `PRIOR_ART_EXPOSURE` under `PRIOR_ART_ELIMINATION_v0.2.md` §4.3 and may not be cited as S2 data.

---

## 11. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §5, §6 |
| `F2` | Corpus design: class-assignment design, within-bundle cap, item classes, sentence-bank schema, placement rules, generator and balance-verification scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — including the `K3` script, feature list, permutation seed, and the frozen model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | **Ground-truth record authored and sealed** (SHA-256) by the corpus party |
| `F6` | Bundles generated deterministically from the sealed truth; fidelity re-derivation must match byte-identically; balance and cap verified |
| `F7` | Leakage probe `K3` |
| `F8` | Adjudication, both channels |
| `F9` | Determinism re-run, both channels; metrics computed by the `F3` script; `§8` decision function applied |

The v0.2 order inverted `F5`/`F6` and ran the probe against labels that were not yet sealed, leaving room for regeneration after seeing the probe. Sealing now precedes generation because the bundles are generated *from* the truth.

---

## 12. Declared limitations

### 12.1 Statistical scope
Failure-detection design, not estimation. No confidence intervals, no rates presented as population estimates, no extrapolation from corpus performance to real deposits. No rate bound is derived from `K1`.

### 12.2 Ecological transfer — raised by the constructor, not by the gate

The corpus is template-generated from a sentence bank. Real deposits are longer, messier, and state facts in prose no bank contains, spread across sections in ways no placement rule models. **Qualification on this corpus may therefore be a test of template recognition rather than of reading real documentation.**

Consequence, frozen: **a `QUALIFIED` result does not license S3.** It prevents S3 from beginning with a demonstrably broken instrument, which is all it does. Closing the ecological gap requires a separate step, on real material, with its own freeze, and that step is not specified here and is not part of S2.

### 12.3 Prohibited outputs
- No verdict about any real deposit.
- No prevalence figure about documentation quality in any literature.
- No pooled single-number accuracy.
- No agreement figure unless §8.1 passes.
- No confidence interval or population estimate.
- No claim that the S2 architecture is methodologically novel.
- No non-resolution figure without the §5.3 frozen sentence attached.

---

## 13. L3 decisions

1. **Ratify or revise the six discrimination thresholds in §8.1** and the 80% stability floor in §8.2. These are constructor judgements and should not rest solely on the constructor's choice, by the same principle applied to `K1`.
2. **Staffing of the five (or six) separated parties** — `K5`, binding on whether S2 runs at all.
3. **Corpus budget**: 30 bundles / 1200 adjudication events as derived, or a reduced qualification.
4. **Publication status** of the qualification artifact, in verbatim form.
5. **BatteryLake manifest review** — see `PRIOR_ART_ELIMINATION_v0.2.md` §6.
6. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`. Self-contained; no earlier version is normative. Written by a constructor with a declared S1 conflict, whose v0.1 failed its own atomicity rule on two parameters, whose v0.2 failed it on one and carried a statistical claim it had itself just ruled out elsewhere in the same document. A gate should start at §8.1, where six unratified numbers do the most work, and at §4.4, where the fidelity claim rests on a generator that does not yet exist.
