# S2 Candidate Specification v0.5 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** v0.1–v0.4 — retained as history, **none normative**. This document is self-contained.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items in §14.

---

## 0. Changelog from v0.4

| # | Change |
|---|---|
| B11 | Atomicity split into three named tests. `ATOM-3` (real-domain exhaustiveness) is **explicitly not claimed**. Compositional parameters (`E5`, `E6`, `E7a`, `E7b`) take **set-valued** answers; `E8b` gains `affine` (§3, §5.2). |
| B12 | `EVIDENCE_UNSUPPORTED` added: every excerpt must contain the bank entry that realizes the claimed value. Evidence→claim binding is now scored, per reading (§6.3). |
| B13 | `ABSENT` correctness requires a complete traversal record against the manifest; `NOT_APPLICABLE` requires a located justification. Both mechanically scored (§6.4). |
| B14 | **§8.3 instrument-level thresholds demoted to reported diagnostics.** Scope membership is determined solely by the per-parameter conditions. One deterministic function (§8). |
| B15 | Freeze order corrected: corpus party is staffed **before** the sentence bank is authored and frozen (§12). |
| F5 | `K5` is **six** primary parties, seven with an independent reserve. No permitted overlap (§11.5). |
| F6 | All S1-conflicted actors excluded from adjudication by name, **including Ivan** (§11.5). |
| F7 | Qualification renamed `QUALIFIED_ON_CVD_FOR` with a frozen accompanying sentence (§8.1). |
| — | Class assignment adopted as the gate's demonstrated arrangement `(i + j) mod 6` (§4.1). |
| — | Dead-cell rule tightened from `> 0/5` to `≥ 3/5`, flagged as a visible policy choice (§8.2, §14). |

---

## 1. What S2 measures

> Does the deposit-semantics adjudication instrument produce verdicts that are discriminating against known ground truth, stable under adjudicator substitution, and deterministic on re-run — **for which parameters, and on what domain**?

S2 measures the instrument on a **constructed validation domain (CVD)**. It touches no real deposit, emits no statement about any dataset, no prevalence figure, and no methodological novelty claim.

Ground truth is written before the documentary artifact, because an adjudication instrument cannot be validated on labels produced by adjudication. Established paradigm, not a contribution.

---

## 2. Documentary space

`D` is an exhaustive ordered manifest per unit; each entry carries generation ID, timestamp, SHA-256, media type, stratum tag.

| Stratum | Contents | Proposition it supports |
|---|---|---|
| `S-DOC` | Article-style text, README, data dictionary, declared prose | *The depositor stated a rule.* |
| `S-FILE` | Declared in-file labels: column names, header rows, declared unit strings, explicit legend or comment lines | *The file declares a property.* |

Strata are **not ranked**. The verdict records which stratum carried it.

---

## 3. Atomicity, in three tests

The single rule in v0.1–v0.4 conflated properties with different evidentiary status. Split, named, and separately dispositioned:

| Test | Statement | Status in S2 |
|---|---|---|
| `ATOM-1` | Exactly one interrogative per parameter. | **Required. Tested by `K4`.** |
| `ATOM-2` | The answer space is mutually exclusive and exhaustive **over the CVD** — the frozen constructed corpus. | **Required. Tested by `K4`, mechanically verifiable against the sentence bank.** |
| `ATOM-3` | The answer space is exhaustive over the real semantic domain of public battery deposits. | **NOT DEMONSTRATED AND NOT CLAIMED.** |

Closing an answer space by construction is a property of the corpus, not a discovery about reality. Real logging can be hybrid fixed-plus-event-triggered, adaptive, per-step, or multi-rate; real scaling can be piecewise; the unit enum in `E8a` is not the set of all units a real export may declare. None of that is inside the CVD, and `K4` does not assert otherwise.

This is why qualification is named `QUALIFIED_ON_CVD_FOR` (§8.1) and why §13.2 stands.

### 3.1 Composition is not ambiguity

