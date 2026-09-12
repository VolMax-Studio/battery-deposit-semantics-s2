# S2 Candidate Specification v0.6 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** v0.1–v0.5 — retained as history, **none normative**. Self-contained.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items in §14.

---

## 0. Changelog from v0.5

| # | Change |
|---|---|
| B16 | Decision function is now **two-stage**: global prerequisites, then per-parameter membership. `K1` resolved as **global**. §10 is a restatement, not a parallel list (§8). |
| B17 | **Exactly one canonical scope per `(bundle, parameter)`**, drawn from a frozen scope vocabulary, declared in the manifest and **scored for exact match**. Cell arithmetic unchanged (§5.1, §6.2). |
| B18 | **Bank back-translation round** by an independent validator party; disagreeing entries rejected, never corrected. **Frozen incompatibility relation**, with an exclusive sub-bank for set-valued parameters (§5.3, §5.4). |
| B19 | `E8b` canonical forms made disjoint. Overlap check extended to `E5` and `E3` (§4.1). |
| F-a | Canonical numeric serialization frozen (§6.6). |
| F-b | CI assertion of parameter×fold balance (§5.1). |
| — | Parties: **seven primary**, eight with reserve (§11). |

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

| Test | Statement | Status |
|---|---|---|
| `ATOM-1` | Exactly one interrogative per parameter, **at a fixed scope**. | Required. Tested by `K4`. |
| `ATOM-2` | Answer space mutually exclusive and exhaustive **over the CVD**, with no two canonical forms expressing the same fact. | Required. Tested by `K4`, mechanically. |
| `ATOM-3` | Answer space exhaustive over the real semantic domain. | **NOT DEMONSTRATED AND NOT CLAIMED.** |

Closing an answer space by construction is a property of the corpus, not a discovery about reality. Real logging can be hybrid, adaptive, per-step or multi-rate; real scaling can be piecewise; the `E8a` unit enum is not the set of all units a real export may declare. None of that is in the CVD, and `K4` does not assert otherwise.

**Composition is not ambiguity.** A parameter may have several simultaneously true mechanisms — that is one reading whose `semantic_value` is a **set**, verdict `EXPLICIT_*`. Ambiguity is two or more **mutually incompatible** readings, verdict `AMBIGUOUS`, where incompatibility is established by the frozen relation in §5.4, never by mere difference.

---

## 4. Parameters — eleven

Each verdict is emitted for exactly one `(unit, parameter, scope)`, and the CVD assigns exactly one canonical scope per `(bundle, parameter)` (§5.1). The scope rule is what makes `ATOM-1` hold for `E1` and `E8a`, whose v0.5 wording ("a signed quantity", "each quantity") quantified over signals and was therefore a hidden conjunction.

