# F7/F8 Boundary Implementation Correction — Operator Ratification 001

Instance: `battery-deposit-semantics-s2`  
Operator: Ivan (VolMax Studio Lab)  
Governing frozen specification: `construction/S2_CANDIDATE_SPEC_v0.11.md`  
Current closed stage: `F6`  
F6 closure commit: `0c9bab200a448a4967d7495968b7fc556e2b0d5a`  
Date: 2026-09-13  

---

## 1. Decision

The operator accepts the Party-1 (Constructor / Adversarial Reviewer) analysis of the F7→F8 boundary and formally authorizes a scoped implementation-conformance correction.

This decision does **not** reopen the frozen methodology:
- `S2_CANDIDATE_SPEC_v0.11.md` remains governing without amendment.
- No `v0.12` specification cycle is authorized.
- Stage F5 (Bank Authoring) and Stage F6 (Role-Aware Back-Translation) remain closed, valid, and unchanged.
- Final retained bank: `corpus/f5_bank/F5_BANK_ATTEMPT_03.jsonl` (330 unique entries, SHA256: `22fa12f14cbd0fda08293fd7c7886b7793d80bf7ec9dfa9cf2330e3b26e62859`).
- Final F6 status: `F6_BANK_INTEGRITY = ESTABLISHED`, cumulative $R_{\text{total}} = 53 \le 99$.

---

## 2. Confirmed Implementation-Conformance Defects

### IC-1 — F7 Sealed-GT Location Coupling
The current fidelity implementation in `template_generator.py` includes F8-only location information (`component`, `byte_start`, `byte_end`) inside the canonical derived ground-truth readings.
Because Stage F7 is frozen to occur before Stage F8 bundle generation (§11), bundle byte offsets and concrete file components do not exist at F7.
The canonical F7 ground truth shall therefore be strictly **location-independent**. F8 byte locations remain fidelity evidence / provenance used during reconstruction and verification, but are not fields of the sealed logical GT record.

### IC-2 — POS Class Borrowed from Expected Placement
The current `reconstruct_derived_ground_truth()` implementation assigns `POS-EXPLICIT` versus `POS-BURIED` by reading `slot_placement = slot_info.get("placement", "prominent")` rather than deriving the placement class from the actual location of the discovered bank entry in generated bundle bytes.
This fails to independently verify placement fidelity.
The corrected implementation must derive placement-sensitive class from the actual discovered occurrence position under mechanically invertible frozen placement rules. Expected layout placement metadata may not be used as the authority for this derivation.

### IC-3 — Executable F2 Bundle Generator Absent
Frozen §11 Stage F2 requires *"generator and validator scripts"*.
At commit `0c9bab2`, the reviewed F2 artifact set contains fidelity reconstruction and checking code, but lacks an executable bundle-generation routine that generates concrete bundle files under the frozen placement rules.
This is an artifact-conformity defect in the previously gated F2 implementation set. It does not alter frozen methodology.

---

## 3. Authorized Correction Scope

The correction package is strictly limited to:
1. **Canonical location-independent logical-GT schema**;
2. **Canonical GT serializer**, including §6.6 numeric canonicalization, sorted keys, and deterministic ordering;
3. **Executable bundle generator** implementing the frozen corpus and placement rules across 30 bundles;
4. **Mechanically invertible prominent/buried placement mapping**;
5. **Corrected fidelity reconstruction** deriving placement-sensitive class from actual byte occurrence position;
6. **Regression test suite** covering the corrected F7/F8 boundary and all invariants.

No interrogative, answer space, scope set, class assignment, coverage threshold, decision threshold, F5 bank content, F6 result, party architecture, or scientific claim may change under this authorization.

---

## 4. Canonical Logical-GT Requirements

The canonical sealed record is an ordered array of 330 cells, sorted by `(bundle_idx, parameter)`.

Each parameter-cell object shall contain:
- `bundle_idx`: integer (`0..29`)
- `parameter`: string (`"E1".. "E8b"`)
- `scope`: string (from applicable scope set)
- `class`: string (`"POS-EXPLICIT" | "POS-BURIED" | "NEG-ABSENT" | "NEG-ADJACENT" | "AMBIG-CONSTRUCTED" | "NA-CONSTRUCTED"`)
- `verdict_class`: string (`"EXPLICIT_DOC" | "EXPLICIT_FILE" | "AMBIGUOUS" | "ABSENT" | "NOT_APPLICABLE"`)
- `readings`: list of reading objects, sorted lexicographically by canonical serialization of `semantic_value`
- `support_entry_ids`: list of bank `entry_id` strings, canonically sorted

Each reading object in `readings` contains:
- `entry_id`: string
- `semantic_value`: canonical string or numeric/set structure under §6.6
- `evidence_stratum`: string (`"S-DOC" | "S-FILE"`)
- `exclusive_assertion`: boolean
- `verbatim_excerpt`: string (verbatim bank entry text)

The canonical sealed record shall NOT contain:
- `component`
- `byte_start`
- `byte_end`
- `placement`
- `realization_index`
- `keyed_bank_entry_ids`

### Support Entry IDs Cardinality
`support_entry_ids` provides exact bank-entry provenance for fidelity verification without overloading the §6.1 adjudication concept of `readings`:
- `POS-EXPLICIT` / `POS-BURIED`: exactly 1 entry ID
- `AMBIG-CONSTRUCTED`: exactly 2 entry IDs (lexicographically sorted)
- `NEG-ADJACENT`: exactly 1 entry ID (the keyed adjacent entry)
- `NA-CONSTRUCTED`: exactly 1 entry ID (the keyed non-applicable entry)
- `NEG-ABSENT`: 0 entry IDs (`[]`)

`readings` remains strictly empty (`[]`) for `ABSENT` and `NOT_APPLICABLE` cells.

---

## 5. Placement Invertibility Requirements

1. **Mechanically Invertible**: Prominent and buried placement regions within bundle components must be mechanically distinguishable from bundle structure and byte offsets.
2. **Independence**: The fidelity checker must determine whether an occurrence is prominent or buried solely from its byte location in the bundle, without consulting expected `slot_info["placement"]`.
3. **Anti-Leakage / Retrieval Integrity**: The placement mechanism must not introduce explicit class-bearing textual markers (e.g. `"BURIED_SECTION"`) or trivial shortcuts visible to adjudicators. `POS-BURIED` must remain a genuine retrieval condition. Any residual formatting characteristics remain subject to the frozen K3 leakage probe.

---

## 6. Preserved Invariants

Ground-truth reconstruction must continue to iterate over the complete frozen cell layout across all 30 bundles and 11 parameters (330 cells). Parameter-cells with zero discovered bank entries must remain represented as `NEG-ABSENT` with `readings: []` and `support_entry_ids: []`.

---

## 7. Gate Consequence & Execution Hold

The previous G2 artifact-conformity verdict does not cover corrected or newly introduced F7/F8 implementation bytes.

Therefore, a **scoped Party-7 artifact-conformity re-gate** is required after implementation and regression tests are complete. The scoped re-gate is strictly limited to the corrected/new F7/F8 boundary artifacts and their compliance with v0.11.

Stage F7 is **HELD** and not authorized to begin until:
1. The correction package is fully implemented;
2. The regression suite passes with 0 failures;
3. The correction is merged to `main`;
4. The scoped Party-7 artifact-conformity re-gate returns `ARTIFACT_CONFORMITY_PASS`.

Lifecycle status:
`F7_BLOCKED_PENDING_SCOPED_G2_REGATE`