A parameter can have several **simultaneously true** mechanisms — a deposit may carry both an explicit cycle index and a filename encoding. That is not conflicting evidence and must not be scored `AMBIGUOUS`.

Frozen distinction:

- **Composition:** one reading whose `semantic_value` is a **set** of co-existing mechanisms. Verdict `EXPLICIT_*`.
- **Ambiguity:** two or more readings whose values are **mutually incompatible**. Verdict `AMBIGUOUS`. In the CVD, incompatibility is established by construction: `AMBIG-CONSTRUCTED` cells contain two bank entries whose values cannot both hold (e.g. `charge_positive` and `discharge_positive` for `E1`).

v0.4 forced composition into `AMBIGUOUS` or into a single-value answer, and both were wrong.

---

## 4. Parameters — eleven

| ID | Interrogative | Canonical answer (CVD-closed) |
|---|---|---|
| `E1` | For a signed quantity, which sign denotes charge? | `polarity ∈ {charge_positive, discharge_positive}` |
| `E2` | Does a zero in a signal column denote a measured value or a placeholder for an unrecorded value? | `zero_meaning ∈ {measured, placeholder}` |
| `E3` | What is the **finest** operational boundary at which a cumulative quantity resets to zero? | `finest_reset_boundary ∈ {step, cycle, test, never}` |
| `E4a` | Does a reported interval's timestamp denote start, end, or midpoint? | `timestamp_position ∈ {start, end, midpoint}` |
| `E4b` | Which endpoint convention governs reported intervals? | `endpoint_convention ∈ {closed_closed, open_open, closed_open, open_closed}` |
| `E5` | What rule governs the interval between logged records? | **set**, non-empty, of `{mode: fixed, interval_seconds: n}` and/or `{mode: event_driven, trigger ∈ {delta_voltage, delta_current, step_transition}}` |
| `E6` | By what rule is the absence of unlogged gaps established? | **set**, non-empty, of `{completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation}` |
| `E7a` | By what rule does a record map to an operation identifier? | **set**, non-empty, of `{explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker}` |
| `E7b` | By what rule is operational state (charge / discharge / rest) encoded in a record? | **set**, non-empty, of `{step_type_column, current_sign, separate_state_column, mode_code_enum}` |
| `E8a` | In what physical unit is each quantity reported? | `unit ∈ {A, mA, V, mV, Ah, mAh, Wh, mWh, s, ms, degC, K}` |
| `E8b` | What scaling, if any, was applied? | `scaling ∈ {none, factor, affine}`; `factor_value: number` (required iff `factor` or `affine`); `offset_value: number` (required iff `affine`) |

**Scope rule (frozen):** verdicts are emitted per `(unit, parameter, scope)`, where scope is the declared set of columns or signals governed.

**Provenance disclosure, mandatory in the frozen preregistration.** The cadence / coverage distinction (`E5`/`E6`) was first named by the S1 reviewer after the S1 outcome was known, and that reviewer authored this document. It is retained because uniform application of `ATOM-1` has forced four splits — `E2`/`E7b`, `E4a`/`E4b`, `E7a`/`E7b`, `E8a`/`E8b` — not one.

---

## 5. Corpus

### 5.1 Design and class assignment

```text
30 bundles x 11 parameters      = 330 parameter-cells

CLASS ASSIGNMENT (frozen, deterministic):
  class(bundle_i, parameter_j) = (i + j) mod 6
  i = 0..29, j = 0..10

Per parameter:   exactly 5 cells in each of 6 classes   (30 bundles = 5 full cycles)
Per bundle:      no class appears more than 2 times     (cap is 3; satisfied)
Across corpus:   55 cells per class, 330 total

Adjudications:
  330 x 2 adjudicators           = 660 primary
  330 x 2 (determinism re-run)   = 660
                                   1320 total
```

Column balance and row cap are **constructively demonstrated** by this arrangement, not asserted. The `F7` script re-verifies both and refuses to emit a corpus that fails either.

