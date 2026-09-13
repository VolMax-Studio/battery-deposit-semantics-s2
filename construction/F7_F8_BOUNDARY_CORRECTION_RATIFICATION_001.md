# F7/F8 Boundary Implementation Correction — Operator Ratification 001

Instance: `battery-deposit-semantics-s2`

Operator: Ivan

Governing frozen specification:

`construction/S2_CANDIDATE_SPEC_v0.11.md`

Current closed stage:

`F6`

F6 closure commit:

`0c9bab200a448a4967d7495968b7fc556e2b0d5a`

---

## 1. Decision

The operator accepts the Party-1 adversarial construction review of the F7→F8 boundary and authorizes a scoped implementation-conformance correction.

This decision does **not** reopen the frozen methodology.

`construction/S2_CANDIDATE_SPEC_v0.11.md` remains governing.

No `v0.12` is authorized.

F5 and F6 remain closed and unchanged.

The final validated bank remains:

`corpus/f5_bank/F5_BANK_ATTEMPT_03.jsonl`

F6 status remains:

`F6_BANK_INTEGRITY = ESTABLISHED`

Final cumulative rejection count remains:

`R_total = 53`

No F5/F6 bank entry, semantic value, scope, class, stratum, replacement history, or F6 result may be modified under this authorization.

---

# 2. Confirmed implementation-conformance defects

## IC-1 — F7 sealed-GT location coupling

The current fidelity implementation includes F8-only location information in the canonical derived ground-truth record, including:

* `component`
* `byte_start`
* `byte_end`

Because frozen execution order requires F7 ground truth to be authored and sealed before F8 bundle generation, these fields cannot be part of the canonical F7 sealed record.

The canonical F7 ground truth shall therefore be **location-independent**.

F8 byte locations remain fidelity evidence used during independent reconstruction and verification, but are not fields of the canonical sealed logical GT.

Frozen methodology and stage order remain unchanged.

---

## IC-2 — POS class borrowed from expected placement

The current `reconstruct_derived_ground_truth()` implementation derives `POS-EXPLICIT` versus `POS-BURIED` from expected layout metadata rather than from the actual location of the discovered bank entry in generated bundle bytes.

This does not independently verify placement fidelity.

The corrected implementation must derive placement-sensitive class from the actual discovered occurrence position under mechanically invertible frozen placement rules.

Expected class, `slot_info["placement"]`, or any value directly or indirectly derived from expected class or expected placement may not be used as the authority for this derivation.

In particular, the checker may not treat the realization index, generator-side placement metadata, or any equivalent derivative of expected placement as authoritative evidence of actual placement.

The realization index remains a secondary cross-check only, as required by frozen §5.8.

---

## IC-3 — Required executable F2 bundle generator absent

Frozen F2 requires generator and validator scripts.

At commit `0c9bab2`, the gated F2 implementation set contains fidelity reconstruction/checking code but no executable bundle-generation routine implementing the frozen corpus placement rules.

This is an implementation artifact-conformity defect.

It also establishes a scoped finding concerning the earlier G2 artifact-conformity process:

> The G2 package presented `template_generator.py` as satisfying the frozen F2 generator requirement. No gate verified that the required artifact set was complete against §11 before verifying the artifacts present.

This does not imply misconduct or general unreliability by Party 7.

The finding concerns package completeness and gate coverage: the artifacts submitted for review did not contain one frozen required implementation artifact, while the package representation did not make that absence explicit.

The correction therefore adds a permanent scoped gate requirement:

**Artifact-set completeness must be checked before artifact-content conformity.**

For every gated stage, the gate must first establish that every artifact explicitly required by the governing frozen stage definition exists in the submitted package.

Only after completeness is established may byte/content conformity be assessed.

“Artifact absent” and “artifact present but non-conformant” must remain distinguishable outcomes.

---

# 3. Authorized correction scope

The implementation correction is strictly limited to:

1. canonical location-independent logical-GT schema;
2. canonical GT serializer, including §6.6 numeric canonicalization and deterministic ordering;
3. executable bundle generator implementing the already frozen corpus and placement rules;
4. mechanically invertible prominent/buried placement mapping;
5. corrected fidelity reconstruction deriving placement-sensitive class from actual bundle evidence rather than expected placement;
6. regression tests covering the corrected F7/F8 boundary.

No interrogative, answer space, scope set, class assignment, coverage threshold, decision threshold, bank semantic content, F6 result, party architecture, scientific claim, or frozen execution order may change under this authorization.

Any required change outside this scope must be returned to the operator as a new decision.

It may not be silently absorbed into this correction.

---

# 4. Canonical logical-GT requirements

The F7 sealed record is a location-independent logical reference record.

Each parameter-cell shall contain:

* `bundle_idx`
* `parameter`
* `scope`
* `class`
* `verdict_class`
* `readings`
* `support_entry_ids`

