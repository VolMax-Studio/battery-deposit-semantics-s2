# S2 Candidate Specification v0.11 — Deposit Semantics Instrument Qualification

**Instance:** `battery-deposit-semantics-s2`
**Instance type:** `INTERNAL_QUALIFICATION` (ratified)
**Supersedes:** v0.1–v0.10 — retained as history, **none normative**. Self-contained.
**Constructor:** Claude ("Fable") — S1 contributing reviewer, conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Prior-art status:** governed by `PRIOR_ART_ELIMINATION_v0.2.md`
**Status:** `SPREMNO ZA GEJT` — requires a new G1 pass; not frozen, not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; L3 items in §15.

---

## 0. Provenance and authorized scope of this version

**Authorizing finding:** `G1-BLOCK-002`, returned by the external party-7 G1 gate against v0.10.

```text
G1-BLOCK-002
E8a coverage / scope-allocation inconsistency

VALID: YES

ROOT DEFECT:
The coverage rule assumed an exact number of standalone determining
parameter-cells per E8a scope that was not implied by the frozen F2
balancing constraints.

AUTHORIZED CHANGE (Route A, ratified by the operator):
- remove the false denominator assertion;
- add explicit F2 capacity constraints sufficient to realize E8a's
  frozen scope-partitioned coverage contract;
- add the corresponding CI assertion;
- record the defect in K4 history.

NOT AUTHORIZED:
- redesign the E8a interrogative;
- remove E8a;
- change thresholds;
- alter unrelated scope sets or coverage policy.
```

The arithmetic behind the finding: `E8a` has 15 `current` and 15 `voltage` parameter-cells across 6 classes. Row sums are 5, so each class carries `2/3` or `3/2`, and the column sum of 15 forces exactly three classes to carry three `current`. Which three is the `F2` solver's choice, so `POS-EXPLICIT + POS-BURIED` together yield **4, 5 or 6** `current` standalone determining parameter-cells. v0.10 asserted five.

| # | Change | Location |
|---|---|---|
| 1 | The false `5 + 5` denominator assertion for `E8a` removed; coverage requirement stated without assuming an allocation. | §5.2.2 |
| 2 | **Explicit `E8a` `F2` capacity constraints** added, satisfiable at every admissible allocation, plus the CI assertion. | §5.1, §5.2.2 |
| 3 | A **principle**, not a formula, for scope-dependent answer spaces in general. | §5.2.5 |
| 4 | `K4` history: twelfth form. | §9.4 |

Nothing else is changed from v0.10. `E8a`'s interrogative, its scopes, its enum, all thresholds, `K1`, the bank loop, the decision function, class assignment, `K3` and the party architecture are the v0.10 text.

**A general formula was considered and rejected.** The obvious rule — `standalone_determining_cells(parameter, scope) ≥ 2 × |legal categories for that scope|` — is correct for `E8a` because it is single-valued and one parameter-cell covers exactly one category. It overestimates required capacity for a future scope-dependent **set-valued** parameter, where one determining parameter-cell can cover several coverage categories at once. Freezing it would have generalised a single observation into a law that is wrong for a case the specification already admits. §5.2.5 states the principle instead and leaves the capacity derivation to each parameter's own scoring and coverage semantics.

---

## 1. What S2 measures

> Does the deposit-semantics adjudication instrument produce verdicts that are discriminating against known ground truth, stable under adjudicator substitution, and deterministic on re-run — **for which parameters, on which evidence strata, and on what domain**?

S2 measures the instrument on a **constructed validation domain (CVD)**. It touches no real deposit, emits no statement about any dataset, no prevalence figure, no methodological novelty claim.

Ground truth is written before the documentary artifact, because an adjudication instrument cannot be validated on labels produced by adjudication. Established paradigm, not a contribution.

---

## 2. Documentary space

`D` is an exhaustive ordered manifest per unit; each entry carries generation ID, timestamp, SHA-256, media type, stratum tag.

| Stratum | Contents | Proposition it supports |
|---|---|---|
| `S-DOC` | Article-style text, README, data dictionary, declared prose | *The depositor stated a rule.* |
| `S-FILE` | Declared in-file labels: column names, header rows, declared unit strings, explicit legend or comment lines | *The file declares a property.* |

Strata are **not ranked**. The verdict records which stratum carried it, and §5.2 requires both to be exercised.

---

## 3. Atomicity and scope tests

| Test | Statement | Status |
|---|---|---|
| `ATOM-1` | Exactly one interrogative per parameter, at a fixed scope, with a stable referent for every applicable scope. | Required. Tested by `K4`. |
| `ATOM-2` | Answer space mutually exclusive and exhaustive **over the CVD**, no two canonical forms expressing the same fact, and **empirically separable in every realized bundle**. | Required. Tested by `K4`. |
| `ATOM-3` | Answer space exhaustive over the real semantic domain. | **NOT DEMONSTRATED AND NOT CLAIMED.** |
| `SCOPE-1` | Applicable scopes derived from the interrogative's semantics before any balancing construction. | Required. Tested by `K4`. |
| `SCOPE-2` | For every applicable scope, the answer space contains at least two values legal for that scope. | Required. Tested by `K4`. |

**Composition is not ambiguity.** Several simultaneously true mechanisms are one reading whose `semantic_value` is a **set**, verdict `EXPLICIT_*`. Ambiguity is two or more **mutually incompatible** readings, verdict `AMBIGUOUS`, incompatibility established only by §5.7.

### 3.1 `SCOPE-1` — frozen

```text
Applicable scopes are derived from the interrogative's semantics
before any balancing or orthogonality construction.

Arithmetic may select among semantically admissible scopes.
Arithmetic may not create semantic admissibility.
```

### 3.2 `SCOPE-2` — frozen

```text
For every applicable scope of a parameter, the CVD answer space must
contain at least two values that are legal for that scope.

A scope with zero legal values compels nonsensical gold.
A scope with exactly one legal value makes the answer derivable from
the scope, so the parameter-cell measures nothing: a value error
becomes impossible and AMBIG-CONSTRUCTED becomes unconstructible.
```