Verified property relevant to `K3`: with `fold = i mod 5`, each fold contains bundles `{f, f+5, f+10, f+15, f+20, f+25}`, whose `i mod 6` values cover all six residues. Every parameter therefore sees each class exactly once per fold, so `(parameter, fold)` carries no class information.

### 5.2 Item classes

| Class | Construction | Failure it detects |
|---|---|---|
| `POS-EXPLICIT` | Determining statement present, prominent | Cannot apply the standard to clear text |
| `POS-BURIED` | Determining statement present, non-obvious location | Retrieval failure → false `ABSENT` |
| `NEG-ABSENT` | No determining statement anywhere in `D` | Fabrication |
| `NEG-ADJACENT` | Related but non-determining statement present | Accepting a neighbour as the asked-for fact |
| `AMBIG-CONSTRUCTED` | Two mutually incompatible determining statements | Picking one reading instead of `AMBIGUOUS` |
| `NA-CONSTRUCTED` | No data of the governed kind, plus an explicit scope statement | Forcing a verdict where none applies |

`NA-CONSTRUCTED` cells carry a determining bank entry establishing non-applicability (e.g. a declared statement that the dataset contains no channel of the governed kind), so that `NOT_APPLICABLE` is scoreable symmetrically with the rest (§6.4).

No real deposit, including Chung 2021, is used as template or inspiration.

### 5.3 Generation and fidelity

Bundles are **generated, not written.** A frozen template engine inserts entries from a frozen **sentence bank**, keyed by `(parameter, class, semantic_value)`, **verbatim — no paraphrase**. Placement follows frozen rules under a frozen seed. The generator emits a realization index.

**Fidelity check — byte-level, 100%, no sampling.** The checker receives the generated bundle bytes and the sentence bank. It does **not** receive the realization index as an authority.

1. Search bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences found and their byte spans.
3. The derived record must equal the sealed record byte-identically.
4. For every `NEG-ABSENT` cell, verify mechanically that **no** determining bank entry for that parameter — of any value — occurs anywhere in the bundle bytes.
5. For every `NEG-ADJACENT` cell, verify the present entry is from the non-determining bank and no determining entry for that parameter occurs.
6. The realization index is a cross-check only. **Index–bytes disagreement halts at `F7`.**

`[L2]` Declared tension: verbatim insertion raises fidelity and lowers stylistic variety, raising leakage risk. `K3` is the arbiter. If `K3` fires because the bank is too templated, the response is a larger bank and full regeneration — never selective editing of the bundles the probe found.

---

## 6. Output schema and scoring

### 6.1 Record

```text
parameter_id
scope
verdict_class
readings: [                    # 1 for EXPLICIT_*, >=2 for AMBIGUOUS, 0 otherwise
  {
    semantic_value             # canonical fields or set, §4
    evidence_stratum           # S-DOC | S-FILE
    artifact_sha256
    locator                    # byte span
    verbatim_excerpt
  }
]
traversal_record               # required for ABSENT and NOT_APPLICABLE
note_text                      # optional, RECORDED AND NEVER SCORED
```

`readings` are sorted lexicographically by the canonical serialization of `semantic_value`. Set-valued `semantic_value`s are themselves canonically sorted.

| Verdict class | Meaning | `readings` |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | exactly 1, stratum `S-DOC` |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | exactly 1, stratum `S-FILE` |
| `AMBIGUOUS` | Two or more mutually incompatible readings located | ≥ 2 |
| `ABSENT` | Exhaustive traversal found no determining evidence | 0 |
| `NOT_APPLICABLE` | No data of the governed kind | 0 |

**`EXPLICIT_FILE` is narrow.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines. **Inadmissible: value patterns.** Deriving a sign convention from the relation between current sign and a state-of-charge trend is domain inference; admitting it would restore through `S-FILE` the inference removed by deleting `INFERABLE`. This is the sharpest deliberate difference from published prior art, which permits value statistics to bind columns.

### 6.2 Value correctness

No free text is scored. Every gold `semantic_value` is a frozen enum, typed field, or set thereof; comparison is exact and field-wise, sets by exact set equality, numerics by exact equality.

### 6.3 Evidence support — scored, per reading

