# S2 Candidate Specification v0.4 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** v0.1, v0.2, v0.3 — retained as history, **none normative**. This document is self-contained.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items in §13.

---

## 0. Changelog from v0.3

| # | Change |
|---|---|
| B7 | `E7` split into `E7a`/`E7b`. `E4b` answer space encodes orientation. `E3` interrogative asks for the **finest** reset boundary. **Eleven parameters.** All corpus arithmetic re-derived (§3, §4). |
| B8 | Every parameter's `semantic_value` is a **frozen closed enum or typed field**; no free text is scored. `AMBIGUOUS` gets a multi-reading schema with canonical ordering (§5). |
| B9 | Qualification is **scoped per parameter**, with a parameter-level floor and a dead-cell rule. Class-level aggregation can no longer hide a dead parameter (§8). |
| B10 | Fidelity check verifies **emitted bundle bytes** against the sentence bank. The realization index is a cross-check, never the authority (§4.4). |
| F1 | `K1` fabrication redefined: `AMBIGUOUS` on `NEG-ABSENT` is fabrication. Added mechanical `EVIDENCE_INVALID` check on every verdict (§6.3, §9.1). |
| F2 | The independence-model comparator is **removed**. Replaced with a model-free joint error decomposition (§8.4). |
| F3 | Twenty formatting markers enumerated; exact permutation p-value formula frozen (§9.3). |
| F4 | The `POS-BURIED` rationale no longer appeals to unknown future S3 effect sizes (§8.2). |

Consequence the gate must re-check: feasibility of column balance plus row cap was verified for a 30×10 design. The design is now **30×11**. That verification does not carry over.

---

## 1. What S2 measures

> Does the deposit-semantics adjudication instrument produce verdicts that are discriminating against known ground truth, stable under adjudicator substitution, and deterministic on re-run — **and for which parameters**?

S2 measures the instrument. It touches no real deposit. It emits no statement about any dataset, no prevalence figure, no methodological novelty claim.

Ground truth is written before the documentary artifact, because an adjudication instrument cannot be validated on labels produced by adjudication. This is an established paradigm, not a contribution.

---

## 2. Documentary space

`D` is an exhaustive ordered manifest per unit; each entry carries generation ID, timestamp, SHA-256, media type, stratum tag.

| Stratum | Contents | Proposition it supports |
|---|---|---|
| `S-DOC` | Article-style text, README, data dictionary, declared prose | *The depositor stated a rule.* |
| `S-FILE` | Declared in-file labels: column names, header rows, declared unit strings, explicit legend or comment lines | *The file declares a property.* |

Strata are **not ranked**. The verdict records which stratum carried it.

---

## 3. Parameters — eleven, atomic

**Atomicity rule (frozen):** exactly one interrogative; answer space mutually exclusive and exhaustive; vocabulary expressive over every state the interrogative can produce.

**Scope rule (frozen):** verdicts are emitted per `(unit, parameter, scope)`.

| ID | Interrogative | Canonical answer space |
|---|---|---|
| `E1` | For a signed quantity, which sign denotes charge? | `charge_positive` \| `discharge_positive` |
| `E2` | Does a zero in a signal column denote a measured value or a placeholder for an unrecorded value? | `measured` \| `placeholder` |
| `E3` | What is the **finest** operational boundary at which a cumulative quantity resets to zero? | `step` \| `cycle` \| `test` \| `never` |
| `E4a` | Does a reported interval's timestamp denote start, end, or midpoint? | `start` \| `end` \| `midpoint` |
| `E4b` | Which endpoint convention governs reported intervals? | `closed_closed` \| `open_open` \| `closed_open` \| `open_closed` |
| `E5` | What rule governs the interval between logged records? | `{cadence_mode, interval_seconds, trigger}` — see §5.2 |
| `E6` | By what rule is the absence of unlogged gaps established? | `completeness_counter` \| `expected_count_comparison` \| `gap_flag_column` \| `acquisition_log_reconciliation` |
| `E7a` | By what rule does a record map to an operation identifier (step / cycle / test index)? | `explicit_index_column` \| `filename_encoding` \| `time_segmentation_rule` \| `row_grouping_marker` |
| `E7b` | By what rule is operational state (charge / discharge / rest) encoded in a record? | `step_type_column` \| `current_sign` \| `separate_state_column` \| `mode_code_enum` |
| `E8a` | In what physical unit is each quantity reported? | frozen unit enum (§5.2) |
| `E8b` | What scaling, if any, was applied? | `{scaling, factor_value}` — see §5.2 |

