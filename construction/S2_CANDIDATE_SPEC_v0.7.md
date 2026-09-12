# S2 Candidate Specification v0.7 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** v0.1–v0.6 — retained as history, **none normative**. Self-contained.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`
**Status:** `SPREMNO ZA GEJT` — candidate, not frozen, not ratified, **not gated**
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items in §15.

---

## 0. Changelog from v0.6

| # | Change |
|---|---|
| B20 | Bank key extended to `(parameter, scope, class, semantic_value)`; evidence support and back-translation are now scope-bound; **scope is orthogonal to class by construction** and enters the `K3` feature set (§4.2, §5.1, §5.3, §6.3). |
| B21 | Back-translation validates `semantic_role` and `exclusive_assertion`, not only value (§5.4). |
| B22 | Bank loop made finite: frozen inventory of **330 single-use entries**, 3-round limit, 30% rejection ceiling, no adaptive simplification, terminal state `BANK_INTEGRITY_NOT_ESTABLISHED` (§5.5). |
| B23 | `E3` structural realization constraints separate step / cycle / test / never (§4.3). |
| F8 | **Semantic stability** (gating) split from **evidence concordance** (diagnostic) (§8, §9.2). |
| F9 | `note_text` **prohibited** during the qualification run (§6.1). |
| — | Governance: reviews by parties excluded under `K5` are recorded as `ADVERSARIAL_PRE_GATE_REVIEW` and cannot satisfy the gate (§12). |

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
| `ATOM-1` | Exactly one interrogative per parameter, at a fixed scope. | Required. Tested by `K4`. |
| `ATOM-2` | Answer space mutually exclusive and exhaustive **over the CVD**, no two canonical forms expressing the same fact, and **empirically separable in every realized bundle**. | Required. Tested by `K4`, mechanically. |
| `ATOM-3` | Answer space exhaustive over the real semantic domain. | **NOT DEMONSTRATED AND NOT CLAIMED.** |

Closing an answer space by construction is a property of the corpus, not a discovery about reality.

**Composition is not ambiguity.** Several simultaneously true mechanisms are one reading whose `semantic_value` is a **set**, verdict `EXPLICIT_*`. Ambiguity is two or more **mutually incompatible** readings, verdict `AMBIGUOUS`, incompatibility established only by the frozen relation in §5.6.

---

## 4. Parameters and scopes

Each verdict is emitted for exactly one `(unit, parameter, scope)`. The CVD assigns exactly one scope per `(bundle, parameter)`.

### 4.1 The eleven parameters