Each item in `readings` may contain:

* `entry_id`
* `semantic_value`
* `evidence_stratum`
* `exclusive_assertion`
* `verbatim_excerpt`

The canonical sealed record shall not contain:

* `component`
* `byte_start`
* `byte_end`
* `placement`
* `realization_index`
* `keyed_bank_entry_ids`

`support_entry_ids` must be canonically sorted.

Expected `support_entry_ids` cardinality:

```text
POS-EXPLICIT        -> 1
POS-BURIED          -> 1
AMBIG-CONSTRUCTED   -> 2
NEG-ADJACENT        -> 1
NA-CONSTRUCTED      -> 1
NEG-ABSENT          -> 0
```

`readings` cardinality remains governed by semantic verdict:

```text
EXPLICIT_DOC        -> exactly 1
EXPLICIT_FILE       -> exactly 1
AMBIGUOUS           -> >= 2
ABSENT              -> 0
NOT_APPLICABLE      -> 0
```

`readings` must be sorted deterministically according to the frozen canonical semantic-value serialization.

Set-valued semantic values must themselves be canonically sorted.

Numeric semantic values must use the frozen §6.6 canonicalization rules.

The canonical serializer must admit exactly one byte representation for one logical GT.

---

# 5. Placement requirements

Prominent and buried placements must be mechanically distinguishable from generated bundle bytes.

The fidelity checker must be able to derive the placement of a discovered occurrence without consulting:

* expected class;
* expected placement;
* realization-index placement claims;
* generator-side placement metadata;
* any derivative value whose authority ultimately comes from expected class or placement.

The placement mechanism must not introduce an explicit class-bearing marker or other intentional retrieval shortcut visible to the adjudicator.

The prohibition applies to **any reliable class-revealing signature, lexical or structural**.

A construction is therefore non-conformant if an adjudicator can reliably infer `POS-EXPLICIT` versus `POS-BURIED` from a single fixed token, section name, component choice, ordinal position, document depth, or other invariant structural signature deliberately coupled one-to-one with class.

Examples of prohibited lexical shortcuts include:

```text
POS_EXPLICIT
POS_BURIED
BURIED_SECTION
GROUND_TRUTH_REGION
```

These examples are illustrative and not exhaustive.

Where mechanical distinguishability and adjudicator-invisibility conflict, placement must be derived from ordinary document structure rather than from inserted class-bearing tokens.

The mapping must also avoid a globally trivial one-position-per-class rule.

Each placement class must be realizable in **multiple structural positions or equivalent structural realizations**, while the frozen placement rule remains mechanically invertible for the fidelity checker.

Thus:

* actual bundle structure must be sufficient for the checker to determine placement;
* no single structural position or signature may globally disclose the class;
* `POS-EXPLICIT` and `POS-BURIED` must each admit more than one structural realization;
* the checker’s mapping must be frozen and deterministic;
* the adjudicator must not receive the mapping or an intentional class label.

If no mechanism satisfies both mechanical invertibility and absence of an adjudicator-visible class shortcut, the conflict must be reported to the operator.

The implementer may not resolve that conflict silently.

`POS-BURIED` must remain a genuine retrieval condition rather than a trivially labeled or positionally deterministic class.

Any residual formatting or structural signal remains subject to the frozen K3 leakage probe.

---

# 6. F8 fidelity reconstruction requirements

The corrected fidelity path shall operate conceptually as:

```text
bundle bytes
   ↓
independent byte search over frozen bank
   ↓
discovered occurrences + actual byte spans
   ↓
derive actual placement from bundle structure
   ↓
derive class / verdict / readings / support
   ↓
discard location-only evidence from logical GT
   ↓
canonical logical-GT serialization
   ↓
byte comparison against F7 sealed logical GT
```

`component`, `byte_start`, and `byte_end` may be retained separately as fidelity evidence or diagnostics.

They may not alter the canonical logical GT bytes.

The checker must independently enforce frozen §5.8 requirements including:

* byte-exact bank-entry occurrence search;
* NEG-ABSENT determining-evidence prohibition;
* NEG-ADJACENT keyed-adjacent presence and determining-evidence prohibition;
* E3 structural requirements;
* E4 strictly-positive-duration requirements;
* realization-index cross-check as secondary evidence only.

---

# 7. Preserved complete-layout invariant

`reconstruct_derived_ground_truth()` already iterates the frozen cell layout rather than only discovered occurrences.

This is not recorded as a discovered defect.

It is recorded as a required regression invariant.

The corrected implementation must continue to emit every frozen parameter-cell, including cells for which no bank occurrence exists.

In particular:

`NEG-ABSENT` parameter-cells must remain represented in the derived logical GT with zero readings and zero support entry IDs.

A patch that reconstructs only cells represented by discovered bank occurrences is non-conformant.

---