**`E3`.** v0.3 asked "at which boundary does it reset", whose answers are hierarchical and therefore not exclusive: a quantity resetting at every step also resets at the step beginning a cycle. "Finest" makes exactly one answer true.

**`E7`.** v0.3 asked for the record-to-operation rule "including how operational state is encoded" — two propositions, either of which can be documented while the other is absent. This is the P5 defect reintroduced, and it is why `K4` still fired. Split.

**`E4b`.** `half-open` collapsed `[start, end)` and `(start, end]`, which are different rules, into one gold value.

**Provenance disclosure, mandatory in the frozen preregistration.** The cadence / coverage distinction (`E5`/`E6`) was first named by the S1 reviewer after the S1 outcome was known, and that reviewer authored this document. It is retained because uniform application of the atomicity rule has now forced four splits — `E2`/`E7b`, `E4a`/`E4b`, `E7a`/`E7b`, `E8a`/`E8b` — not one.

---

## 4. Corpus

### 4.1 Design

```text
30 bundles x 11 parameters      = 330 parameter-cells

Each parameter:
  30 cells, 5 in each of 6 classes

Across corpus:
  55 cells per class
  330 cells total

Adjudications:
  330 x 2 adjudicators           = 660 primary
  330 x 2 (determinism re-run)   = 660
                                   1320 total
```

- Class assigned **per parameter within a bundle**, not per bundle.
- **Within-bundle cap:** no bundle may contain more than 3 cells of the same class (11 cells, 6 classes).
- Column balance and row cap are satisfied by the generator and verified mechanically at `F6`. A corpus failing either is regenerated, never hand-patched. **Joint feasibility at 30×11 is asserted, not demonstrated, and is a gate item.**

### 4.2 Why per-parameter assignment

Bundle-level assignment would make the bundle the effective independent unit while the arithmetic counted labels. Per-parameter assignment restores the label as the unit of class variation and **removes the direct bundle-level class assignment**. It does not guarantee the absence of other surface-to-class correlations; that is what `K3` tests.

### 4.3 Item classes

| Class | Construction | Failure it detects |
|---|---|---|
| `POS-EXPLICIT` | Fact stated plainly and prominently | Cannot apply the standard to clear text |
| `POS-BURIED` | Fact stated, in a non-obvious location | Retrieval failure → false `ABSENT` |
| `NEG-ABSENT` | No determining statement anywhere in `D` | Fabrication |
| `NEG-ADJACENT` | A related but non-determining statement present | Accepting a neighbour as the asked-for fact |
| `AMBIG-CONSTRUCTED` | Two incompatible determining statements present | Picking one reading instead of `AMBIGUOUS` |
| `NA-CONSTRUCTED` | No data of the governed kind | Forcing a verdict where none applies |

No real deposit, including Chung 2021, is used as template or inspiration.

### 4.4 Generation and fidelity

Bundles are **generated, not written.** A frozen template engine instantiates each cell by inserting an entry from a frozen **sentence bank** keyed by `(parameter, class, semantic_value)`, **verbatim — the generator may not paraphrase a bank entry.** Placement (prominent / buried / absent) follows frozen placement rules under a frozen seed. The generator emits a realization index.

**Fidelity check — byte-level, 100%, no sampling.** The checker receives the generated bundle bytes and the sentence bank. It does **not** receive the realization index as an authority.