v0.4 checked that a cited excerpt **exists**. It did not check that the excerpt **supports the claim**, so an adjudicator could return the right value while citing an unrelated sentence and still pass. Since the sentence bank is frozen and maps entries to `(parameter, semantic_value)`, this is mechanically checkable without a second adjudicator.

Two distinct checks, both on every reading:

- **`EVIDENCE_INVALID`** — `verbatim_excerpt` does not occur byte-exactly in the artifact named by `artifact_sha256`. The citation is invented. **Counts under `K1`, zero tolerance.**
- **`EVIDENCE_UNSUPPORTED`** — the excerpt occurs, but does not **contain, byte-exactly and in full**, the bank entry that realizes the claimed `semantic_value` for that parameter in that bundle. The citation is real but does not ground the claim. **Cell scored incorrect; counted and reported separately; does not carry its own zero-tolerance gate.**

The rule is generous in the safe direction: an adjudicator may quote more context than the determining sentence, never less.

For `AMBIGUOUS`, the check runs **per reading**: each reading's excerpt must contain the bank entry realizing that reading's value. A correct value *set* with mismatched excerpts is incorrect.

### 6.4 `ABSENT` and `NOT_APPLICABLE` — evidence obligations scored

v0.4 required a traversal record in the schema but scored these classes on `verdict_class` alone, so a garbage traversal record passed. That reopened the hole the record exists to close.

- **`ABSENT` is correct** iff `verdict_class` matches gold **and** `traversal_record` lists **every entry of that bundle's manifest `D`**, each marked examined. The scorer holds the manifest; the check is mechanical. Failure is recorded as `TRAVERSAL_INCOMPLETE` and the cell is incorrect.
- **`NOT_APPLICABLE` is correct** iff `verdict_class` matches gold **and** `traversal_record` carries a `verbatim_excerpt` that occurs byte-exactly in the named artifact and contains, in full, the bank entry establishing non-applicability for that parameter in that bundle. Failure is `JUSTIFICATION_UNSUPPORTED` and the cell is incorrect.

### 6.5 Error directions

- **Over-claim:** asserts determinacy the documentation does not support (`NEG-ABSENT` → `EXPLICIT_*` or `AMBIGUOUS`; `NEG-ADJACENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`).
- **Under-claim:** fails to find or accept determinacy that exists (`POS-*` → `ABSENT`).
- **Value error:** correct class, wrong value.
- **Grounding error:** correct class and value, `EVIDENCE_UNSUPPORTED`.

All four are reported separately. Over-claim corrupts instrument integrity; under-claim is the direction that would inflate a future non-resolution figure.

### 6.6 Declared direction of conservatism

The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. Frozen; reproduced in any S2 or S3 output reporting a non-resolution figure.

---

## 7. Adjudication protocol

**Channels.** Two primary adjudicators, independent; one reserve, unused unless a primary becomes unavailable, substitution disclosed.

**Blinding.** Each receives the pinned bundle manifest and the frozen §2–§6 text. Nothing else — not ground truth, not item class, not the sentence bank, not the realization index, not corpus composition, not the other's output, not §8 or §11.

**Disagreement.** Frozen before any disagreement is observed: **disagreements are not resolved.** They are recorded and located. A tie-breaking third adjudicator would convert a measurement of verdict stability into a consensus procedure and destroy the quantity being measured.

**Determinism.** Both adjudicators re-run all 330 cells. Canonical serializer: fixed field order and encoding, no timestamps, no run IDs, no model-version strings inside the record. Model identity, version and sampling settings frozen at `F3` and recorded in a sidecar. Proof: rename the output, re-run, file must be **recreated** byte-identical.

**What agreement does not prove — frozen, reproduced verbatim in any S2 output:**

1. Agreement is not correctness. Two adjudicators can agree and both be wrong.
2. Agreement is not independent replication. LLM adjudicators share training-induced priors; agreement may be correlated error from a common source.
3. Agreement is uninformative without demonstrated discriminative power. An adjudicator returning a constant agrees perfectly with another returning the same constant.
4. Agreement on constructed material does not transfer to real deposits.
5. High agreement is not a goal. Agreement accompanied by a high rate of identical wrong answers is evidence of correlated behaviour.