# 8. Scoped G2 artifact-conformity re-gate

The previous G2 artifact-conformity verdict does not cover corrected or newly introduced F7/F8 implementation bytes.

Therefore a **scoped Party-7 artifact-conformity re-gate** is required.

This re-gate must occur **before F7 ground-truth sealing**.

The re-gate is limited to:

* completeness of the corrected F7/F8 implementation package;
* canonical logical-GT schema;
* canonical GT serializer;
* executable bundle generator;
* placement implementation and invertibility;
* fidelity reconstruction;
* relevant new regression tests;
* correct consumption of the frozen `F5_BANK_ATTEMPT_03.jsonl` bank and frozen cell layout by the new generator, **without reopening their contents or the F6 result**;
* interaction of those artifacts with already frozen v0.11 requirements.

For avoidance of doubt, checking correct consumption includes verifying that the generator:

* consumes the frozen final bank rather than an alternate bank;
* uses all 330 required bank entries exactly once under the frozen single-use rule;
* inserts bank text verbatim and without paraphrase;
* does not silently duplicate, omit, replace, or mutate bank entries;
* obeys the frozen bundle/parameter scope and class layout;
* does not re-key any frozen bank slot.

These checks concern downstream consumption only.

They do not reopen F5 authoring, F6 validation, or the established `R_total = 53` result.

The scoped re-gate does not reopen:

* F1;
* frozen v0.11 methodology;
* F5;
* F6;
* the bank-integrity result;
* party architecture;
* thresholds or decision rules.

## 8.1 Completeness-first gate rule

Before examining content conformity, Party 7 must enumerate the frozen artifacts required for the scoped stage and establish that every required artifact is present in the submitted package.

The scoped gate record must distinguish at minimum:

```text
REQUIRED_ARTIFACT_PRESENT
REQUIRED_ARTIFACT_ABSENT
ARTIFACT_CONTENT_CONFORMANT
ARTIFACT_CONTENT_NONCONFORMANT
```

Content review begins only after required-artifact completeness has been established.

---

# 9. Scoped re-gate failure handling

If the scoped Party-7 re-gate returns an artifact-conformity block, F7 remains blocked.

A finding that can be repaired entirely inside the authorization granted by this record returns the correction package to the constructor/implementation repair loop.

The repair may address only the named finding and remain inside this authorized scope.

After repair, the affected package must be re-submitted for scoped Party-7 review.

A gate finding that would require any change outside the authorized correction scope must not be resolved by the implementer or constructor under this record.

Such a finding must be escalated to the operator for a new explicit decision.

No scope expansion is automatic.

No blocked gate result may be converted into a pass through operator narration alone.

---

# 10. Execution hold

`F7` is not authorized to begin until all of the following are complete:

1. the authorized implementation correction package exists;
2. **the entire pre-existing implementation test suite plus all newly added tests passes**;
3. no previously passing test has been deleted, disabled, bypassed, narrowed, or weakened to obtain that result;
4. the execution record reports the complete test count, with the previous `31 / 31` clean G2 suite serving as the minimum inherited regression baseline before new tests are added;
5. corrected/new implementation artifacts are merged to `main`;
6. the scoped Party-7 artifact-set completeness check succeeds;
7. the scoped Party-7 artifact-conformity review returns the required conformity result.

Only after those conditions are satisfied may:

`GROK-CLEAN-P2-01`

author and SHA-256 seal the F7 ground-truth record.

Until then:

`F7_BLOCKED_PENDING_SCOPED_G2_REGATE`

---

# 11. Methodology status

Frozen methodology:

`UNCHANGED`

Governing specification:

`S2_CANDIDATE_SPEC_v0.11.md`

New specification version:

`NOT AUTHORIZED`

`v0.12`:

`NOT OPENED`

F5:

`CLOSED`

F6:

`CLOSED / BANK INTEGRITY ESTABLISHED`

F7:

`BLOCKED`

Reason:

`SCOPED F7/F8 IMPLEMENTATION-CONFORMANCE CORRECTION AND PARTY-7 RE-GATE REQUIRED`

---

# 12. Provenance note

The present defect family was discovered before any verdict-bearing F8/F10 qualification execution.

The correction does not demonstrate that the instrument is scientifically valid or qualified.

It demonstrates only that the control chain detected an implementation/gate-coverage defect in its own pre-execution artifacts before those artifacts were permitted to produce downstream qualification evidence.

That distinction must be preserved in any future public reporting.

---

## Operator disposition

Upon operator commit of this record:

`F7_F8_BOUNDARY_CORRECTION_001 = RATIFIED`

Authorized next work:

`PARTY_1 / IMPLEMENTATION CORRECTION PACKAGE`

Unauthorized next work:

`F7 EXECUTION`

Required next gate:

`SCOPED PARTY-7 ARTIFACT-CONFORMITY RE-GATE`