1. Search the bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences found and their locations.
3. The derived record must equal the sealed record byte-identically.
4. For every `NEG-ABSENT` cell, verify mechanically that **no** determining bank entry for that parameter — of any `semantic_value` — occurs anywhere in the bundle bytes. Absence is established by exhaustive search over the bank, never by reading the index.
5. For every `NEG-ADJACENT` cell, verify that the present entry comes from the non-determining bank and that no determining entry for that parameter occurs.
6. The realization index is compared as a cross-check only. **Index–bytes disagreement halts at `F6`.**

v0.3 let the checker re-derive truth "from the bundle plus the realization index", which proves only that the generator's own bookkeeping agrees with the sealed record. That is a receipt, not an artifact check.

`[L2]` Declared tension, now stronger: verbatim insertion raises fidelity and lowers stylistic variety, raising leakage risk. `K3` is the arbiter. If `K3` fires because the bank is too templated, the response is a larger bank and full regeneration — never selective editing of the bundles the probe found.

---

## 5. Output schema and verdict vocabulary

### 5.1 Record

```text
parameter_id
scope
verdict_class
readings: [                    # 1 for EXPLICIT_*, >=2 for AMBIGUOUS, 0 otherwise
  {
    semantic_value             # canonical fields, §5.2
    evidence_stratum           # S-DOC | S-FILE
    artifact_sha256
    locator
    verbatim_excerpt
  }
]
traversal_record               # required when ABSENT
note_text                      # optional, RECORDED AND NEVER SCORED
```

**Canonical ordering:** `readings` are sorted lexicographically by the canonical serialization of `semantic_value`. Required for byte-identity and for set comparison.

| Verdict class | Meaning | `readings` |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | exactly 1, stratum `S-DOC` |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | exactly 1, stratum `S-FILE` |
| `AMBIGUOUS` | Evidence located; more than one reading survives | ≥ 2 |
| `ABSENT` | Exhaustive traversal found no determining evidence | 0; traversal record required |
| `NOT_APPLICABLE` | No data of the governed kind | 0; located justification in `traversal_record` |

**`EXPLICIT_FILE` is narrow.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines — text the file *declares*. **Inadmissible: value patterns.** Deriving a sign convention from the relation between current sign and a state-of-charge trend is domain inference, and admitting it would restore through `S-FILE` the inference removed by deleting `INFERABLE`. This is also the sharpest deliberate difference from published prior art, which permits value statistics to bind columns.

### 5.2 Canonical semantic values

**General rule, and the reason this is scoreable:** because the corpus is generated, every gold `semantic_value` is drawn from a frozen closed enum or a typed field. **No free text is scored.** An adjudicator may write anything it likes in `note_text`; the scorer never reads it.

| Parameter | Canonical fields |
|---|---|
| `E1` | `polarity ∈ {charge_positive, discharge_positive}` |
| `E2` | `zero_meaning ∈ {measured, placeholder}` |
| `E3` | `finest_reset_boundary ∈ {step, cycle, test, never}` |
| `E4a` | `timestamp_position ∈ {start, end, midpoint}` |
| `E4b` | `endpoint_convention ∈ {closed_closed, open_open, closed_open, open_closed}` |
| `E5` | `cadence_mode ∈ {fixed, event_driven}`; `interval_seconds: number` (required iff `fixed`, else null); `trigger ∈ {delta_voltage, delta_current, step_transition}` (required iff `event_driven`, else null) |
| `E6` | `coverage_rule ∈ {completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation}` |
| `E7a` | `operation_index_rule ∈ {explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker}` |
| `E7b` | `state_encoding ∈ {step_type_column, current_sign, separate_state_column, mode_code_enum}` |
| `E8a` | `unit ∈ {A, mA, V, mV, Ah, mAh, Wh, mWh, s, ms, degC, K}` |
| `E8b` | `scaling ∈ {none, factor}`; `factor_value: number` (required iff `factor`, else null) |

No `other_declared` value exists in any enum. The corpus never generates a fact outside these spaces, so an adjudicator that returns something outside them is wrong by construction, which is the intended behaviour.