---

## 8. Qualification decision function

### 8.1 Output form

```text
QUALIFIED_ON_CVD_FOR:     [parameter ids]
NOT_QUALIFIED_ON_CVD_FOR: [parameter ids, each with the failing condition]
```

An empty list is `NOT_QUALIFIED`. **S3 may use only parameters in `QUALIFIED_ON_CVD_FOR`**, and only after the separate ecological step of §13.2.

**Frozen sentence, mandatory wherever the result is stated:**

> Qualification is demonstrated on the frozen constructed validation domain only. It is not a claim that the instrument is qualified for this parameter on real deposit documentation.

The name carries `CVD` because `QUALIFIED_FOR: E5` reads as "qualified for cadence semantics", which is broader than what any S2 result can support.

### 8.2 The decision function — parameter conditions only

For parameter `p`, membership in `QUALIFIED_ON_CVD_FOR` requires that **both** adjudicators satisfy all of:

| Condition | Rule |
|---|---|
| **Cell floor** | Every `(p, class)` cell scores **≥ 3 of 5**. |
| **Fabrication** | Zero `K1` events on any of `p`'s 30 cells — no over-claim on `p`'s 5 `NEG-ABSENT` cells, no `EVIDENCE_INVALID` reading anywhere in `p`. |
| **Parameter floor** | ≥ 25 of 30 cells correct, where correctness includes evidence support (§6.3) and traversal obligations (§6.4). |
| **Stability floor** | ≥ 24 of 30 cells agree between the two adjudicators on `(verdict_class, readings)` jointly. |

Nothing else determines membership. **This is the entire decision function.**

The cell floor was `> 0/5` in v0.4, which permitted `1/5` — 80% error on a class — to qualify if the parameter's other cells compensated to `25/30`. `≥ 3/5` is a constructor policy choice and is listed in §14 so the operator ratifies it seeing what it permits.

### 8.3 Reported diagnostics — not gates

v0.4 listed instrument-level class thresholds among the qualification conditions while also declaring qualification to be per-parameter, leaving two readings of the same text. Class-level aggregation is exactly the mechanism shown able to hide a dead parameter, so it cannot be a second veto over a scope decision the parameter conditions already make soundly.

These are computed and reported, and **do not affect `QUALIFIED_ON_CVD_FOR`**:

- per-class correct counts out of 55, per adjudicator;
- instrument-wide cell agreement out of 330;
- counts of `EVIDENCE_UNSUPPORTED`, `TRAVERSAL_INCOMPLETE`, `JUSTIFICATION_UNSUPPORTED`;
- the model-free correlated-error decomposition:

```text
both correct
both wrong, identical readings          <- direct evidence of correlated error
both wrong, different readings
exactly one correct
```

`K1` is the one global condition that is absolute; it enters the decision function through the per-parameter fabrication rule, and any `K1` event anywhere is reported instrument-wide.

---

## 9. Kill conditions

### `K1` — fabrication
Fires on either:
- `EXPLICIT_DOC`, `EXPLICIT_FILE`, **or `AMBIGUOUS`** on a cell whose gold class is `NEG-ABSENT` — all three assert located evidence where gold says none exists;
- any `EVIDENCE_INVALID` reading (§6.3), on any cell of any class.

Permitted count: **0.** No rate bound is reported — the cells share bundles, parameters and a single adjudicator, so they are not independent trials.

### `K2` — determinism
Any re-run producing a non-identical canonical verdict record, for either adjudicator.

### `K3` — corpus leakage