`SCOPE-1` asks whether the question makes sense for the scope. `SCOPE-2` asks whether the *answer* can vary given the scope. The two failure modes look identical from inside `SCOPE-1`.

Minimum legal values per scope, all eleven parameters: `E1` 2, `E2` 2, `E3` 4, `E4a` 3, `E4b` 4, `E5` ≥4 base members, `E6` 4, `E7a` 4, `E7b` 4, `E8a` 2, `E8b` 3 (scope-independent). All pass.

`E8a` is the only parameter whose answer space is scope-dependent: every other parameter asks what convention was applied to a signal, and conventions vary independently of which signal it is, while `E8a` asks what the signal is measured in, which is partly determined by the signal.

---

## 4. Parameters and scopes

### 4.1 The eleven parameters

| ID | Interrogative (at the parameter-cell's scope) | Canonical answer (CVD-closed) |
|---|---|---|
| `E1` | Which sign of this signal denotes charge? | `polarity ∈ {charge_positive, discharge_positive}` |
| `E2` | Does a zero in this signal denote a measured value or a placeholder for an unrecorded value? | `zero_meaning ∈ {measured, placeholder}` |
| `E3` | What is the **finest** operational boundary at which this cumulative quantity resets to zero? | `finest_reset_boundary ∈ {step, cycle, test, never}` |
| `E4a` | Does this signal's interval timestamp denote start, end, or midpoint? | `timestamp_position ∈ {start, end, midpoint}` |
| `E4b` | Which endpoint convention governs this signal's intervals? | `endpoint_convention ∈ {closed_closed, open_open, closed_open, open_closed}` |
| `E5` | What rule governs the interval between logged records of this signal? | **set**, non-empty, over `{fixed(interval_seconds), event_driven(delta_voltage), event_driven(delta_current), event_driven(step_transition)}` |
| `E6` | By what rule is the absence of unlogged gaps in this signal established? | **set**, non-empty, over `{completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation}` |
| `E7a` | By what rule does a record map to this operation identifier? | **set**, non-empty, over `{explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker}` |
| `E7b` | By what rule is operational state (charge / discharge / rest) encoded in a record? | **set**, non-empty, over `{step_type_column, current_sign, separate_state_column, mode_code_enum}` |
| `E8a` | In what physical unit is this signal reported? | `unit ∈ {A, mA, V, mV}` |
| `E8b` | What scaling was applied to this signal? | `scaling ∈ {none, factor, affine}` with `factor_value`, `offset_value` — §4.3 |

`E8a`: `A` and `mA` are legal for `current`, `V` and `mV` for `voltage`. Two legal values per scope satisfies `SCOPE-2` and keeps `AMBIG-CONSTRUCTED` constructible (`A` against `mA`, `V` against `mV`). The real unit space is far larger; that is an `ATOM-3` matter and is not claimed (§13.2).

### 4.2 Scope vocabulary and semantics-first subsets

Frozen vocabulary: `current`, `voltage`, `power`, `capacity_charge`, `capacity_discharge`, `energy`, `temperature`, `time`, `step_index`, `cycle_index`, `test_index`, `dataset`.

| Parameter | Semantic admissibility criterion | Applicable scopes | s |
|---|---|---|---|
| `E1` | A signed, bidirectional instantaneous signal | current, power | 2 |
| `E2` | A measured instantaneous signal in which zero is a possible reading | current, voltage, power, temperature | 4 |
| `E3` | An accumulating quantity that can reset | capacity_charge, capacity_discharge, energy, time | 4 |
| `E4a` | A signal whose records aggregate over an interval | current, voltage, power, temperature | 4 |
| `E4b` | As `E4a` | current, voltage, power, temperature | 4 |
| `E5` | A logged signal with a record cadence | current, voltage, power, temperature | 4 |
| `E6` | As `E5` | current, voltage, power, temperature | 4 |
| `E7a` | An operation identifier | step_index, cycle_index, test_index | 3 |
| `E7b` | **None — the question is asked once of the dataset** | dataset | 1 |
| `E8a` | A quantity for which the CVD enum offers **≥ 2** legal units (`SCOPE-2`) | current, voltage | 2 |
| `E8b` | Any reported quantity | current, voltage, power, capacity_charge, capacity_discharge, energy, temperature, time | 8 |

Balance feasibility at these cardinalities, checked against §5.1:

- **`E8a`, `s = 2`**: 6 classes × 2 scopes, row sums 5, column sums 15. Cells lie in `{2, 3}`, so `max − min = 1`; exactly three classes carry three `current`. Every scope sees all six classes; every class sees both scopes. **Which three classes carry three is the solver's choice**, which is the fact v0.10 assumed away — see §5.2.2.
- **`E8b`, `s = 8`**: 6 × 8 table, 30 units, row sums 5, column sums 4,4,4,4,4,4,3,3; cells lie in `{0, 1}`, `max − min = 1`. Every class sees five distinct scopes; every scope sees three or four distinct classes.

### 4.3 Canonical-form disjointness and empirical separability (`ATOM-2`)

**`E8b`:**

```text
none    factor_value = 1  AND offset_value = 0
factor  factor_value != 1 AND offset_value = 0
affine  offset_value != 0 (factor_value unrestricted)
```

**`E5`** — the trigger set contains no time-based trigger, so a fixed cadence cannot also be expressed as `event_driven`. Adding one later is prohibited without a new freeze.

**`E3`** — every bundle carrying an `E3` parameter-cell, of any class, must declare a structure in which:

```text
at least one cycle contains >= 2 steps     separates step from cycle
at least one test  contains >= 2 cycles    separates cycle from test
the data contains  >= 2 tests              separates test from never
```

**`E4a` / `E4b`** — every bundle carrying an `E4a` or `E4b` parameter-cell must declare records aggregating over an interval of **strictly positive duration**. In a degenerate zero-length interval, `start`, `midpoint` and `end` coincide and the enum collapses in the realized bundle however clean it looks on paper.

The `F2` validator enforces these structures; the `F8` fidelity check verifies the bundle declares them.

**Provenance disclosure, mandatory in the frozen preregistration.** The cadence / coverage distinction (`E5`/`E6`) was first named by the S1 reviewer after the S1 outcome was known, and that reviewer authored this document. It is retained because uniform application of `ATOM-1` has forced four splits — `E2`/`E7b`, `E4a`/`E4b`, `E7a`/`E7b`, `E8a`/`E8b` — not one.

---

## 5. Corpus

### 5.1 Parameter-cells, class, scope

```text
30 bundles x 11 parameters = 330 parameter-cells
Per parameter: 30 parameter-cells, 5 in each of 6 classes

CLASS   class(i, j) = (i + j) mod 6     i = 0..29, j = 0..10   (closed form, frozen)
SCOPE   frozen explicit table, produced at F2 by a constraint-satisfying
        script, NOT a closed form
```

Scope counts are heterogeneous (`s` from 1 to 8), so no closed form gives exact class×scope balance: at 30 parameter-cells per parameter, exact balance requires `6·s | 30`, which holds only for `s ∈ {1, 5}`.

**Frozen scope-assignment constraints**, satisfied by the `F2` script and asserted by CI:

```text
for every parameter:            class counts == [5,5,5,5,5,5]          (exact)
for every parameter:            scope counts differ by at most 1
for every parameter:            class x scope table: max cell - min cell <= 1
for every parameter with s > 1: no scope occurs with fewer than 2 distinct classes
for every parameter with s > 1: no class occurs with fewer than 2 distinct scopes
for every bundle:               max class count <= 3
for every (parameter, fold):    class counts == [1,1,1,1,1,1]
for every (bundle, parameter):  exactly one scope, from that parameter's
                                applicable set
for every (parameter, scope):   the answer space admits >= 2 legal values
                                (SCOPE-2, §3.2)

COVERAGE FEASIBILITY (E8a, frozen; see §5.2.2)
  Among the 10 standalone determining parameter-cells of E8a
  (the POS-EXPLICIT and POS-BURIED classes):
    count(scope = current) >= 4
    count(scope = voltage) >= 4
```

Exact class balance is retained because `K3`'s null (`p0 = 1/6`) and the Stage 2 class-score floor both depend on it. The `(parameter, fold)` assertion depends only on the class closed form.

**Declared consequence.** For `E8b`, 30 parameter-cells over 8 scopes and 6 classes leaves most of the 48 `(class, scope)` combinations untested: breadth without depth. For `E7b` and `E8a`, the reverse. See §13.2.

### 5.2 Frozen coverage contract

A corpus party could otherwise make nearly every determinate `E8b` parameter-cell `scaling = none`, leave `factor` and `affine` to appear only inside `AMBIG-CONSTRUCTED` pairs, and the instrument would collect `QUALIFIED_ON_CVD_FOR: E8b` without ever having extracted a standalone affine transformation. The same held for evidence strata.

#### 5.2.1 Two terms, frozen

```text
CANONICAL SEMANTIC VALUE
  The full typed value that is SCORED under §6.2, including any
  numeric payload. factor(2) and factor(3) are different canonical
  semantic values. fixed(10 s) and fixed(30 s) are different
  canonical semantic values.

COVERAGE CATEGORY
  The frozen categorical branch of the answer space, used ONLY for
  minimum-coverage accounting in §5.2.2. factor(2) and factor(3)
  are the SAME coverage category. fixed(10 s) and fixed(30 s) are
  the SAME coverage category.
```

Coverage is accounted in categories. Scoring is on canonical semantic values. The two are never interchanged, and no `[L1]` sentence in this document may use "canonical value" to mean the category.

**Frozen coverage categories per parameter:**

| Parameter | Coverage categories | Count |
|---|---|---|
| `E1` | charge_positive, discharge_positive | 2 |
| `E2` | measured, placeholder | 2 |
| `E3` | step, cycle, test, never | 4 |
| `E4a` | start, end, midpoint | 3 |
| `E4b` | closed_closed, open_open, closed_open, open_closed | 4 |
| `E5` | fixed, event_driven(delta_voltage), event_driven(delta_current), event_driven(step_transition) | 4 |
| `E6` | completeness_counter, expected_count_comparison, gap_flag_column, acquisition_log_reconciliation | 4 |
| `E7a` | explicit_index_column, filename_encoding, time_segmentation_rule, row_grouping_marker | 4 |
| `E7b` | step_type_column, current_sign, separate_state_column, mode_code_enum | 4 |
| `E8a` | A, mA, V, mV | 4 |
| `E8b` | none, factor, affine | 3 |

For set-valued parameters (`E5`, `E6`, `E7a`, `E7b`), a coverage category is a **base-enum member**, and a gold set covers every category whose member it contains.

#### 5.2.2 Requirements

Each parameter has **10 standalone determining parameter-cells** (5 `POS-EXPLICIT` + 5 `POS-BURIED`). Frozen requirements on those 10:

| Requirement | Rule |
|---|---|
| **Category coverage** | Every **coverage category** appears in **≥ 2** standalone determining parameter-cells. |
| **Composition coverage** | For set-valued parameters, **≥ 2** standalone determining parameter-cells have a gold set of size ≥ 2. |
| **Stratum coverage** | **≥ 2** standalone determining parameter-cells are `S-FILE` and **≥ 2** are `S-DOC`. |

Arithmetic against the budget of 10, in categories: `E1` 4, `E2` 4, `E3` 8, `E4a` 6, `E4b` 8, `E8a` 8, `E8b` 6; set-valued `2 × 4 + 2 = 10`. All fit; the four set-valued parameters fit exactly.

**`E8a`, scope-partitioned.** Because `E8a`'s categories are scope-restricted, its requirement is stated per scope and **makes no assumption about how many standalone determining parameter-cells each scope receives**:

```text
Among the standalone determining parameter-cells whose scope is current:
  A  occurs in >= 2
  mA occurs in >= 2

Among the standalone determining parameter-cells whose scope is voltage:
  V  occurs in >= 2
  mV occurs in >= 2

The F2 scope-assignment solver MUST satisfy the §5.1 COVERAGE FEASIBILITY
constraints in addition to the general §5.1 balance constraints.
```

v0.10 stated this as "≥ 2 of the five … whose scope is `current`" and justified it with "both are 4 ≤ 5". The `5 + 5` split was assumed, not implied: the admissible allocations are `4/6`, `5/5` and `6/4`, and the solver chooses.

**Feasibility, and the zero-slack case.** The `≥ 4` constraints in §5.1 are in fact implied by the balance — every admissible allocation gives each scope at least 4 — and they are frozen explicitly anyway, because inferring feasibility from marginal balance is precisely the defect `G1-BLOCK-002` named. `[L2]` In the worst admissible allocation, the scope receiving 4 has **exactly** `2 + 2` slots and no slack: the `F2` unit assignment for that scope is then forced, and a single misassignment makes the coverage contract unsatisfiable rather than merely tight. The `F2` script must therefore treat unit assignment as part of the constraint problem, not as a free choice made after scopes are allocated.

#### 5.2.3 Numeric-payload diversity is not required

Two parameters carry a numeric payload inside the scored value: `E5` (`interval_seconds`) and `E8b` (`factor_value`, `offset_value`). **The coverage contract places no requirement on how many distinct numeric payloads appear.**

Stated consequence: a parameter may reach `QUALIFIED_ON_CVD_FOR` having only ever been asked to extract `fixed(10 s)` and `factor(2)`. Nothing in S2 would then demonstrate that the instrument reads numeric payloads correctly across magnitudes, decimal forms, or negative offsets, even though §6.2 scores those payloads for exact equality and §6.6 defines their serialization in detail.

This gap is deliberately left open rather than closed with an invented threshold. Surfaced in §15 as an L3 decision.

#### 5.2.4 Stratum exemption

If `S-FILE` evidence is not plausibly constructible for a parameter, the corpus party may declare the exemption **at `F2`, in writing, before any bank entry exists**, and that parameter's result is reported as:

```text
QUALIFIED_ON_CVD_FOR: E3 (S-DOC only)
```

An exemption declared after `F2` is not admissible; the parameter fails `K4`'s coverage check instead.

#### 5.2.5 Principle for scope-dependent answer spaces — frozen

```text
For any scope-dependent answer space, F2 MUST verify that the realized
standalone determining allocation is sufficient to satisfy the frozen
coverage contract for every applicable scope.

The required capacity is derived from that parameter's scoring and
coverage semantics; it is not inferred from marginal balance alone.
```

The §5.1 `COVERAGE FEASIBILITY` block is the concrete instance of this principle for `E8a`, the only scope-dependent parameter in the current set.

No general capacity formula is frozen. `2 × |legal categories for that scope|` is correct for a single-valued parameter, where one parameter-cell covers exactly one category, and overestimates for a scope-dependent **set-valued** parameter, where one determining parameter-cell can cover several categories at once. Deriving such a formula from the single case at hand would repeat the error pattern this version exists to fix.

### 5.3 Bank metadata — semantic and placement, separated

`class` **cannot** be reconstructed from an entry's text: `POS-EXPLICIT` and `POS-BURIED` differ only in placement, and for a single-valued parameter an `AMBIG-CONSTRUCTED` entry is an ordinary determining statement whose ambiguity arises from the *pair*, not the sentence.

```text
SEMANTIC BANK METADATA   — validated by back-translation (§5.4)
  parameter
  scope
  evidence_stratum       S-DOC | S-FILE
  semantic_role          determining | non_determining_adjacent | non_applicable
  semantic_value         REQUIRED iff semantic_role = determining, else MUST be null
  exclusive_assertion    true | false; may be true only for determining entries
                         of set-valued parameters; MUST be false otherwise

CORPUS PLACEMENT METADATA — never validated by back-translation
  class
  placement              prominent | buried | absent
  bundle / parameter-cell assignment
```

Every entry text must name its scope's signal explicitly (`dataset`-scoped entries name the dataset). This binds evidence to scope in §6.3.

### 5.4 Role-aware back-translation

The validator receives entry texts **shuffled, stripped of all metadata**, plus the frozen interrogatives, answer enums, stratum definitions and scope vocabulary, and returns the **six semantic fields** of §5.3 for each text. All six must match the authored semantic metadata; any mismatch rejects the entry. `class` and `placement` are never asked.

**Declared limitation:** a two-party agreement check on six fields, not a proof of meaning. A misreading shared by corpus party and validator propagates into gold undetected (§13.3).

The validator has seen the bank and is excluded from adjudication (§12).

### 5.5 Bank inventory and single use

Per parameter: 5 `POS-EXPLICIT` + 5 `POS-BURIED` + 5 `NEG-ADJACENT` + 10 (`AMBIG`, two each) + 5 `NA` = **30 entries**; `NEG-ABSENT` parameter-cells require none.

```text
I = 30 x 11 = 330 required entries
Every entry is used exactly once in the corpus. No reuse.
```

Single use forces 330 distinct texts and makes "recycle one very obvious template" structurally impossible. `K3` does not measure lexical diversity, so the constraint is imposed rather than tested for.

**Stated cost:** 330 distinct entries authored by one party and independently back-translated by another, with up to two replacement attempts each. The largest single work item in S2; in §15 for budget ratification.

### 5.6 Loop termination — byte-unambiguous

```text
SLOT              a required (parameter, scope, class, semantic_role,
                  semantic_value, exclusive_assertion, evidence_stratum) entry
ATTEMPTS          1 initial attempt + at most 2 replacement attempts per slot
                  A slot whose 3rd attempt is rejected -> terminal state

R_total           cumulative count of rejected attempts, all slots, all rounds
CEILING           R_total > floor(0.30 x I) = floor(0.30 x 330) = 99
                  -> terminal state, immediately, no further attempts

REPLACEMENT       must target the identical slot. The corpus party may not
                  substitute an easier value, drop a scope, change stratum,
                  or re-key an entry.

TERMINAL STATE    BANK_INTEGRITY_NOT_ESTABLISHED
                  S2 does not proceed.
```

The denominator is the **required inventory `I`**, fixed at 330 before any authoring, so the ceiling is the constant **99** and cannot drift with the number of attempts made.

`[L2]` A terminal state here is informative: it says the vocabulary cannot be expressed unambiguously even in purpose-built prose. The values `3` and `0.30` are constructor policy with no analysis behind them and are in §15.

### 5.7 Frozen incompatibility relation

- **Single-valued parameters** (`E1`, `E2`, `E3`, `E4a`, `E4b`, `E8a`, `E8b`): any two distinct canonical semantic values **legal for the same scope** are incompatible, by `ATOM-2`. `SCOPE-2` guarantees at least two such values exist for every applicable scope, which is what makes `AMBIG-CONSTRUCTED` constructible for every parameter.
- **Set-valued parameters** (`E5`, `E6`, `E7a`, `E7b`): different sets are **not** incompatible by default — they may compose. Incompatibility requires both entries to carry `exclusive_assertion = true`, independently confirmed by back-translation, and their value sets to differ.

The `F2` validator rejects any `AMBIG-CONSTRUCTED` parameter-cell whose two entries do not satisfy this.

### 5.8 Generation and byte-level fidelity

Bundles are **generated, not written**: a frozen template engine inserts bank entries **verbatim, no paraphrase**, placement under frozen rules and a frozen seed. The generator emits a realization index.

The fidelity checker receives the bundle bytes and the frozen bank, and **not** the realization index as an authority:

1. Search bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences and byte spans.
3. The derived record must equal the sealed record byte-identically.
4. For every `NEG-ABSENT` parameter-cell: **no** determining entry for that `(parameter, scope)` — of any value — occurs anywhere in the bundle.
5. For every `NEG-ADJACENT` parameter-cell: the present entry is the keyed adjacent entry and no determining entry for that `(parameter, scope)` occurs.
6. Every bundle carrying an `E3` parameter-cell declares the §4.3 structure; every bundle carrying an `E4a`/`E4b` parameter-cell declares a strictly positive interval length.
7. The realization index is a cross-check only. **Index–bytes disagreement halts at `F8`.**

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

`note_text` is **prohibited** during the qualification run and must be absent: as unscored free text it could fail `K2` on a re-worded note alone, and it gave the adjudicator an unscored channel for reasoning the instrument does not evaluate.

`readings` sorted lexicographically by canonical serialization of `semantic_value`; set values themselves canonically sorted.

| Verdict class | Meaning | `readings` |
|---|---|---|
| `EXPLICIT_DOC` | A located `S-DOC` passage states the rule | exactly 1, `S-DOC` |
| `EXPLICIT_FILE` | A **declared** `S-FILE` label determines it | exactly 1, `S-FILE` |
| `AMBIGUOUS` | Two or more readings incompatible under §5.7 | ≥ 2 |
| `ABSENT` | Exhaustive traversal found no determining evidence | 0 |
| `NOT_APPLICABLE` | No data of the governed kind | 0 |

**`EXPLICIT_FILE` is narrow.** Admissible: column names, header rows, declared unit strings, explicit legend or comment lines. **Inadmissible: value patterns** — deriving a sign convention from the relation between current sign and a state-of-charge trend is domain inference, and admitting it would restore through `S-FILE` the inference removed by deleting `INFERABLE`. This is the sharpest deliberate difference from published prior art, which permits value statistics to bind columns.

### 6.2 Correctness

A parameter-cell is correct iff all of: **scope** matches gold exactly; **`verdict_class`** matches gold; **`semantic_value`** matches gold as a **canonical semantic value** (§5.2.1) — field-wise, sets by exact set equality, numeric payloads by exact equality after §6.6; **evidence support** holds for every reading (§6.3); **traversal obligations** hold for `ABSENT` and `NOT_APPLICABLE` (§6.4).

Coverage categories play no part in scoring.

### 6.3 Evidence checks, per reading

- **`EVIDENCE_INVALID`** — `verbatim_excerpt` does not occur byte-exactly in the artifact named by `artifact_sha256`. The citation is invented. **Counts under `K1`, zero tolerance, global.**
- **`EVIDENCE_UNSUPPORTED`** — the excerpt occurs but does not **contain, byte-exactly and in full**, the bank entry keyed for `(parameter, scope, semantic_value)` in that bundle. Parameter-cell incorrect; counted and reported separately; no zero-tolerance gate of its own.

Generous in the safe direction: quote more context than the determining sentence, never less. For `AMBIGUOUS` the check runs per reading.

`[L2]` This remains a proxy for evidence→claim validity: it tests that the adjudicator cited the scope-specific passage carrying the fact, not that it understood why. §5.4 stands behind the bank keys, with residual risk in §13.3.

### 6.4 `ABSENT` and `NOT_APPLICABLE`

- **`ABSENT`** correct only if `traversal_record` lists **every entry of that bundle's manifest `D`**, each marked examined. Failure: `TRAVERSAL_INCOMPLETE`.
- **`NOT_APPLICABLE`** correct only if `traversal_record` carries a `verbatim_excerpt` occurring byte-exactly in the named artifact and containing, in full, the keyed non-applicability entry for that `(parameter, scope)`. Failure: `JUSTIFICATION_UNSUPPORTED`.

### 6.5 Error directions
Over-claim (`NEG-ABSENT` → `EXPLICIT_*`/`AMBIGUOUS`; `NEG-ADJACENT` → `EXPLICIT_*`; `AMBIG-CONSTRUCTED` → `EXPLICIT_*`); under-claim (`POS-*` → `ABSENT`); scope error; value error; grounding error; stratum error. All reported separately. Over-claim corrupts instrument integrity; under-claim is the direction that would inflate a future non-resolution figure.

### 6.6 Canonical numeric serialization (frozen)
Decimal only, never exponent; integers with no decimal point and no trailing zeros; non-integers to 6 significant digits, trailing zeros stripped; no leading `+`; single leading `-`; no thousands separators. So `10`, `10.0` and `1e1` are one byte value. Applies to `interval_seconds`, `factor_value`, `offset_value`, and every numeric field in gold and output alike.

### 6.7 Declared direction of conservatism
The restricted vocabulary is intentionally conservative relative to expert-assisted interpretation and may increase observed non-resolution. **No mathematical upper-bound interpretation follows from this design alone** — the instrument can err in both directions. Frozen; reproduced in any S2 or S3 output reporting a non-resolution figure.

---

## 7. Adjudication protocol

**Channels.** Two primary adjudicators, independent; one reserve, unused unless a primary becomes unavailable, substitution disclosed.

**Blinding.** Each receives the pinned bundle manifest — including the parameter-cell's scope — and the frozen §2–§6 text. Nothing else: not ground truth, not item class, not the bank, not the realization index, not corpus composition, not the other's output, not §8.

**Disagreement.** Frozen before any disagreement is observed: **disagreements are not resolved.** They are recorded and located.

**Determinism.** Both adjudicators re-run all 330 parameter-cells. Canonical serializer: fixed field order and encoding, §6.6 numerics, no timestamps, no run IDs, no model-version strings in the record; `note_text` absent by §6.1. Model identity, version and sampling settings frozen at `F3`, in a sidecar. Proof: rename output, re-run, file must be **recreated** byte-identical.

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
| Bank integrity | §5.4 back-translation agrees on all six fields for 100% of retained entries, within §5.6 limits |
| Coverage | §5.2.2 category, composition and stratum requirements met, including the `E8a` scope-partitioned form; exemptions declared at `F2` only |
| Fidelity | §5.8 byte-level re-derivation match, 100% |
| `K4` | `ATOM-1`, `ATOM-2`, `SCOPE-1`, `SCOPE-2` hold for all eleven parameters, pre-freeze |
| `K3` leakage | Probe does not fire (§9.3) |
| `K2` determinism | Both adjudicators reproduce byte-identically |
| `K1` fabrication | **Zero events, either adjudicator, any parameter-cell** (§9.1) |

**`K1` is global, not per-parameter.** Fabrication is a property of the adjudicator, not of the parameter. **Stated consequence, for ratification:** with 660 primary adjudications and zero tolerance, one fabrication anywhere terminates the run. `[L2]` `NOT_QUALIFIED` is the more likely first outcome; that is an informative result, not a wasted run.

`K2`, `K3`, `K4`, coverage, fidelity and bank integrity are global for a different reason: each invalidates the *measurement* rather than the adjudicator.

### Stage 2 — Per-parameter membership

Evaluated only if Stage 1 passes in full. Terms:

```text
parameter-cell   one (bundle, parameter) test instance; 330 in the corpus
class score      the number of correct parameter-cells among the five
                 belonging to a (parameter, class) pair; range 0..5
```

For parameter `p`, both adjudicators must satisfy:

| Condition | Rule |
|---|---|
| **Class-score floor** | Every `(p, class)` **class score** is **≥ 3 of 5** |
| **Parameter floor** | ≥ **25 of 30** parameter-cells correct, per §6.2 |
| **Semantic stability** | ≥ **24 of 30** parameter-cells agree on `(scope, verdict_class, semantic_value set)` |

Nothing else determines membership. **Stability is semantic only**; evidence concordance is a diagnostic (§9.2), because two adjudicators quoting two different valid sentences for the same fact is not instability of the verdict.

### 8.1 Output form

```text
QUALIFIED_ON_CVD_FOR:     [parameter ids, with (S-DOC only) where §5.2.4 exempted]
NOT_QUALIFIED_ON_CVD_FOR: [parameter ids, each with the failing condition]
```

**Frozen sentence, mandatory wherever the result is stated:**

> Qualification is demonstrated on the frozen constructed validation domain only. It is not a claim that the instrument is qualified for this parameter on real deposit documentation.

---

## 9. Kill conditions and diagnostics

### 9.1 `K1` — fabrication
Fires on: `EXPLICIT_DOC`, `EXPLICIT_FILE` or `AMBIGUOUS` on a parameter-cell whose gold class is `NEG-ABSENT`; or any `EVIDENCE_INVALID` reading, any parameter-cell, any class. Permitted count **0**, global. No rate bound is reported — the parameter-cells share bundles, parameters, scopes and a single adjudicator and are not independent trials.

### 9.2 Reported diagnostics — never gating
Per-class correct counts out of 55 per adjudicator; instrument-wide semantic agreement out of 330; **evidence concordance** among semantically agreeing parameter-cells; counts of `EVIDENCE_UNSUPPORTED`, `TRAVERSAL_INCOMPLETE`, `JUSTIFICATION_UNSUPPORTED`, scope errors, stratum errors; per-coverage-category and per-stratum correct counts, limited by the numeric-payload gap of §5.2.3; and the model-free correlated-error decomposition (`both correct` / `both wrong, identical readings` / `both wrong, different readings` / `exactly one correct`).

**Stated trade.** There is no instrument-wide discrimination gate. All eleven parameters could sit at the `3/5` class-score floor on `POS-BURIED` and every one still qualify. The class-score floor is the only protection, and it is in §15.

### 9.3 `K3` — corpus leakage

```text
TASK        predict the class of each parameter-cell

CLASSIFIER  multinomial logistic regression, L2, C = 1.0, max_iter = 1000
            scikit-learn version pinned at F3
            (Simple frozen probe by design. A negative result means
             "no leakage detectable by THIS probe".)

FEATURES (62)
  per component (article / README / CSV header):
    character count 3 | line count 3 | digit ratio 3 | punctuation 3
  bundle-level:
    article heading count 1 | README section count 1
    CSV header column count 1
    mean sentence length (article, README) 2
    type-token ratio (article, README) 2
      tokenization: whitespace, lowercased, no stemming
    formatting-marker presence flags 20
  parameter-cell level:
    parameter ID one-hot 11 | scope ID one-hot 12

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

PREPROCESSING  numeric features standardized on training-fold statistics
               only; no imputation

FOLDS       unit = bundle; all 11 parameter-cells of a bundle in one fold
            bundles sorted by ID; fold = index mod 5
            5 folds x 6 bundles = 30 bundles = 330 parameter-cells
            deterministic; no shuffling

NULL        p0 = 1/6, uniform by the §5.1 exact class balance

STATISTIC   A_obs = mean CV multiclass accuracy over 330 held-out
            parameter-cells

TEST        permutation, N = 2000, seed 20260912
            unit: a bundle's whole 11-parameter-cell class vector,
            permuted across bundles; full CV re-run per permutation
            parameter-cell-level permutation PROHIBITED
            p = (1 + #{A_perm >= A_obs}) / (1 + N)

FIRES IF    p < 0.01
```

**On the scope feature.** The protection against scope→class association is the §5.1 CI assertion on the class×scope table. The `K3` scope feature is a weak additional sensor only.

`parameter ID` and `scope ID` are admissible as features only because §5.1 constrains class against both. If any of those constraints is relaxed, both features must be dropped.

### 9.4 `K4` — atomicity, scope semantics, coverage
Tests `ATOM-1`, `ATOM-2`, `SCOPE-1`, `SCOPE-2`, and §5.2.2 coverage including the `E8a` scope-partitioned form and its §5.1 feasibility constraints. `ATOM-3` is outside `K4` by design and is claimed nowhere.

Defect history: v0.1 two parameters; v0.2 one; v0.3 three; v0.4 exclusivity for four; v0.5 canonical overlap in `E8b` plus scope-quantification in `E1`/`E8a`; v0.6 empirical non-separability of `E3`'s hierarchy; v0.7 cardinality-first scope assignment and non-uniform separability for `E4a`; v0.8 a coverage rule stated over "canonical values" but counted over categories; **v0.9 `E8a` scopes with zero or one legal answer value — found by the external G1 gate**; **v0.10 `E8a` coverage feasibility inferred from marginal balance rather than constrained explicitly — also found by the external G1 gate.**

Twelve forms: **hierarchy**, **conjunction**, **non-exhaustive enumeration**, **composition mistaken for conflict**, **canonical-form overlap**, **implicit quantification over signals**, **enum disjoint on paper but not separable in the realized bundle**, **scope admissibility created by arithmetic**, **a separability standard stated generally but applied to one parameter**, **one term carrying two meanings across scoring and accounting**, **an answer derivable from the scope**, and **coverage feasibility inferred from balance rather than constrained explicitly**.

`[L2]` The twelfth form is the general lesson of the last two rounds: two constraint systems — scope allocation and coverage — were each individually valid, and their **joint satisfiability was never frozen**. Both were found by a party outside the construction loop, in the same region of the specification, after internal sweeps that claimed to have checked it. A gate should weigh the internal defect-detection record accordingly and should look for other places where two frozen constraint systems meet without their conjunction being asserted.

### 9.5 `K5` — party independence
See §12. Fires if the parties cannot be staffed.

---

## 10. Condition table

Restatement of §8. Where tension is read into it, **§8 governs**.

```text
STAGE 1  K5 | bank integrity | coverage | fidelity | K4 | K3 | K2 | K1
              |
              v
STAGE 2  class-score floor >= 3/5 | parameter floor >= 25/30
         | semantic stability >= 24/30
              |
              v
         QUALIFIED_ON_CVD_FOR

TERMINAL STATES: BANK_INTEGRITY_NOT_ESTABLISHED (§5.6)
                 NOT_QUALIFIED (Stage 1 failure, prerequisite named)
DIAGNOSTICS (§9.2) are reported and never gate.
```

---

## 11. Freeze and execution order

No stage begins before every prior stage is merged to `main` by the operator.

| Stage | Content |
|---|---|
| `F1` | Instrument text: §2, §3, §4, §6 |
| `F2` | Corpus design: class closed form, scope-assignment table and constraint script **including the §5.1 coverage-feasibility constraints and the unit assignment for `E8a`**, per-parameter scope subsets, `SCOPE-2` verification, cap, item classes, coverage contract with frozen category lists and any stratum exemptions in writing, bank semantic/placement schemas, inventory, exclusive sub-bank definition, incompatibility relation, `E3` and `E4` structural constraints, placement rules, generator and validator scripts |
| `F3` | Protocol and decision rules: §7, §8, §9 — `K3` script, 62 features, 20 markers, seed and p formula, canonical serializer, model/sampling sidecar spec |
| `F4` | Roles ratified and staffed (`K5`) |
| `F5` | Bank authored by the corpus party — 330 entries against the frozen inventory |
| `F6` | Role-aware back-translation; rejections removed; §5.6 limits; bank frozen or terminal state |
| `F7` | Ground-truth record authored and **sealed** (SHA-256) by the corpus party |
| `F8` | Bundles generated; byte-level fidelity; `E3`/`E4` structure checks; CI assertions of §5.1; coverage verification |
| `F9` | Leakage probe `K3` |
| `F10` | Adjudication, both channels |
| `F11` | Determinism re-run; metrics by the `F3` script; §8 decision function applied |

---

## 12. Parties, and what counts as a gate

| # | Party | Role | May not also be |
|---|---|---|---|
| 1 | **Constructor** | Generation protocol, instrument, this document | any of 2–7 |
| 2 | **Corpus / reference-label party** | Authors the bank, authors and seals ground truth, runs the generator | any other |
| 3 | **Bank validator** | §5.4 back-translation, metadata-blind | any other |
| 4 | **Fidelity checker** | §5.8 byte-level check | any other |
| 5 | **Adjudicator A** | Blind adjudication | any other |
| 6 | **Adjudicator B** | Blind adjudication | any other |
| 7 | **Gate party** | Reviews and gates | any of 1–6 |
| 8 | *Reserve adjudicator* | Substitute for 5 or 6, disclosed | any of 1, 2, 3, 4, 7 |

**No permitted overlap.** The gate party may not be the fidelity checker — fidelity checking is execution, and a gate performing it would certify its own work. The bank validator may not adjudicate, having seen the bank.

**Excluded from parties 2–8, by name and by role:** Fable (constructor, S1 contributing reviewer); Sol (S1 instrument, sampling, calibration, decision-rule construction); Ivan (S1 construction, specification and ratification — retains L3 ratification, which is not an evaluative role); any agent that materially encoded S1 classifier or decision logic; and generally any actor materially involved in S1 as author, specifier, implementer of decision rules, or contributing reviewer.

### 12.1 Adversarial pre-gate review is not a gate

```text
ADVERSARIAL_PRE_GATE_REVIEW
Reviewer: <party>
Independent-gate eligibility: NO
```

Such reviews are legitimate construction aid. They **cannot satisfy the Stage 1 `K5` prerequisite**, and no `PASS` issued by an excluded party may be recorded as a gate verdict or merged as one. The independent gate is party 7, sees the candidate for the first time, and has no prior exposure to its construction.

### 12.2 Process rule — frozen, as amended

```text
Internal adversarial review of a candidate version ends at its
closure check. The next internal pass is a CLOSURE CHECK ONLY,
against the named finding list of the immediately preceding review.
It may not open a new redesign line.

AMENDMENT (v0.10): an external G1 or G2 BLOCK authorizes a new
version. This rule closes internally-initiated redesign; it does
not close a response to an external gate finding. The new version
must state which external finding authorized it, must confine
itself to that finding and its consequences, and must return to
G1.
```

**v0.11's authorizing finding is `G1-BLOCK-002`** (§0). Its `NOT AUTHORIZED` list is part of the authorization and was observed: the `E8a` interrogative, its scopes, its enum, all thresholds and all unrelated coverage policy are unchanged.

`[L2]` A wider `E8a` redesign was considered and refused. The gate's second finding did not show the interrogative broken; it showed a coverage constraint unconnected to the scope solver. Opening the interrogative because the region has now failed twice would be changing something no gate has found defective, which is the pattern this rule exists to stop. If a third external finding shows a fundamental `E8a` defect, a wider cycle becomes justified on evidence.

---

## 13. Declared limitations

**13.1 Statistical scope.** Failure-detection design, not estimation. No confidence intervals, no population estimates, no extrapolation to real deposits. No rate bound from `K1`.

**13.2 Domain and coverage.** The CVD is template-generated from a frozen bank with entries inserted verbatim; answer spaces are closed by construction (`ATOM-3` not demonstrated). Every `(bundle, parameter)` parameter-cell carries exactly one scope, where a real deposit has many. Scope depth is uneven by design: `E8b` is exercised across eight scopes with most `(class, scope)` combinations untested; `E7b` on one scope only; and `E8a` on two signals of the eight it could apply to, with a four-unit enum instead of the far larger real unit space. That narrowing is the price of `SCOPE-2`: a unit question is only measurable where the answer is not implied by the signal, and in the CVD that holds for `current` and `voltage` alone. Numeric payloads are covered only by category, not by value diversity (§5.2.3). Real deposits are longer, messier, and state facts in prose no bank contains.

**Frozen consequence: `QUALIFIED_ON_CVD_FOR` does not license S3.** It prevents S3 from beginning with an instrument demonstrably broken on the listed parameters, on a simpler domain, and nothing more. Closing the gap requires a separate step on real material with its own freeze, not specified here.

**13.3 Bank meaning.** §5.4 establishes two-party agreement on six fields, not meaning itself. A misreading shared by corpus party and validator propagates into gold undetected.

**13.4 Prohibited outputs.** No verdict about any real deposit; no prevalence figure about documentation quality in any literature; no pooled single-number accuracy; no claim of real-domain exhaustiveness for any answer space; no confidence interval or population estimate; no claim of methodological novelty; no non-resolution figure without the §6.7 sentence; no statement of qualification without the §8.1 sentence; no use in S3 of any parameter outside `QUALIFIED_ON_CVD_FOR`; no gate verdict from a party excluded under §12.

---

## 14. Reserved

---

## 15. L3 decisions

1. **Stage 2 thresholds**: class-score floor `≥ 3/5`, parameter floor `25/30`, semantic stability `24/30`.
2. **`K1` as a global prerequisite**, knowing one fabrication in 660 adjudications terminates the run.
3. **Bank loop limits**: 3 attempts per slot, rejection ceiling `99`, single-use entries, no re-keying.
4. **Coverage contract levels**: 2 parameter-cells per coverage category, 2 composition, 2 per stratum.
5. **Numeric-payload coverage**: whether the contract should require more than one distinct numeric payload for `E5` and `E8b`, and how many.
6. **Staffing of seven (or eight) separated parties** — `K5`, binding on whether S2 runs.
7. **Corpus budget**: 330 single-use bank entries plus back-translation, 30 bundles, 1320 adjudication events.
8. **Publication status** of the qualification artifact, verbatim.
9. **BatteryLake manifest review** — `PRIOR_ART_ELIMINATION_v0.2.md` §6. If ratified, its output is `PRIOR_ART_ELIMINATION_v0.3.md`, conditional on that ratification and not an unconditional prerequisite of G1 or G2.
10. **Paywalled / non-English sweep** — not blocking qualification; blocking any public absence claim.

---

**Status:** `SPREMNO ZA GEJT`. Requires a **new G1 pass**. The same eligible party-7 instance remains procedurally eligible, having authored neither v0.10 nor v0.11.

Two places a gate should attack. **§5.2.5**, where the principle is stated but no capacity formula is frozen, so the burden of deriving required capacity falls on the `F2` script — a script that does not exist, for the one region of this specification that has now failed twice. And **§5.2.2's zero-slack case**: in the worst admissible allocation the `E8a` scope receiving four standalone determining parameter-cells has exactly `2 + 2` slots, so scope allocation and unit assignment must be solved jointly rather than in sequence, and the specification asserts that requirement without demonstrating that a joint solution exists for every admissible allocation.