Numeric fields are compared for exact equality. No tolerance: gold values are generated, so exactness is attainable.

### 5.3 Declared direction of conservatism

The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. Frozen; reproduced in any S2 or S3 output that reports a non-resolution figure.

---

## 6. Scoring

### 6.1 Correctness

- `EXPLICIT_DOC` / `EXPLICIT_FILE`: correct iff `verdict_class` matches gold **and** the single reading's `semantic_value` matches gold field-wise.
- `AMBIGUOUS`: correct iff `verdict_class` matches gold **and** the **set** of `semantic_value`s equals the gold set exactly, after canonical sort.
- `ABSENT` / `NOT_APPLICABLE`: correct iff `verdict_class` matches gold.

### 6.2 Error directions

- **Over-claim:** asserts determinacy the documentation does not support (`NEG-ABSENT` → `EXPLICIT_*` or `AMBIGUOUS`; `NEG-ADJACENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`).
- **Under-claim:** fails to find or accept determinacy that exists (`POS-*` → `ABSENT`).
- **Value error:** correct `verdict_class`, wrong `semantic_value`. Scored incorrect and reported separately, because it is invisible to any class-only metric.

Both directions matter, differently. Over-claim corrupts instrument integrity. Under-claim is the direction that would inflate a future non-resolution figure, since an instrument that fails to find stated facts manufactures the appearance of missing documentation.

### 6.3 `EVIDENCE_INVALID` — mechanical, on every verdict

For every reading, `verbatim_excerpt` must occur byte-exactly in the artifact named by `artifact_sha256`. A reading failing this is `EVIDENCE_INVALID`: the cell is scored incorrect, counted separately, and counted as a fabrication under `K1` **regardless of the cell's gold class**.

---

## 7. Adjudication protocol

### 7.1 Channels
Two primary adjudicators working independently; one reserve, unused unless a primary becomes unavailable, substitution disclosed.

**Blinding:** each receives the pinned bundle manifest and the frozen §2–§6 text. Nothing else — not ground truth, not item class, not the sentence bank, not the realization index, not corpus composition, not the other's output, not §8 or §9.

### 7.2 Disagreement
**Frozen before any disagreement is observed: disagreements are not resolved.** They are recorded and located. A tie-breaking third adjudicator would convert a measurement of verdict stability into a consensus procedure and destroy the quantity being measured.

### 7.3 Determinism
**Both** adjudicators re-run all 330 cells.

- Canonical serializer: fixed field order, fixed encoding, no timestamps, no run IDs, no model-version strings inside the verdict record.
- Model identity, version and sampling settings (temperature, seed, max tokens) frozen at `F3` and recorded in a **sidecar**, never in the record.
- Proof: rename the output, re-run, file must be **recreated** byte-identical. Recreation plus identity, not identity alone.

### 7.4 What agreement does not prove — frozen, reproduced verbatim in any S2 output

1. **Agreement is not correctness.** Two adjudicators can agree and both be wrong.
2. **Agreement is not independent replication.** LLM adjudicators share training-induced priors; agreement may be correlated error from a common source.
3. **Agreement is uninformative without demonstrated discriminative power.** An adjudicator returning a constant agrees perfectly with another returning the same constant.
4. **Agreement on constructed material does not transfer to real deposits.**
5. **High agreement is not a goal.** Agreement accompanied by a high rate of identical wrong answers is evidence of correlated behaviour and is reported as such.

---

## 8. Qualification decision function

**Qualification is emitted per parameter.** The output is a scoped statement:

```text
QUALIFIED_FOR:     [parameter ids]
NOT_QUALIFIED_FOR: [parameter ids, each with the failing condition]
```

An empty `QUALIFIED_FOR` list is `NOT_QUALIFIED`. **S3 may use only parameters in `QUALIFIED_FOR`.** There is no partial qualification within a parameter and no remediation-and-retest without a new freeze.

### 8.1 Why scoping replaced a global pass