```text
TASK        predict the class of each (bundle, parameter) cell

CLASSIFIER  multinomial logistic regression, L2, C = 1.0,
            max_iter = 1000; scikit-learn version pinned at F3
            (A simple frozen probe is deliberate: a tuned strong
             learner adds researcher degrees of freedom. A negative
             result means "no leakage detectable by THIS probe".)

FEATURES (50)
  per component (article / README / CSV header):
    character count 3 | line count 3 | digit ratio 3 | punctuation 3
  bundle-level:
    article heading count 1 | README section count 1
    CSV header column count 1
    mean sentence length (article, README) 2
    type-token ratio (article, README) 2
      tokenization: whitespace, lowercased, no stemming
    formatting-marker presence flags 20
  cell-level:
    parameter ID one-hot 11

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

PREPROCESSING  numeric features standardized on training-fold
               statistics only; no imputation

FOLDS       unit = bundle; all 11 cells of a bundle in one fold
            bundles sorted by ID; fold = index mod 5
            5 folds x 6 bundles = 30 bundles = 330 cells
            deterministic; no shuffling

NULL        no association between surface features and class
            p0 = 1/6, uniform by the §5.1 assignment

STATISTIC   A_obs = mean CV multiclass accuracy over 330 held-out cells

TEST        permutation, N = 2000, seed 20260912
            unit: a bundle's whole 11-cell class vector, permuted
            across bundles; full CV re-run per permutation
            cell-level permutation PROHIBITED

            p = (1 + #{A_perm >= A_obs}) / (1 + N)

FIRES IF    p < 0.01
```

`parameter ID` is admissible as a feature only because §5.1 balances classes within every parameter. If that balance is relaxed, parameter ID must be dropped. The `F7` script verifies the balance and refuses to emit otherwise.

### `K4` — atomicity
Tests `ATOM-1` and `ATOM-2` only (§3). Fires if any parameter carries more than one interrogative, or if its answer space is not mutually exclusive and exhaustive over the CVD. `ATOM-3` is outside `K4` by design and is not claimed anywhere.

Defect history in this document: v0.1 failed on two parameters, v0.2 on one, v0.3 on three, v0.4 on the exclusivity half for four. The forms it has taken are **hierarchy** (`E3`), **conjunction** (`E7`), **non-exhaustive enumeration** (`E4b`), and **composition mistaken for conflict** (`E5`–`E7b`). A gate should test all four forms against all eleven interrogatives.

### `K5` — party independence
See §11.5. Fires if the required parties cannot be staffed. That is the correct outcome, not an argument for relaxing the rule. `K5` is a resourcing condition, not a specification defect.

---

## 10. Condition table

```text
SCOPE          §8.2 per-parameter conditions -> QUALIFIED_ON_CVD_FOR
FABRICATION    K1 — zero, both adjudicators, incl. EVIDENCE_INVALID
DETERMINISM    K2 — both adjudicators, canonical form, recreation proof
LEAKAGE        K3 — probe does not fire
ATOMICITY      K4 — ATOM-1 and ATOM-2 on all eleven parameters
FIDELITY       §5.3 — byte-level re-derivation match, 100%
STAFFING       K5 — six separated parties staffed
DIAGNOSTICS    §8.3 — reported, not gating
```

---

## 11. Parties

### 11.5 `K5` — six primary parties, seven with an independent reserve

| # | Party | Role | May not also be |
|---|---|---|---|
| 1 | **Constructor** | Generation protocol, instrument, this document | any of 2–6 |
| 2 | **Corpus / reference-label party** | Authors the sentence bank, authors and seals ground truth, runs the generator | any of 1, 3–6 |
| 3 | **Fidelity checker** | Byte-level §5.3 check | any of 1, 2, 4, 5, 6 |
| 4 | **Adjudicator A** | Blind adjudication | any other |
| 5 | **Adjudicator B** | Blind adjudication | any other |
| 6 | **Gate party** | Reviews and gates | any of 1–5 |
| 7 | *Reserve adjudicator* | Substitute for 4 or 5, disclosed | any of 1, 2, 3, 6 |

v0.4 said "five separated parties" and then listed six. There is **no permitted overlap**. In particular the gate party may not be the fidelity checker: fidelity checking is execution, and a gate that performs it would be certifying its own work.