| ID | Interrogative (at the cell's scope) | Canonical answer (CVD-closed) |
|---|---|---|
| `E1` | Which sign of this signal denotes charge? | `polarity ∈ {charge_positive, discharge_positive}` |
| `E2` | Does a zero in this signal denote a measured value or a placeholder for an unrecorded value? | `zero_meaning ∈ {measured, placeholder}` |
| `E3` | What is the **finest** operational boundary at which this cumulative quantity resets to zero? | `finest_reset_boundary ∈ {step, cycle, test, never}` |
| `E4a` | Does this signal's interval timestamp denote start, end, or midpoint? | `timestamp_position ∈ {start, end, midpoint}` |
| `E4b` | Which endpoint convention governs this signal's intervals? | `endpoint_convention ∈ {closed_closed, open_open, closed_open, open_closed}` |
| `E5` | What rule governs the interval between logged records of this signal? | **set**, non-empty, of `{mode: fixed, interval_seconds: n}` and/or `{mode: event_driven, trigger ∈ {delta_voltage, delta_current, step_transition}}` |
| `E6` | By what rule is the absence of unlogged gaps in this signal established? | **set**, non-empty, of `{completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation}` |
| `E7a` | By what rule does a record map to this operation identifier? | **set**, non-empty, of `{explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker}` |
| `E7b` | By what rule is operational state (charge / discharge / rest) encoded at this level? | **set**, non-empty, of `{step_type_column, current_sign, separate_state_column, mode_code_enum}` |
| `E8a` | In what physical unit is this signal reported? | `unit ∈ {A, mA, V, mV, W, mW, Ah, mAh, Wh, mWh, s, ms, degC, K}` |
| `E8b` | What scaling was applied to this signal? | `scaling ∈ {none, factor, affine}` with `factor_value`, `offset_value` — §4.3 |

### 4.2 Scope vocabulary and per-parameter subsets

Frozen vocabulary: `current`, `voltage`, `power`, `capacity_charge`, `capacity_discharge`, `energy`, `temperature`, `time`, `step_index`, `cycle_index`, `test_index`.

**Every parameter has exactly five applicable scopes in the CVD.** Five is not arbitrary: it makes scope exactly orthogonal to class (§5.1).

| Parameter | Applicable scopes |
|---|---|
| `E1` | current, power, capacity_charge, capacity_discharge, energy |
| `E2` | current, voltage, power, temperature, energy |
| `E3` | capacity_charge, capacity_discharge, energy, time, step_index |
| `E4a` | current, voltage, temperature, energy, capacity_charge |
| `E4b` | current, voltage, temperature, energy, capacity_charge |
| `E5` | current, voltage, power, temperature, capacity_charge |
| `E6` | current, voltage, power, temperature, capacity_charge |
| `E7a` | step_index, cycle_index, test_index, time, current |
| `E7b` | step_index, cycle_index, test_index, time, current |
| `E8a` | current, voltage, capacity_charge, energy, temperature |
| `E8b` | current, voltage, capacity_charge, energy, temperature |

### 4.3 Canonical-form disjointness and empirical separability (`ATOM-2`)

**`E8b`** — disjoint forms:

```text
none    factor_value = 1  AND offset_value = 0
factor  factor_value != 1 AND offset_value = 0
affine  offset_value != 0 (factor_value unrestricted)
```

**`E5`** — the trigger enum contains no time-based trigger, so a fixed cadence cannot also be expressed as `event_driven`. Adding a time-based trigger later is prohibited without a new freeze.

**`E3`** — v0.6 separated only `test` from `never`. Disjointness of the enum on paper is not enough: if every cycle has one step, then in that bundle the step boundary *is* the cycle boundary and `finest_reset_boundary` is not empirically separable, however clean the enum looks.

Frozen structural realization constraint. **Every** bundle carrying an `E3` cell — of any class — must declare a dataset structure in which:

```text
at least one cycle contains >= 2 steps     separates step from cycle
at least one test  contains >= 2 cycles    separates cycle from test
the data contains  >= 2 tests              separates test from never
```

and the determining statement (where the class provides one) must state reset behaviour such that exactly one boundary is the finest at which reset occurs. For gold `never`, the statement asserts that no reset occurs at any boundary while the structure still contains all three boundary levels. The `F2` validator enforces the structure; the `F8` fidelity check enforces that the bundle declares it.

This constraint is the reason `ATOM-2` now carries the words *empirically separable in every realized bundle*.

**Provenance disclosure, mandatory in the frozen preregistration.** The cadence / coverage distinction (`E5`/`E6`) was first named by the S1 reviewer after the S1 outcome was known, and that reviewer authored this document. It is retained because uniform application of `ATOM-1` has forced four splits — `E2`/`E7b`, `E4a`/`E4b`, `E7a`/`E7b`, `E8a`/`E8b` — not one.

---

## 5. Corpus

### 5.1 Design: cells, class, scope, orthogonality

```text
30 bundles x 11 parameters      = 330 parameter-cells

CLASS   class(i, j) = (i + j) mod 6           i = 0..29, j = 0..10
SCOPE   scope_index(i, j) = (i + 2j) mod 5    -> j's 5th applicable scope

Per parameter:            5 cells in each of 6 classes
Per parameter:            6 cells for each of 5 scopes
Per parameter:            each (class, scope) pair occurs EXACTLY ONCE
Per bundle:               no class more than 2 times (cap 3)
Across corpus:            55 cells per class, 330 total

Adjudications: 330 x 2 = 660 primary; 660 determinism re-run; 1320 total
```

**Scope is orthogonal to class by construction.** For fixed `j`, `i mod 6` and `i mod 5` jointly determine `i mod 30`, so as `i` runs over 0..29 the pair `((i+j) mod 6, (i+2j) mod 5)` takes each of the 30 `(class, scope)` combinations exactly once. There is therefore no scope→class signal for an adjudicator to exploit, and the `(parameter, class)` cell's five cells span five distinct scopes.

**CI assertions, run before execution and sealed:**

```text
for every parameter:            class counts == [5,5,5,5,5,5]
for every parameter:            scope counts == [6,6,6,6,6]
for every parameter:            every (class, scope) pair count == 1
for every bundle:               max class count <= 3
for every (parameter, fold):    class counts == [1,1,1,1,1,1]
for every (bundle, parameter):  exactly one scope, from j's applicable five
```

`scope_index` depends on `i mod 5`, as does `fold = i mod 5`, so within a fold each parameter carries a single scope. That redundancy is stated rather than hidden: the real protection against scope leakage is the orthogonality assertion above, and the `K3` scope feature (§9.3) can only detect a violation the CI assertions should have caught first.

### 5.2 Item classes

| Class | Construction | Failure it detects | Bank entries per cell |
|---|---|---|---|
| `POS-EXPLICIT` | Determining statement, prominent | Cannot apply the standard to clear text | 1 determining |
| `POS-BURIED` | Determining statement, non-obvious location | Retrieval failure → false `ABSENT` | 1 determining |
| `NEG-ABSENT` | No determining statement anywhere in `D` | Fabrication | 0 |
| `NEG-ADJACENT` | Related, non-determining statement | Accepting a neighbour as the asked-for fact | 1 adjacent |
| `AMBIG-CONSTRUCTED` | Two readings incompatible under §5.6 | Picking one reading instead of `AMBIGUOUS` | 2 determining |
| `NA-CONSTRUCTED` | No data of the governed kind, plus explicit scope statement | Forcing a verdict where none applies | 1 non-applicable |

No real deposit, including Chung 2021, is used as template or inspiration.

### 5.3 Sentence bank — key and scope binding

```text
BANK KEY:  (parameter, scope, class, semantic_value, semantic_role)
           -> entry text
```

v0.6 keyed the bank on `(parameter, class, semantic_value)` with no scope, so a cell whose gold was `E5 / current / fixed 10 s` could be "supported" by an excerpt stating that *voltage* is logged every ten seconds: scope matched gold, value matched gold, and the quoted entry matched the key. The evidence was about the wrong signal and every check passed.

Frozen consequences:

- Each entry text **must name its scope's signal explicitly.**
- `EVIDENCE_UNSUPPORTED` (§6.3) checks the excerpt against the entry keyed for `(parameter, scope, semantic_value)` — the scope-specific entry, not any entry with the right value.
- Back-translation (§5.4) must reconstruct **scope** as well.

### 5.4 Bank back-translation — role-aware

Byte-level fidelity proves the bytes are the entries the key says. It does not prove an entry's text *means* what its key says, nor that it plays the *role* the key assigns.

The validator receives entry texts **shuffled, stripped of keys**, plus the frozen interrogatives, answer enums, and scope vocabulary, and returns for each text:

```text
parameter
scope
semantic_value          # null iff semantic_role = non_determining_adjacent
semantic_role ∈ { determining, non_determining_adjacent, non_applicable }
exclusive_assertion ∈ { true, false }
```

**All five fields must match the authored key.** Any mismatch rejects the entry.

This is what v0.6 missed. A corpus party could label a sentence `NEG-ADJACENT` while the validator, reading the same sentence, correctly extracts a determining value — which *proves* the sentence is determining, not adjacent, yet v0.6's protocol never asked and so never noticed. The same gap made the exclusive sub-bank unverified: the validator could recognise a value without ever confirming the "and by no other rule" assertion that is the sole basis for two set-valued readings being in conflict.

**Declared limitation:** this is a two-party agreement check on five fields, not a proof of meaning. A misreading shared by corpus party and validator propagates into gold undetected (§14.3).

The validator has seen the bank and its keys and is excluded from adjudication (§12).

### 5.5 Bank inventory, single use, and a finite loop

**Required inventory, frozen.** Per `(parameter, scope)` — 55 pairs — six cells require:

```text
1 determining  (POS-EXPLICIT)
1 determining  (POS-BURIED)
1 adjacent     (NEG-ADJACENT)
2 determining  (AMBIG-CONSTRUCTED, both exclusive for set-valued parameters)
1 non-applicable (NA-CONSTRUCTED)
= 6 entries per (parameter, scope)
```

`55 x 6 = 330 entries`, and **every entry is used exactly once in the corpus.** No reuse. This is the frozen coverage requirement: it forces 330 distinct texts and makes "recycle one very obvious template" structurally impossible. `K3`'s feature set does not measure lexical diversity, so the constraint must be imposed rather than tested for.

**Loop termination, frozen.**

- **Round limit: 3.** A rejected entry may be replaced twice.
- **Replacements must target the identical key** — same parameter, scope, class, semantic_value and role. The corpus party may **not** substitute an easier value, drop a hard scope, or re-key an entry. Without this, the CVD could be adaptively simplified until the validator agrees.
- **Rejection ceiling: 30% of authored entries, cumulative.** Exceeding it fires the terminal state immediately, without further rounds. A high rejection rate means the two parties systematically disagree about the answer space itself, which is a finding about the instrument's vocabulary and is not something to iterate away.
- **Terminal state:** if after three rounds any of the 330 required slots is unfilled, or the rejection ceiling is breached, the run ends at `BANK_INTEGRITY_NOT_ESTABLISHED`. S2 does not proceed. `[L2]` This is an informative outcome — the vocabulary cannot be expressed unambiguously even in purpose-built prose — and reporting it is more valuable than a bank massaged into agreement.

**Stated cost:** 330 distinct entries authored by one party and independently back-translated by another, with up to two replacement rounds. This is the largest single work item in S2 and it is in §15 for budget ratification.

### 5.6 Frozen incompatibility relation

- **Single-valued parameters** (`E1`, `E2`, `E3`, `E4a`, `E4b`, `E8a`, `E8b`): any two distinct canonical values are incompatible, by `ATOM-2`.
- **Set-valued parameters** (`E5`, `E6`, `E7a`, `E7b`): different sets are **not** incompatible by default — they may compose. Incompatibility requires both entries to carry `exclusive_assertion = true`, independently confirmed by back-translation, and their value sets to differ.

The `F2` validator rejects any `AMBIG-CONSTRUCTED` cell whose two entries do not satisfy this.

### 5.7 Generation and byte-level fidelity

Bundles are **generated, not written**: a frozen template engine inserts bank entries **verbatim, no paraphrase**, placement under frozen rules and a frozen seed. The generator emits a realization index.

The fidelity checker receives the bundle bytes and the frozen bank, and **not** the realization index as an authority:

1. Search bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences and byte spans.
3. The derived record must equal the sealed record byte-identically.
4. For every `NEG-ABSENT` cell: **no** determining entry for that `(parameter, scope)` — of any value — occurs anywhere in the bundle.
5. For every `NEG-ADJACENT` cell: the present entry is the keyed adjacent entry and no determining entry for that `(parameter, scope)` occurs.
6. For every bundle carrying an `E3` cell: the declared structure satisfies §4.3.
7. The realization index is a cross-check only. **Index–bytes disagreement halts at `F8`.**

`[L2]` Declared tension: verbatim single-use insertion raises fidelity and, with 330 distinct texts, raises lexical diversity — which is the one place where the single-use rule and `K3` pull in the same direction rather than against each other.

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
```

`note_text` is **prohibited during the qualification run** and must be absent. v0.6 carried it as unscored free text, which created two hazards: it entered the canonical record and could fail `K2` on a re-worded note alone, and it gave the adjudicator an unscored channel for reasoning that the instrument does not evaluate. Removing it closes both.

`readings` sorted lexicographically by canonical serialization of `semantic_value`; set values themselves canonically sorted.

| Verdict class | Meaning | `readings` |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | exactly 1, `S-DOC` |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | exactly 1, `S-FILE` |
| `AMBIGUOUS` | Two or more readings incompatible under §5.6 | ≥ 2 |
| `ABSENT` | Exhaustive traversal found no determining evidence | 0 |
| `NOT_APPLICABLE` | No data of the governed kind | 0 |

**`EXPLICIT_FILE` is narrow.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines. **Inadmissible: value patterns** — deriving a sign convention from the relation between current sign and a state-of-charge trend is domain inference, and admitting it would restore through `S-FILE` the inference removed by deleting `INFERABLE`. This is the sharpest deliberate difference from published prior art, which permits value statistics to bind columns.

### 6.2 Correctness

A cell is correct iff all of:

1. **Scope** matches gold exactly.
2. **`verdict_class`** matches gold.
3. **`semantic_value`** matches gold field-wise; sets by exact set equality; numerics by exact equality after canonical serialization (§6.6). For `AMBIGUOUS`, the set of reading values equals the gold set.
4. **Evidence support** holds for every reading (§6.3).
5. **Traversal obligations** hold for `ABSENT` and `NOT_APPLICABLE` (§6.4).

### 6.3 Evidence checks, per reading

- **`EVIDENCE_INVALID`** — `verbatim_excerpt` does not occur byte-exactly in the artifact named by `artifact_sha256`. The citation is invented. **Counts under `K1`, zero tolerance, global.**
- **`EVIDENCE_UNSUPPORTED`** — the excerpt occurs but does not **contain, byte-exactly and in full**, the bank entry keyed for `(parameter, scope, semantic_value)` in that bundle. Cell incorrect; counted and reported separately; no zero-tolerance gate of its own.

Generous in the safe direction: quote more context than the determining sentence, never less. For `AMBIGUOUS` the check runs **per reading**.

`[L2]` This remains a proxy for evidence→claim validity. It tests that the adjudicator cited the scope-specific passage carrying the fact; it cannot test whether the adjudicator understood why. §5.4 is what stands behind the bank keys, with the residual risk stated in §14.3.

### 6.4 `ABSENT` and `NOT_APPLICABLE`

- **`ABSENT`** correct only if `traversal_record` lists **every entry of that bundle's manifest `D`**, each marked examined. Failure: `TRAVERSAL_INCOMPLETE`.
- **`NOT_APPLICABLE`** correct only if `traversal_record` carries a `verbatim_excerpt` occurring byte-exactly in the named artifact and containing, in full, the keyed non-applicability entry for that `(parameter, scope)`. Failure: `JUSTIFICATION_UNSUPPORTED`.

### 6.5 Error directions
Over-claim (`NEG-ABSENT` → `EXPLICIT_*`/`AMBIGUOUS`; `NEG-ADJACENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`); under-claim (`POS-*` → `ABSENT`); scope error; value error; grounding error. All reported separately. Over-claim corrupts instrument integrity; under-claim is the direction that would inflate a future non-resolution figure.

### 6.6 Canonical numeric serialization (frozen)
Decimal only, never exponent; integers with no decimal point and no trailing zeros; non-integers to 6 significant digits with trailing zeros stripped; no leading `+`; single leading `-`; no thousands separators. So `10`, `10.0` and `1e1` are one byte value. Applies to `interval_seconds`, `factor_value`, `offset_value`, and every numeric field in gold and output alike.

### 6.7 Declared direction of conservatism
The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. Frozen; reproduced in any S2 or S3 output reporting a non-resolution figure.

---

## 7. Adjudication protocol

**Channels.** Two primary adjudicators, independent; one reserve, unused unless a primary becomes unavailable, substitution disclosed.

**Blinding.** Each receives the pinned bundle manifest — including the cell's scope — and the frozen §2–§6 text. Nothing else: not ground truth, not item class, not the bank, not the realization index, not corpus composition, not the other's output, not §8.

**Disagreement.** Frozen before any disagreement is observed: **disagreements are not resolved.** They are recorded and located.

**Determinism.** Both adjudicators re-run all 330 cells. Canonical serializer: fixed field order and encoding, §6.6 numerics, no timestamps, no run IDs, no model-version strings in the record; `note_text` absent by §6.1. Model identity, version and sampling settings frozen at `F3`, recorded in a sidecar. Proof: rename output, re-run, file must be **recreated** byte-identical.

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
| `K5` staffing | Seven separated parties staffed (§12) |
| Bank integrity | §5.4 back-translation agrees on all five fields for 100% of retained entries, within §5.5 limits |
| Fidelity | §5.7 byte-level re-derivation match, 100% |
| `K4` atomicity | `ATOM-1` and `ATOM-2` hold for all eleven parameters, pre-freeze |
| `K3` leakage | Probe does not fire (§9.3) |
| `K2` determinism | Both adjudicators reproduce byte-identically |
| `K1` fabrication | **Zero events, either adjudicator, any cell** (§9.1) |

**`K1` is global, not per-parameter.** Fabrication is a property of the adjudicator, not of the parameter; an adjudicator that invents evidence once has shown it invents evidence. **Stated consequence, for ratification:** with 660 primary adjudications and zero tolerance, one fabrication anywhere terminates the run. `[L2]` My expectation is that `NOT_QUALIFIED` is the more likely first outcome. That is an informative result, not a wasted run.

`K2`, `K3`, `K4`, fidelity and bank integrity are global for a different reason: each invalidates the *measurement* rather than the adjudicator, and none can be scoped to a parameter.

### Stage 2 — Per-parameter membership

Evaluated only if Stage 1 passes in full. For parameter `p`, both adjudicators must satisfy:

| Condition | Rule |
|---|---|
| **Cell floor** | Every `(p, class)` cell scores **≥ 3 of 5** |
| **Parameter floor** | ≥ **25 of 30** cells correct, correctness per §6.2 |
| **Semantic stability** | ≥ **24 of 30** cells agree on `(scope, verdict_class, semantic_value set)` |

Nothing else determines membership.

**Stability is semantic only.** v0.6 required agreement on `readings` entire, including locator and excerpt, so two adjudicators both returning `charge_positive / EXPLICIT_DOC` while quoting two different valid sentences counted as a disagreement. That measured evidence-selection identity, not verdict stability, and could fail a sound instrument for having more than one good citation available. **Evidence concordance** — agreement on `(artifact_sha256, locator, verbatim_excerpt)` among semantically agreeing cells — is computed and reported as a diagnostic (§9.2) and does not gate.

### 8.1 Output form

```text
QUALIFIED_ON_CVD_FOR:     [parameter ids]
NOT_QUALIFIED_ON_CVD_FOR: [parameter ids, each with the failing condition]
```

**Frozen sentence, mandatory wherever the result is stated:**

> Qualification is demonstrated on the frozen constructed validation domain only. It is not a claim that the instrument is qualified for this parameter on real deposit documentation.

---

## 9. Kill conditions and diagnostics

### 9.1 `K1` — fabrication
Fires on: `EXPLICIT_DOC`, `EXPLICIT_FILE` or `AMBIGUOUS` on a cell whose gold class is `NEG-ABSENT`; or any `EVIDENCE_INVALID` reading, any cell, any class. Permitted count **0**, global. No rate bound is reported — the cells share bundles, parameters, scopes and a single adjudicator and are not independent trials.

### 9.2 Reported diagnostics — never gating
Per-class correct counts out of 55 per adjudicator; instrument-wide semantic agreement out of 330; **evidence concordance** out of the semantically agreeing cells; counts of `EVIDENCE_UNSUPPORTED`, `TRAVERSAL_INCOMPLETE`, `JUSTIFICATION_UNSUPPORTED`, scope errors; and the model-free correlated-error decomposition (`both correct` / `both wrong, identical readings` / `both wrong, different readings` / `exactly one correct`).

**Stated trade.** There is no instrument-wide discrimination gate. All eleven parameters could sit at the `3/5` cell floor on `POS-BURIED` and every one still qualify, leaving an instrument systematically weak at buried retrieval with a full `QUALIFIED_ON_CVD_FOR` list. The cell floor is the only protection, and it is in §15 for ratification.

### 9.3 `K3` — corpus leakage

```text
TASK        predict the class of each (bundle, parameter) cell

CLASSIFIER  multinomial logistic regression, L2, C = 1.0,
            max_iter = 1000; scikit-learn version pinned at F3
            (Simple frozen probe by design: a tuned learner adds
             researcher degrees of freedom. A negative result means
             "no leakage detectable by THIS probe".)

FEATURES (61)
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
    scope ID one-hot 11

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

`parameter ID` and `scope ID` are admissible as features only because §5.1 makes class, parameter and scope mutually balanced. If any balance is relaxed, both must be dropped.

### 9.4 `K4` — atomicity
Tests `ATOM-1` and `ATOM-2` only. `ATOM-3` is outside `K4` by design and is claimed nowhere.

Defect history: v0.1 two parameters, v0.2 one, v0.3 three, v0.4 exclusivity for four, v0.5 canonical overlap in `E8b` plus scope-quantification in `E1`/`E8a`, v0.6 empirical non-separability of `E3`'s hierarchy. Seven forms so far: **hierarchy**, **conjunction**, **non-exhaustive enumeration**, **composition mistaken for conflict**, **canonical-form overlap**, **implicit quantification over signals**, and **enum disjoint on paper but not separable in the realized bundle**. A gate should test all seven against all eleven interrogatives.

### 9.5 `K5` — party independence
See §12. Fires if the parties cannot be staffed. That is the correct outcome, not an argument for relaxing the rule.

---

## 10. Condition table

Restatement of §8, not a parallel set of rules. Where tension is read into it, **§8 governs**.

```text
STAGE 1  K5 staffing | bank integrity | fidelity | K4 | K3 | K2 | K1
              |
              v
STAGE 2  cell floor >= 3/5 | parameter floor >= 25/30
         | semantic stability >= 24/30
              |
              v
         QUALIFIED_ON_CVD_FOR

TERMINAL STATES: BANK_INTEGRITY_NOT_ESTABLISHED (§5.5)
                 NOT_QUALIFIED (Stage 1 failure, prerequisite named)
DIAGNOSTICS (§9.2) are reported and never gate.
```

---

## 11. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §4, §6 |
| `F2` | Corpus design: class and scope assignment rules, per-parameter scope subsets, cap, item classes, bank schema and keying **(not contents)**, inventory requirement, exclusive sub-bank definition, incompatibility relation, `E3` structural constraint, placement rules, generator and validator scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — `K3` script, 61 features, 20 markers, seed and p formula, canonical serializer, model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | **Bank authored by the corpus party** — 330 entries against the frozen inventory |
| `F6` | **Role-aware back-translation; rejections removed; up to 3 rounds; bank frozen or terminal state** |
| `F7` | Ground-truth record authored and **sealed** (SHA-256) by the corpus party |
| `F8` | Bundles generated; byte-level fidelity check; `E3` structure check; CI assertions of §5.1 |
| `F9` | Leakage probe `K3` |
| `F10` | Adjudication, both channels |
| `F11` | Determinism re-run; metrics by the `F3` script; §8 decision function applied |

Staffing precedes bank authorship; back-translation precedes sealing, because the sealed truth is expressed in bank entries and a rejected entry would otherwise be sealed into gold.

---

## 12. Parties, and what counts as a gate

| # | Party | Role | May not also be |
|---|---|---|---|
| 1 | **Constructor** | Generation protocol, instrument, this document | any of 2–7 |
| 2 | **Corpus / reference-label party** | Authors the bank, authors and seals ground truth, runs the generator | any other |
| 3 | **Bank validator** | §5.4 role-aware back-translation, key-blind | any other |
| 4 | **Fidelity checker** | §5.7 byte-level check | any other |
| 5 | **Adjudicator A** | Blind adjudication | any other |
| 6 | **Adjudicator B** | Blind adjudication | any other |
| 7 | **Gate party** | Reviews and gates | any of 1–6 |
| 8 | *Reserve adjudicator* | Substitute for 5 or 6, disclosed | any of 1, 2, 3, 4, 7 |

**No permitted overlap.** The gate party may not be the fidelity checker — fidelity checking is execution, and a gate performing it would certify its own work. The bank validator may not adjudicate, having seen the bank and its keys.

**Excluded from parties 2–8, by name and by role:** Fable (constructor, S1 contributing reviewer); Sol (S1 instrument, sampling, calibration, decision-rule construction); Ivan (S1 construction, specification and ratification — retains L3 ratification, which is not an evaluative role, and is excluded from bank authorship, bank validation, fidelity checking, adjudication and gate); any agent that materially encoded S1 classifier or decision logic; and generally any actor materially involved in S1 as author, specifier, implementer of decision rules, or contributing reviewer.

### 12.1 Adversarial pre-gate review is not a gate

Reviews of this document produced by parties excluded under `K5` are recorded as:

```text
ADVERSARIAL_PRE_GATE_REVIEW
Reviewer: <party>
Independent-gate eligibility: NO
```

Such reviews are legitimate and valuable construction aid — every version of this document from v0.2 onward exists because of them. They **cannot satisfy the Stage 1 `K5` gate prerequisite**, and no `PASS` issued by an excluded party may be recorded as a gate verdict or merged as one. The independent gate is party 7, sees the candidate for the first time, and has no prior exposure to its construction.

This applies to the constructor's own confidence as well: this document has never been gated.

---

## 13. Declared limitations

**13.1 Statistical scope.** Failure-detection design, not estimation. No confidence intervals, no population estimates, no extrapolation to real deposits. No rate bound from `K1`.

**13.2 Domain and ecological transfer.** The CVD is template-generated from a frozen bank with entries inserted verbatim; answer spaces are closed by construction (`ATOM-3` not demonstrated); every `(bundle, parameter)` cell has exactly one scope, where a real deposit has many signals per parameter; and each parameter is exercised on only five scopes. Real deposits are longer, messier, and state facts in prose no bank contains. Qualification here may be a test of template recognition on a domain simpler than reality in at least four respects.

**Frozen consequence: `QUALIFIED_ON_CVD_FOR` does not license S3.** It prevents S3 from beginning with an instrument demonstrably broken on the listed parameters, on a simpler domain, and nothing more. Closing the gap requires a separate step on real material with its own freeze, not specified here.

**13.3 Bank meaning.** §5.4 establishes two-party agreement on five fields, not meaning itself. A misreading shared by corpus party and validator propagates into gold undetected.

**13.4 Prohibited outputs.** No verdict about any real deposit; no prevalence figure about documentation quality in any literature; no pooled single-number accuracy; no claim of real-domain exhaustiveness for any answer space; no confidence interval or population estimate; no claim of methodological novelty; no non-resolution figure without the §6.7 sentence; no statement of qualification without the §8.1 sentence; no use in S3 of any parameter outside `QUALIFIED_ON_CVD_FOR`; no gate verdict from a party excluded under §12.

---

## 14. L3 decisions

1. **Ratify or revise Stage 2 thresholds**: cell floor `≥ 3/5`, parameter floor `25/30`, semantic stability `24/30`. At `≥ 3/5` a parameter qualifies with 40% error on one class, and with no instrument-wide gate every parameter could sit there at once.
2. **Ratify `K1` as a global prerequisite**, knowing one fabrication in 660 adjudications terminates the run.
3. **Ratify the bank loop limits**: 3 rounds, 30% rejection ceiling, single-use entries, no re-keying.
4. **Staffing of seven (or eight) separated parties** — `K5`, binding on whether S2 runs.
5. **Corpus budget**: 330 single-use bank entries plus back-translation rounds, 30 bundles, 1320 adjudication events — or a reduced qualification.
6. **Publication status** of the qualification artifact, verbatim.
7. **BatteryLake manifest review** — `PRIOR_ART_ELIMINATION_v0.2.md` §6.
8. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`, and never yet gated. Self-contained; no earlier version normative. Written by a constructor with a declared S1 conflict whose atomicity rule has failed in every prior version of this document, in seven distinct forms. A gate should start at `K4` against all seven forms; at §4.2, where five applicable scopes per parameter were chosen because five makes the orthogonality arithmetic work and the scope lists were then filled to fit that number rather than derived from the parameters; and at §5.5, where the 30% rejection ceiling and the three-round limit are constructor policy with no analysis behind them.