v0.3 computed pass/fail per class across all parameters, so an adjudicator scoring `0/5` on one parameter's `POS-BURIED` cells and `45/45` elsewhere reached `45/50` and passed — certifying an instrument demonstrably unable to retrieve that parameter. At the `AMBIG-CONSTRUCTED` threshold, two whole parameters could be dead and the class still pass. That is a structural defect of aggregation, not a question of where the threshold sits.

### 8.2 Parameter-level conditions

For parameter `p` to enter `QUALIFIED_FOR`, **both** adjudicators must satisfy all of:

| Condition | Rule |
|---|---|
| **Dead-cell rule** | No `(p, class)` cell scores 0 of 5. A parameter with a dead class is not qualified, whatever its total. |
| **Parameter floor** | ≥ 25 of 30 cells correct. |
| **Fabrication** | Zero fabrications on `p`'s 5 `NEG-ABSENT` cells, and zero `EVIDENCE_INVALID` readings on any of `p`'s 30 cells (`K1`). |
| **Stability floor** | ≥ 24 of 30 cells agree between the two adjudicators on `(verdict_class, readings)` jointly. |

### 8.3 Instrument-level conditions

Reported alongside the scope, and required for any instrument-level statement:

| Class | Minimum correct, of 55, per adjudicator |
|---|---|
| `POS-EXPLICIT` | 54 |
| `POS-BURIED` | 49 |
| `NEG-ABSENT` | 55, with zero fabrications (`K1`) |
| `NEG-ADJACENT` | 49 |
| `AMBIG-CONSTRUCTED` | 44 |
| `NA-CONSTRUCTED` | 49 |

Instrument-level stability floor: ≥ 264 of 330 (80%) cell-level agreement.

**These numbers, and those in §8.2, are the constructor's policy tolerances. They are not statistical guarantees, they are not derived from any distribution, and they do not appeal to any anticipated S3 effect size — S3 is neither executed nor fully specified, and using its hypothetical results to justify a threshold would be reasoning from an unknown.** They are listed in §13 for ratification, on the principle by which `K1`'s threshold was sent back.

### 8.4 Correlated-error diagnostic — model-free

v0.3 promised to compare observed agreement against a value predicted from two accuracies under independent errors. Two overall accuracies do not determine that value for a multiclass output with an attached `semantic_value`: two adjudicators that are each 80% accurate may, when wrong, choose the same wrong answer or different ones, giving different expected agreement. Rather than freeze a formula whose assumptions are unverifiable, the comparison is removed and replaced by a decomposition that needs no model:

```text
both correct
both wrong, identical readings          <- direct evidence of correlated error
both wrong, different readings
exactly one correct
```

Reported per parameter and per class. Descriptive; it does not feed the decision function.

### 8.5 Condition table

```text
SCOPE            §8.2 per-parameter conditions -> QUALIFIED_FOR list
DISCRIMINATION   §8.3 class thresholds, both adjudicators
FABRICATION      K1  — zero, both adjudicators, incl. EVIDENCE_INVALID
STABILITY        §8.2 parameter floor and §8.3 instrument floor
DETERMINISM      K2  — both adjudicators, canonical form, recreation proof
LEAKAGE          K3  — probe does not fire
ATOMICITY        K4  — all eleven parameters pass pre-freeze re-inspection
FIDELITY         §4.4 — byte-level re-derivation match, 100%
STAFFING         K5  — five separated parties staffed
```

---

## 9. Kill conditions

### `K1` — fabrication

Fires on either of:

- a verdict of `EXPLICIT_DOC`, `EXPLICIT_FILE`, **or `AMBIGUOUS`** on a cell whose gold class is `NEG-ABSENT`. All three assert that bearing evidence was located; if gold says none exists, evidence was invented or misidentified. v0.3 counted only the two `EXPLICIT_*` cases and would have reported `fabrications: 0` while an adjudicator hallucinated conflicting evidence;
- any `EVIDENCE_INVALID` reading (§6.3), on any cell of any class.