| ID | Interrogative (at the cell's scope) | Canonical answer (CVD-closed) |
|---|---|---|
| `E1` | Which sign of this signal denotes charge? | `polarity ∈ {charge_positive, discharge_positive}` |
| `E2` | Does a zero in this signal denote a measured value or a placeholder for an unrecorded value? | `zero_meaning ∈ {measured, placeholder}` |
| `E3` | What is the **finest** operational boundary at which this cumulative quantity resets to zero? | `finest_reset_boundary ∈ {step, cycle, test, never}` |
| `E4a` | Does this signal's interval timestamp denote start, end, or midpoint? | `timestamp_position ∈ {start, end, midpoint}` |
| `E4b` | Which endpoint convention governs this signal's intervals? | `endpoint_convention ∈ {closed_closed, open_open, closed_open, open_closed}` |
| `E5` | What rule governs the interval between logged records of this signal? | **set**, non-empty, of `{mode: fixed, interval_seconds: n}` and/or `{mode: event_driven, trigger ∈ {delta_voltage, delta_current, step_transition}}` |
| `E6` | By what rule is the absence of unlogged gaps in this signal established? | **set**, non-empty, of `{completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation}` |
| `E7a` | By what rule does a record map to an operation identifier? | **set**, non-empty, of `{explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker}` |
| `E7b` | By what rule is operational state (charge / discharge / rest) encoded in a record? | **set**, non-empty, of `{step_type_column, current_sign, separate_state_column, mode_code_enum}` |
| `E8a` | In what physical unit is this signal reported? | `unit ∈ {A, mA, V, mV, Ah, mAh, Wh, mWh, s, ms, degC, K}` |
| `E8b` | What scaling was applied to this signal? | `scaling ∈ {none, factor, affine}` with `factor_value`, `offset_value` — canonical forms in §4.1 |

### 4.1 Canonical-form disjointness (`ATOM-2`)

Different canonical forms must not express the same fact. Frozen:

**`E8b`** — `none` and `factor_value = 1` are the same transformation; `factor = 2` and `affine(2, 0)` are the same transformation. Disjoint forms:

```text
none    factor_value = 1  AND offset_value = 0
factor  factor_value != 1 AND offset_value = 0
affine  offset_value != 0 (factor_value unrestricted)
```

The `F2` validator rejects any bank entry whose canonical form is not unique under this rule.

**`E5`** — checked and clean: the trigger enum contains no time-based trigger, so a fixed cadence cannot also be expressed as `event_driven`. Any future addition of a time-based trigger reopens this and is prohibited without a new freeze.

**`E3`** — `never` and `test` overlap when the deposit contains a single test. Frozen: `never` means no reset occurs at any boundary within the deposited data; a bundle whose gold is `test` must declare **at least two tests**. The `F2` validator enforces this.

**Provenance disclosure, mandatory in the frozen preregistration.** The cadence / coverage distinction (`E5`/`E6`) was first named by the S1 reviewer after the S1 outcome was known, and that reviewer authored this document. It is retained because uniform application of `ATOM-1` has forced four splits — `E2`/`E7b`, `E4a`/`E4b`, `E7a`/`E7b`, `E8a`/`E8b` — not one.

---

## 5. Corpus

### 5.1 Design, scope, class assignment

```text
30 bundles x 11 parameters      = 330 parameter-cells

SCOPE: exactly one canonical scope per (bundle, parameter),
declared in the bundle manifest, drawn from the frozen vocabulary
  current | voltage | capacity_charge | capacity_discharge |
  energy | temperature | time | step_index | cycle_index
Each parameter has a frozen subset of applicable scopes.
The cell unit therefore remains (bundle, parameter).

CLASS ASSIGNMENT (frozen, deterministic):
  class(bundle_i, parameter_j) = (i + j) mod 6,  i = 0..29, j = 0..10

Per parameter:  exactly 5 cells in each of 6 classes
Per bundle:     no class appears more than 2 times (cap is 3)
Across corpus:  55 cells per class, 330 total

Adjudications:  330 x 2 = 660 primary; 660 determinism re-run; 1320 total
```

**CI assertions, run before execution and sealed:**

```text
for every parameter j:        class counts == [5,5,5,5,5,5]
for every bundle i:           max class count <= 3
for every (parameter, fold):  class counts == [1,1,1,1,1,1]
for every (bundle, parameter): exactly one scope, in the frozen
                               applicable subset for that parameter
```

The third holds because `fold = i mod 5` puts bundles `{f, f+5, …, f+25}` in a fold, whose `i mod 6` values cover all six residues — so `(parameter, fold)` carries no class information. True by construction, asserted mechanically anyway.

### 5.2 Item classes

| Class | Construction | Failure it detects |
|---|---|---|
| `POS-EXPLICIT` | Determining statement present, prominent | Cannot apply the standard to clear text |
| `POS-BURIED` | Determining statement present, non-obvious location | Retrieval failure → false `ABSENT` |
| `NEG-ABSENT` | No determining statement anywhere in `D` | Fabrication |
| `NEG-ADJACENT` | Related but non-determining statement present | Accepting a neighbour as the asked-for fact |
| `AMBIG-CONSTRUCTED` | Two readings incompatible under §5.4 | Picking one reading instead of `AMBIGUOUS` |
| `NA-CONSTRUCTED` | No data of the governed kind, plus an explicit scope statement | Forcing a verdict where none applies |

No real deposit, including Chung 2021, is used as template or inspiration.

### 5.3 Sentence bank and its integrity

The bank maps `(parameter, class, semantic_value) → entry text`. Byte-level fidelity (§5.5) proves that the bytes in a bundle are the entries the key says they are. It does **not** prove that an entry's text *means* what its key says: a corpus party that writes "Positive current denotes discharge." under the key `charge_positive` produces a gold value that the bytes contradict, and every mechanical check downstream inherits the error while punishing an adjudicator that reads correctly.

**Bank back-translation round, frozen:**

1. The corpus party authors the bank as `key → text`.
2. An independent **bank validator party** receives the entry texts **shuffled and stripped of keys**, plus the frozen answer enums and parameter interrogatives, and assigns each text a `(parameter, semantic_value)` key.
3. Every entry whose back-translated key differs from the authored key is **rejected and removed from the bank — never corrected**. Correction would let the corpus party's reading override an independent one.
4. The corpus party may author replacements; replacements enter a further round.
5. The bank is frozen only when back-translation agrees on 100% of retained entries.

**Declared limitation:** this is a two-party agreement check, not a proof of meaning. It cannot detect a misreading shared by both parties. That residual risk is real and is not closed by anything in this specification.

The bank validator has seen the bank and its keys and is therefore excluded from adjudication (§11).

### 5.4 Frozen incompatibility relation

`AMBIG-CONSTRUCTED` requires that the two readings cannot both hold. Difference is not incompatibility.

- **Single-valued parameters** (`E1`, `E2`, `E3`, `E4a`, `E4b`, `E8a`, `E8b`): any two distinct canonical values are incompatible, by `ATOM-2` mutual exclusivity.
- **Set-valued parameters** (`E5`, `E6`, `E7a`, `E7b`): two different sets are **not** incompatible by default — they may compose. Incompatibility requires that both statements come from the bank's **exclusive sub-bank**, whose entries assert exclusivity in their text (for example, a statement that records are logged at a fixed interval *and by no other rule*). Frozen relation: two set-valued readings are incompatible iff both entries are from the exclusive sub-bank and their value sets differ.

The `F2` validator rejects any `AMBIG-CONSTRUCTED` cell whose two entries do not satisfy this relation.

### 5.5 Generation and byte-level fidelity

Bundles are **generated, not written**: a frozen template engine inserts bank entries **verbatim, no paraphrase**, with placement under frozen rules and a frozen seed. The generator emits a realization index.

The fidelity checker receives the generated bundle bytes and the frozen bank, and **not** the realization index as an authority:

1. Search bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences and their byte spans.
3. The derived record must equal the sealed record byte-identically.
4. For every `NEG-ABSENT` cell, verify that **no** determining bank entry for that parameter — of any value — occurs anywhere in the bundle.
5. For every `NEG-ADJACENT` cell, verify the present entry is from the non-determining bank and no determining entry for that parameter occurs.
6. The realization index is a cross-check only. **Index–bytes disagreement halts at `F8`.**

`[L2]` Declared tension: verbatim insertion raises fidelity and lowers stylistic variety, raising leakage risk. `K3` is the arbiter. If `K3` fires because the bank is too templated, the response is a larger bank and full regeneration — never selective editing of the bundles the probe found.

---

## 6. Output schema and scoring

### 6.1 Record

```text
parameter_id
scope
verdict_class
readings: [ { semantic_value, evidence_stratum, artifact_sha256,
              locator, verbatim_excerpt } ]
traversal_record          # required for ABSENT and NOT_APPLICABLE
note_text                 # optional, RECORDED AND NEVER SCORED
```

`readings` sorted lexicographically by canonical serialization of `semantic_value`; set values themselves canonically sorted.

| Verdict class | Meaning | `readings` |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | exactly 1, stratum `S-DOC` |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | exactly 1, stratum `S-FILE` |
| `AMBIGUOUS` | Two or more readings incompatible under §5.4 | ≥ 2 |
| `ABSENT` | Exhaustive traversal found no determining evidence | 0 |
| `NOT_APPLICABLE` | No data of the governed kind | 0 |

**`EXPLICIT_FILE` is narrow.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines. **Inadmissible: value patterns** — deriving a sign convention from the relation between current sign and a state-of-charge trend is domain inference, and admitting it would restore through `S-FILE` the inference removed by deleting `INFERABLE`. This is the sharpest deliberate difference from published prior art, which permits value statistics to bind columns.

### 6.2 Correctness

A cell is correct iff **all** of:

1. **Scope** matches gold exactly. v0.5 carried `scope` in the schema and never scored it, so an adjudicator could attach a right value to the wrong signal and pass.
2. **`verdict_class`** matches gold.
3. **`semantic_value`** matches gold field-wise; sets by exact set equality; numerics by exact equality after canonical serialization (§6.6). For `AMBIGUOUS`, the **set** of reading values equals the gold set.
4. **Evidence support** holds for every reading (§6.3).
5. **Traversal obligations** hold for `ABSENT` and `NOT_APPLICABLE` (§6.4).

No free text is scored. `note_text` is never read by the scorer.

### 6.3 Evidence checks, per reading

- **`EVIDENCE_INVALID`** — `verbatim_excerpt` does not occur byte-exactly in the artifact named by `artifact_sha256`. The citation is invented. **Counts under `K1`, zero tolerance, global.**
- **`EVIDENCE_UNSUPPORTED`** — the excerpt occurs but does not **contain, byte-exactly and in full**, the bank entry realizing the claimed `semantic_value` for that parameter in that bundle. Cell incorrect; counted and reported separately; no zero-tolerance gate of its own.

The rule is generous in the safe direction: quote more context than the determining sentence, never less. For `AMBIGUOUS` the check runs **per reading** — a correct value set with mismatched excerpts is incorrect.

`[L2]` This is a proxy for evidence→claim validity, not the thing itself. It tests that the adjudicator cited the passage that carries the fact; it cannot test whether the adjudicator understood why. §5.3's back-translation is what stands behind the bank keys, and its residual risk is stated there.

### 6.4 `ABSENT` and `NOT_APPLICABLE`

- **`ABSENT`** is correct only if `traversal_record` lists **every entry of that bundle's manifest `D`**, each marked examined. The scorer holds the manifest. Failure: `TRAVERSAL_INCOMPLETE`, cell incorrect.
- **`NOT_APPLICABLE`** is correct only if `traversal_record` carries a `verbatim_excerpt` occurring byte-exactly in the named artifact and containing, in full, the bank entry establishing non-applicability. Failure: `JUSTIFICATION_UNSUPPORTED`, cell incorrect.

### 6.5 Error directions

Over-claim (`NEG-ABSENT` → `EXPLICIT_*`/`AMBIGUOUS`; `NEG-ADJACENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`); under-claim (`POS-*` → `ABSENT`); scope error; value error; grounding error. All reported separately. Over-claim corrupts instrument integrity; under-claim is the direction that would inflate a future non-resolution figure.

### 6.6 Canonical numeric serialization (frozen)

So that `10`, `10.0` and `1e1` are one byte value:

- decimal notation only, never exponent;
- integers rendered with no decimal point and no trailing zeros;
- non-integers rendered to 6 significant digits, trailing zeros stripped;
- no leading `+`; a single leading `-` for negatives; no thousands separators.

Applies to `interval_seconds`, `factor_value`, `offset_value`, and every numeric field in gold and output alike.

### 6.7 Declared direction of conservatism

The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. Frozen; reproduced in any S2 or S3 output reporting a non-resolution figure.

---

## 7. Adjudication protocol

**Channels.** Two primary adjudicators, independent; one reserve, unused unless a primary becomes unavailable, substitution disclosed.

**Blinding.** Each receives the pinned bundle manifest — including the cell's scope — and the frozen §2–§6 text. Nothing else: not ground truth, not item class, not the sentence bank, not the realization index, not corpus composition, not the other's output, not §8.

**Disagreement.** Frozen before any disagreement is observed: **disagreements are not resolved.** They are recorded and located. A tie-breaking third adjudicator would convert a measurement of verdict stability into a consensus procedure.

**Determinism.** Both adjudicators re-run all 330 cells. Canonical serializer: fixed field order and encoding, §6.6 numerics, no timestamps, no run IDs, no model-version strings in the record. Model identity, version and sampling settings frozen at `F3`, recorded in a sidecar. Proof: rename output, re-run, file must be **recreated** byte-identical.

**What agreement does not prove — frozen, reproduced verbatim in any S2 output:**

1. Agreement is not correctness.
2. Agreement is not independent replication; LLM adjudicators share training-induced priors.
3. Agreement is uninformative without demonstrated discriminative power.
4. Agreement on constructed material does not transfer to real deposits.
5. High agreement is not a goal; agreement with a high rate of identical wrong answers is evidence of correlated behaviour.

---

## 8. Decision function — two stages, single-valued

### Stage 1 — Global prerequisites

All must pass. Any failure yields `QUALIFIED_ON_CVD_FOR = []`, the run terminates with the named prerequisite, and per-parameter results are reported as diagnostics carrying no qualification.

| Prerequisite | Rule |
|---|---|
| `K5` staffing | Seven separated parties staffed (§11) |
| Bank integrity | §5.3 back-translation agrees on 100% of retained entries |
| Fidelity | §5.5 byte-level re-derivation match, 100% |
| `K4` atomicity | `ATOM-1` and `ATOM-2` hold for all eleven parameters, pre-freeze |
| `K3` leakage | Probe does not fire (§9.3) |
| `K2` determinism | Both adjudicators reproduce byte-identically |
| `K1` fabrication | **Zero events, either adjudicator, any cell** (§9.1) |

**`K1` is global, not per-parameter.** v0.5 left both readings open. The resolution is the stricter one: fabrication is a property of the adjudicator, not of the parameter, and an adjudicator that invents evidence once has shown it invents evidence. Qualifying `E7` on the strength of clean `E7` cells while the same adjudicator fabricated on `E1` would certify exactly the behaviour the instrument exists to exclude.

**Stated consequence, for ratification.** With 660 primary adjudications and zero tolerance, a single fabrication anywhere terminates the run. `[L2]` My expectation is that this makes `NOT_QUALIFIED` the more likely first outcome. That is an informative result — it says the instrument fabricates — not a wasted run. The operator should ratify the rule knowing this.

The same logic does not extend to `K2`, `K3`, `K4`, fidelity or bank integrity for a different reason: each of those invalidates the *measurement*, not the adjudicator. A leaky corpus makes every parameter's numbers uninterpretable; a failed fidelity or bank check makes gold unreliable everywhere; a staffing failure means the independence architecture does not hold. None can be scoped to a parameter.

### Stage 2 — Per-parameter membership

Evaluated **only if Stage 1 passes in full**. For parameter `p`, membership requires that **both** adjudicators satisfy:

| Condition | Rule |
|---|---|
| **Cell floor** | Every `(p, class)` cell scores **≥ 3 of 5** |
| **Parameter floor** | ≥ **25 of 30** cells correct, correctness per §6.2 |
| **Stability floor** | ≥ **24 of 30** cells agree on `(scope, verdict_class, readings)` jointly |

Nothing else determines membership.

### 8.1 Output form

```text
QUALIFIED_ON_CVD_FOR:     [parameter ids]
NOT_QUALIFIED_ON_CVD_FOR: [parameter ids, each with the failing condition]
```

**Frozen sentence, mandatory wherever the result is stated:**

> Qualification is demonstrated on the frozen constructed validation domain only. It is not a claim that the instrument is qualified for this parameter on real deposit documentation.

### 8.2 Reported diagnostics — not gates

Computed and reported; they do **not** affect membership: per-class correct counts out of 55 per adjudicator; instrument-wide cell agreement out of 330; counts of `EVIDENCE_UNSUPPORTED`, `TRAVERSAL_INCOMPLETE`, `JUSTIFICATION_UNSUPPORTED`, scope errors; and the model-free correlated-error decomposition (`both correct` / `both wrong, identical readings` / `both wrong, different readings` / `exactly one correct`).

**Stated trade.** There is no instrument-wide discrimination gate. All eleven parameters could sit at the `3/5` cell floor on `POS-BURIED` and every one still qualify, leaving an instrument systematically weak at buried retrieval with a full `QUALIFIED_ON_CVD_FOR` list. The cell floor is the only protection against that, and it is in §14 for ratification.

---

## 9. Kill conditions

### `K1` — fabrication
Fires on either: `EXPLICIT_DOC`, `EXPLICIT_FILE` or `AMBIGUOUS` on a cell whose gold class is `NEG-ABSENT`; or any `EVIDENCE_INVALID` reading, on any cell of any class. Permitted count **0**, global. No rate bound is reported — the cells share bundles, parameters and a single adjudicator and are not independent trials.

### `K2` — determinism
Any re-run producing a non-identical canonical verdict record, either adjudicator.

### `K3` — corpus leakage

```text
TASK        predict the class of each (bundle, parameter) cell

CLASSIFIER  multinomial logistic regression, L2, C = 1.0,
            max_iter = 1000; scikit-learn version pinned at F3
            (Simple frozen probe by design: a tuned learner adds
             researcher degrees of freedom. A negative result means
             "no leakage detectable by THIS probe".)

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

NULL        p0 = 1/6, uniform by the §5.1 assignment

STATISTIC   A_obs = mean CV multiclass accuracy over 330 held-out cells

TEST        permutation, N = 2000, seed 20260912
            unit: a bundle's whole 11-cell class vector, permuted
            across bundles; full CV re-run per permutation
            cell-level permutation PROHIBITED
            p = (1 + #{A_perm >= A_obs}) / (1 + N)

FIRES IF    p < 0.01
```

`parameter ID` is admissible only because §5.1 balances classes within every parameter; if the balance is relaxed it must be dropped. The `F8` script verifies and refuses to emit otherwise.

### `K4` — atomicity
Tests `ATOM-1` and `ATOM-2` only. `ATOM-3` is outside `K4` by design and is not claimed anywhere.

Defect history: v0.1 failed on two parameters, v0.2 on one, v0.3 on three, v0.4 on exclusivity for four, v0.5 on canonical overlap in `E8b` and on scope-quantification in `E1`/`E8a`. The forms are **hierarchy**, **conjunction**, **non-exhaustive enumeration**, **composition mistaken for conflict**, **canonical-form overlap**, and **implicit quantification over signals**. A gate should test all six against all eleven interrogatives.

### `K5` — party independence
See §11. Fires if the parties cannot be staffed. That is the correct outcome, not an argument for relaxing the rule; `K5` is a resourcing condition, not a specification defect.

---

## 10. Condition table

This table is a restatement of §8, not a parallel set of rules. Where any tension is read into it, **§8 governs**.

```text
STAGE 1 (global prerequisites, all required)
  K5 staffing | bank integrity | fidelity | K4 | K3 | K2 | K1
       |
       v
STAGE 2 (per-parameter membership)
  cell floor >= 3/5 | parameter floor >= 25/30 | stability >= 24/30
       |
       v
  QUALIFIED_ON_CVD_FOR

DIAGNOSTICS (§8.2) are reported and never gate.
```

---

## 11. Parties — seven primary, eight with reserve

| # | Party | Role | May not also be |
|---|---|---|---|
| 1 | **Constructor** | Generation protocol, instrument, this document | any of 2–7 |
| 2 | **Corpus / reference-label party** | Authors the bank, authors and seals ground truth, runs the generator | any other |
| 3 | **Bank validator** | §5.3 back-translation, key-blind | any other |
| 4 | **Fidelity checker** | §5.5 byte-level check | any other |
| 5 | **Adjudicator A** | Blind adjudication | any other |
| 6 | **Adjudicator B** | Blind adjudication | any other |
| 7 | **Gate party** | Reviews and gates | any of 1–6 |
| 8 | *Reserve adjudicator* | Substitute for 5 or 6, disclosed | any of 1, 2, 3, 4, 7 |

**No permitted overlap.** In particular the gate party may not be the fidelity checker — fidelity checking is execution, and a gate performing it would certify its own work — and the bank validator may not adjudicate, having seen the bank and its keys.

**Excluded from parties 2–8, by name and by role:**
- **Fable** — constructor of this instrument and S1 contributing reviewer.
- **Sol** — S1 instrument, sampling, calibration and decision-rule construction.
- **Ivan** — materially participated in S1 construction, specification and ratification. Retains L3 ratification, which is not an evaluative role, and is excluded from bank authorship, bank validation, fidelity checking, adjudication and gate.
- **Any agent that materially encoded S1 classifier or decision logic.**
- Generally: any actor materially involved in S1 as author, specifier, implementer of decision rules, or contributing reviewer, whether or not named above.

---

## 12. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §4, §6 |
| `F2` | Corpus design: class-assignment rule, scope vocabulary and per-parameter applicable subsets, cap, item classes, bank schema and keying **(not contents)**, exclusive sub-bank definition, incompatibility relation, placement rules, generator and validator scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — `K3` script, 50 features, 20 markers, seed and p formula, canonical serializer, model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | **Sentence bank authored by the corpus party** |
| `F6` | **Bank back-translation by the validator; rejections removed; bank frozen** |
| `F7` | Ground-truth record authored and **sealed** (SHA-256) by the corpus party |
| `F8` | Bundles generated; byte-level fidelity check; CI assertions of §5.1 |
| `F9` | Leakage probe `K3` |
| `F10` | Adjudication, both channels |
| `F11` | Determinism re-run; metrics by the `F3` script; §8 decision function applied |

Staffing precedes bank authorship; back-translation precedes sealing, because the sealed truth is expressed in bank entries and a rejected entry would otherwise be sealed into gold.

---

## 13. Declared limitations

**13.1 Statistical scope.** Failure-detection design, not estimation. No confidence intervals, no population estimates, no extrapolation to real deposits. No rate bound from `K1`.

**13.2 Domain and ecological transfer.** The CVD is template-generated from a frozen bank with entries inserted verbatim; its answer spaces are closed by construction (`ATOM-3` not demonstrated); and every `(bundle, parameter)` cell has exactly one scope, where a real deposit has many signals per parameter. Real deposits are longer, messier, and state facts in prose no bank contains. Qualification here may be a test of template recognition on a domain simpler than reality in at least three respects.

**Frozen consequence: `QUALIFIED_ON_CVD_FOR` does not license S3.** It prevents S3 from beginning with an instrument demonstrably broken on the listed parameters, on a simpler domain, and nothing more. Closing the gap requires a separate step on real material with its own freeze, not specified here.

**13.3 Bank meaning.** §5.3 establishes two-party agreement on what each entry means, not meaning itself. A misreading shared by corpus party and validator propagates into gold undetected.

**13.4 Prohibited outputs.** No verdict about any real deposit; no prevalence figure about documentation quality in any literature; no pooled single-number accuracy; no claim of real-domain exhaustiveness for any answer space; no confidence interval or population estimate; no claim of methodological novelty; no non-resolution figure without the §6.7 sentence; no statement of qualification without the §8.1 sentence; no use in S3 of any parameter outside `QUALIFIED_ON_CVD_FOR`.

---

## 14. L3 decisions

1. **Ratify or revise Stage 2 thresholds**: cell floor `≥ 3/5`, parameter floor `25/30`, stability floor `24/30`. At `≥ 3/5` a parameter qualifies with 40% error on one class, and with no instrument-wide gate (§8.2) every parameter could sit there simultaneously.
2. **Ratify `K1` as a global prerequisite**, knowing that one fabrication in 660 adjudications terminates the run.
3. **Staffing of seven (or eight) separated parties** — `K5`, binding on whether S2 runs.
4. **Corpus budget**: 30 bundles / 1320 adjudication events, plus the bank back-translation round, or a reduced qualification.
5. **Publication status** of the qualification artifact, verbatim.
6. **BatteryLake manifest review** — `PRIOR_ART_ELIMINATION_v0.2.md` §6.
7. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`. Self-contained; no earlier version normative. Written by a constructor with a declared S1 conflict whose atomicity rule has failed in every prior version of this document, in six distinct forms. A gate should start at `K4` against all six forms; at §5.3, where the back-translation round adds a party and a rejection loop whose cost and termination behaviour are not modelled; and at §5.4, where the exclusive sub-bank is the only thing making `AMBIG-CONSTRUCTED` valid for four of the eleven parameters and does not yet exist.