**Excluded from parties 2–7 by name:**
- **Fable** — constructor of this instrument and S1 contributing reviewer.
- **Sol** — S1 instrument, sampling, calibration and decision-rule construction.
- **Ivan** — materially participated in S1 construction, specification and ratification. Retains L3 ratification, which is not an evaluative role, and is excluded from corpus authorship, fidelity checking, adjudication and gate.
- **Any agent that materially encoded S1 classifier or decision logic.**

The exclusion is by role, not only by name: any actor materially involved in S1 as author, specifier, implementer of decision rules, or contributing reviewer is excluded from parties 2–7, whether or not listed above.

---

## 12. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §4, §6 |
| `F2` | Corpus design: class-assignment rule, cap, item classes, **sentence-bank schema and keying — not its contents**, placement rules, generator and verification scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — `K3` script, 50 features, 20 markers, permutation seed and p formula, model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | **Sentence bank authored by the corpus party and frozen** |
| `F6` | Ground-truth record authored and **sealed** (SHA-256) by the corpus party |
| `F7` | Bundles generated from the sealed truth; byte-level fidelity check; balance and cap verified |
| `F8` | Leakage probe `K3` |
| `F9` | Adjudication, both channels |
| `F10` | Determinism re-run; metrics by the `F3` script; §8.2 decision function applied |

v0.4 froze the sentence bank at `F2` while the only party authorised to author it was not staffed until `F4` — procedurally impossible under its own rules. Staffing now precedes authorship, and authorship precedes sealing, because the truth is expressed in bank entries.

---

## 13. Declared limitations

**13.1 Statistical scope.** Failure-detection design, not estimation. No confidence intervals, no population estimates, no extrapolation to real deposits. No rate bound from `K1`.

**13.2 Domain and ecological transfer.** The CVD is template-generated from a frozen bank with entries inserted verbatim, and its answer spaces are closed by construction (`ATOM-3` not demonstrated). Real deposits are longer, messier, state facts in prose no bank contains, and can exhibit mechanisms outside every enum here. Qualification here may therefore be a test of template recognition on a domain simpler than reality.

**Frozen consequence: `QUALIFIED_ON_CVD_FOR` does not license S3.** It prevents S3 from beginning with an instrument demonstrably broken on the listed parameters, on a domain simpler than the one S3 faces, and nothing more. Closing the gap requires a separate step on real material with its own freeze, not specified here.

**13.3 Prohibited outputs.**
- No verdict about any real deposit.
- No prevalence figure about documentation quality in any literature.
- No pooled single-number accuracy.
- No claim of real-domain exhaustiveness for any answer space.
- No confidence interval or population estimate.
- No claim that the S2 architecture is methodologically novel.
- No non-resolution figure without the §6.6 frozen sentence attached.
- No statement of qualification without the §8.1 frozen sentence attached.
- No use in S3 of any parameter outside `QUALIFIED_ON_CVD_FOR`.

---

## 14. L3 decisions

1. **Ratify or revise §8.2**: cell floor `≥ 3/5`, parameter floor `25/30`, stability floor `24/30`. The cell floor is the one that determines how bad a single class may be while a parameter still qualifies; at `≥ 3/5` a parameter can qualify with 40% error on one class.
2. **Staffing of six (or seven) separated parties** — `K5`, binding on whether S2 runs.
3. **Corpus budget**: 30 bundles / 1320 adjudication events, or a reduced qualification.
4. **Publication status** of the qualification artifact, verbatim.
5. **BatteryLake manifest review** — `PRIOR_ART_ELIMINATION_v0.2.md` §6.
6. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`. Self-contained; no earlier version normative. Written by a constructor with a declared S1 conflict whose atomicity rule has failed in every prior version of this document, most recently on the exclusivity half rather than the interrogative half. A gate should start at `K4` against all four defect forms, at §6.3's assumption that "excerpt contains the bank entry in full" is the right grounding test rather than a proxy for one, and at §8.3 — where demoting the class thresholds removed an ambiguity and also removed the only instrument-wide discrimination gate, which is a trade the operator should see stated.