Permitted count: **0.** No percentage threshold, and **no rate bound is reported** — the cells share bundles, parameters and a single adjudicator, so they are not independent trials and any Bernoulli bound would be unjustified.

### `K2` — determinism
Any re-run producing a non-identical canonical verdict record, for either adjudicator.

### `K3` — corpus leakage

```text
TASK
  predict the class of each (bundle, parameter) cell

CLASSIFIER
  multinomial logistic regression, L2, C = 1.0, max_iter = 1000
  scikit-learn, version pinned in F3
  (A simple frozen probe is used deliberately: a tuned strong learner
   would introduce researcher degrees of freedom. A negative result
   means "no leakage detectable by THIS probe", not "no leakage".)

FEATURES  (50 total, computed by the frozen F3 script)
  per component (article / README / CSV header):
    character count                                     3
    line count                                          3
    digit-to-character ratio                            3
    punctuation count                                   3
  bundle-level:
    article section-heading count                       1
    README section count                                1
    CSV header column count                             1
    mean sentence length (article, README)              2
    type-token ratio (article, README)                  2
      tokenization: whitespace, lowercased, no stemming
    formatting-marker presence flags                   20
  cell-level:
    parameter ID, one-hot                              11

FORMATTING MARKERS (frozen, presence/absence over whole bundle)
   1 ATX heading '#'          11 year-like '(20'
   2 setext underline '==='   12 bracketed ref '[1]'
   3 bullet '- '              13 'http'
   4 bullet '* '              14 DOI prefix '10.'
   5 numbered list '1.'       15 parenthesised unit token
   6 table pipe '|'           16 colon-terminated label line
   7 code fence '```'         17 ALL-CAPS token, length >= 3
   8 inline backtick          18 em dash
   9 blockquote '>'           19 semicolon
  10 footnote marker '[^'     20 line-initial '#' in CSV header

PREPROCESSING
  numeric features standardized on training-fold statistics only;
  no imputation (all features defined)

FOLD ASSIGNMENT
  unit = bundle. All 11 cells of a bundle stay in one fold.
  bundles sorted by bundle ID; fold = index mod 5
  5 folds x 6 bundles = 30 bundles = 330 cells
  deterministic; no shuffling

NULL
  no association between surface features and class
  p0 = 1/6, uniform by the §4.1 balance

STATISTIC
  A_obs = mean cross-validated multiclass accuracy over the 330
  held-out cell predictions

TEST
  permutation test, N = 2000, seed 20260912
  permutation unit: the bundle's whole 11-cell class-assignment
  vector, permuted across bundles; full CV re-run per permutation
  cell-level permutation is PROHIBITED

  p = (1 + #{permutations with A_perm >= A_obs}) / (1 + N)

FIRES IF
  p < 0.01
```

**`parameter ID` as a feature** is admissible only because §4.1 balances classes within every parameter, making the marginal class distribution uniform per parameter. If that balance is relaxed, parameter ID must be dropped or the probe learns the class-by-parameter distribution and reports it as stylistic leakage. The `F6` script checks the balance and refuses to emit the corpus if it fails.

**On the statistic.** A cell-level exact binomial against `p0 = 1/6` is wrong here for the same reason cell-level CV is: under the null, a probe assigning one class to a whole bundle produces correlated errors, understating variance and firing on noise.

### `K4` — atomicity
Any parameter fails the one-interrogative / mutually-exclusive-answers test on pre-freeze re-inspection. v0.1 failed on two parameters, v0.2 on one, v0.3 on three. **The base rate of this defect in this document's history is 100%.** A gate should assume v0.4 fails somewhere and should test every interrogative for hierarchy, conjunction, and non-exhaustive answer spaces — the three forms it has taken so far.

### `K5` — party independence

**Five separated parties** (six if the reserve adjudicator must also be independent):

1. **Constructor** — generation protocol, instrument, this document. No adjudication, no gate, no corpus authorship.
2. **Corpus / reference-label party** — new; no S1 role, no S2-construction role. Authors and seals ground truth, builds the sentence bank, runs the generator.
3. **Fidelity checker** — not the corpus party. Runs the §4.4 byte-level check.
4. **Adjudicator A** — blind.
5. **Adjudicator B** — blind, independent of A.
6. **Gate party** — new; no S1 role, no S2-construction role.

Excluded from parties 2–6: Fable (constructor), Sol (S1 instrument, sampling, calibration, decision-rule construction), and any agent that materially encoded S1 classifier logic.

`K5` fires if this cannot be staffed. That is the correct outcome, not an argument for relaxing the rule. `K5` is a resourcing condition, not a specification defect.

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

- Chung 2021 (`10.1038/s41597-021-00954-3`) excluded from S2 in every role.
- The §3 provenance disclosure is mandatory in the frozen preregistration.
- No prospective target of any later instance may be inspected during S2.
- The rejected agent analytical document stands as `GATE_BLOCKED / NON_GOVERNING / KNOWN_EXPOSURE`.
- A BatteryLake manifest review, if ratified, is `PRIOR_ART_EXPOSURE` under `PRIOR_ART_ELIMINATION_v0.2.md` §4.3 and may not be cited as S2 data.

---

## 11. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §5, §6 |
| `F2` | Corpus design: class-assignment design, cap, item classes, sentence bank (entries and keys), placement rules, generator and balance-verification scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — `K3` script, 50-feature list, 20 markers, permutation seed and p formula, model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | Ground-truth record authored and **sealed** (SHA-256) by the corpus party |
| `F6` | Bundles generated from the sealed truth; byte-level fidelity check passes; balance and cap verified |
| `F7` | Leakage probe `K3` |
| `F8` | Adjudication, both channels |
| `F9` | Determinism re-run, both channels; metrics by the `F3` script; §8 decision function applied |

Sealing precedes generation because the bundles are generated *from* the truth.

---

## 12. Declared limitations

**12.1 Statistical scope.** Failure-detection design, not estimation. No confidence intervals, no population estimates, no extrapolation to real deposits. No rate bound from `K1`.

**12.2 Ecological transfer.** The corpus is template-generated from a sentence bank, with entries inserted verbatim. Real deposits are longer, messier, and state facts in prose no bank contains. Qualification here may therefore be a test of template recognition rather than of reading real documentation. **Frozen consequence: a `QUALIFIED_FOR` result does not license S3.** It prevents S3 from beginning with a demonstrably broken instrument, on the listed parameters, and nothing more. Closing the ecological gap requires a separate step on real material with its own freeze, not specified here.

**12.3 Prohibited outputs.**
- No verdict about any real deposit.
- No prevalence figure about documentation quality in any literature.
- No pooled single-number accuracy.
- No agreement figure unless §8.3 discrimination passes.
- No confidence interval or population estimate.
- No claim that the S2 architecture is methodologically novel.
- No non-resolution figure without the §5.3 frozen sentence attached.
- No use in S3 of any parameter outside `QUALIFIED_FOR`.

---

## 13. L3 decisions

1. **Ratify or revise the thresholds** in §8.2 (dead-cell rule, 25/30 floor, 24/30 stability) and §8.3 (six class minima, 264/330 floor).
2. **Staffing of the five or six separated parties** — `K5`, binding on whether S2 runs.
3. **Corpus budget**: 30 bundles / 1320 adjudication events, or a reduced qualification.
4. **Publication status** of the qualification artifact, verbatim.
5. **BatteryLake manifest review** — `PRIOR_ART_ELIMINATION_v0.2.md` §6.
6. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`. Self-contained; no earlier version normative. Written by a constructor with a declared S1 conflict whose atomicity rule has failed in every prior version of this document. A gate should start at `K4` against all eleven interrogatives, at §4.1's 30×11 balance-and-cap feasibility, which is asserted and not demonstrated, and at §5.2, where closing the answer spaces by construction makes the corpus easier than reality in a way §12.2 admits but does not measure.
