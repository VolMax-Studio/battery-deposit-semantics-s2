# F4 ROLE STAFFING RECORD

**Instance:** `battery-deposit-semantics-s2`
**Governing specification:** `construction/S2_CANDIDATE_SPEC_v0.11.md` (frozen)
**Main baseline:** `393df15cce6ca1f5f120848e9c89499a63857300`
**Stage:** `F4` — Roles Ratified and Staffed
**Prerequisite discharged:** `K5` role separation
**Drafted by:** Fable / Claude — Party 1 (Constructor). This is an operator governance record, not a gate verdict; the constructor holds no gate authority under §12.

---

## 0. Predecessor stage status

`F2` and `F3` are closed. The initial G2 pre-execution artifact-conformity gate returned `ARTIFACT_CONFORMITY_BLOCK` on two implementation-only findings; remediation landed at `6bdcead2ae8c63a7d636259b55a215fd9b90c8fd`; re-review of exact source returned `ARTIFACT_CONFORMITY_PASS` with 31/31 tests. `F2`/`F3` are **FROZEN & ACCEPTED**.

No `F2`/`F3` artifact is reopened by this record.

---

## 1. Frozen role roster

| Party | Role | Assigned actor | Other S2 role | Status |
|---|---|---|---|---|
| Party 1 | Constructor | Fable / Claude | NONE | CLOSED |
| Party 2 | Corpus / Reference-Label Party | `GEMINI-CLEAN-P2-01` | NONE | STAFFED |
| Party 3 | Bank Validator | `GEMINI-CLEAN-P3-01` | NONE | STAFFED |
| Party 4 | Fidelity Checker | `GEMINI-CLEAN-P4-01` | NONE | STAFFED |
| Party 5 | Adjudicator A | `GEMINI-CLEAN-P5-01` | NONE | STAFFED |
| Party 6 | Adjudicator B | `GEMINI-CLEAN-P6-01` | NONE | STAFFED |
| Party 7 | Gate Party | Existing context-isolated Gemini Party-7 (G1, G2) | NONE | STAFFED |
| Party 8 | Reserve Adjudicator | — | — | **NOT STAFFED** |

Ivan / VolMax Studio Lab remains Operator and final ratifier and holds no Party 1–7 role.

### 1.1 Party 8 — not staffed, and the consequence

```text
Party 8 = NOT STAFFED.
If either primary adjudicator becomes unavailable, execution HALTS.
No silent substitution is permitted.
```

This is a chosen consequence, not an omission. §7 permits a disclosed reserve; none is staffed, so the substitution path is closed rather than left to improvisation mid-run.

---

## 2. F2/F3 implementation provenance — disclosure

```text
F2/F3 IMPLEMENTATION PROVENANCE

Repository commits are operator-controlled under VolMax-Studio.
The historical AI-assistant identity responsible for all portions of the
F2/F3 implementation is not relied upon as an execution or evaluative party.

No historical F2/F3 implementation actor is assigned to Parties 2–7.

Parties 2–6 are fresh role-specific instances created for execution after
F2/F3 closure and receive only their authorized role packages.

If later provenance establishes that a proposed Party 2–7 actor materially
implemented the F2/F3 artifacts, that assignment is invalid and F4 must be
re-evaluated before protected inputs are released.
```

Frozen §12 does not define an F2/F3 implementer as a mandatory eighth party. `K5` requires that Parties 1–7 be mutually disjoint, which the roster satisfies. The disclosure above records what the repository can and cannot establish, rather than asserting an implementer identity the record does not support.

---

## 3. Isolation rules

### Party 2 — Corpus / Reference-Label Party — `GEMINI-CLEAN-P2-01`

**Authorized inputs only:** frozen `F5` inventory; applicable scopes per §4.2; semantic-value vocabulary per §4.1 and §5.2.1; bank semantic and placement schemas per §5.3; the frozen incompatibility relation §5.7; the coverage contract §5.2.2 including the `E8a` scope-partitioned form; **the `E3` and `E4a`/`E4b` structural realization constraints of §4.3**; the frozen scope-assignment table and class closed form of §5.1; frozen construction constraints necessary to author the 330 entries.

The `E3`/`E4` constraints are explicitly in scope because Party 2 runs the generator at `F8` and the bundles it emits must declare the required structures — at least one cycle with ≥ 2 steps, at least one test with ≥ 2 cycles, ≥ 2 tests, and strictly positive interval duration.

**Prohibited inputs:** S1 history; adjudicator outputs; Party-3 back-translation results before submission; sealed qualification results; Party-5 or Party-6 outputs.

**Authorized work:** `F5` bank authoring (330 single-use entries); `F7` ground-truth authoring and sealing; `F8` bundle generation as defined by the frozen specification. No other S2 role.

### Party 3 — Bank Validator — `GEMINI-CLEAN-P3-01`

**Authorized inputs only:** the metadata-blind bank text package required by §5.4 — entry texts shuffled and stripped of all metadata — plus the frozen interrogatives, answer enums, stratum definitions, scope vocabulary, and the six-field back-translation response schema.

**Must not receive:** intended semantic labels before back-translation; ground truth; generated bundles; adjudicator outputs; `class` or `placement` metadata, which §5.3 excludes from validation by design.

**Authorized work:** §5.4 blind back-translation; validation of the six frozen semantic fields; §5.6 loop accounting. No other S2 role.

### Party 4 — Fidelity Checker — `GEMINI-CLEAN-P4-01`

**Authorized inputs only:** the frozen `F2`/`F3` implementation; generated bundle bytes; the frozen bank; sealed ground-truth bytes and the construction metadata required by §5.8.

**Authorized work:** execute the frozen §5.8 fidelity checker; retain literal PASS/FAIL evidence and output artifacts.

Party 4 may not modify the checker, methodology, bank, ground truth, bundles or adjudication outputs. The realization index is a cross-check only and is never an authority; index–bytes disagreement halts at `F8`. No other S2 role.

### Party 5 — Adjudicator A — `GEMINI-CLEAN-P5-01`

Receives only the frozen blind adjudication package defined by §7: the pinned bundle manifest including each parameter-cell's scope, and the frozen §2–§6 instrument text.

**Must not receive:** ground truth; the bank; the realization index; corpus composition; item class; Party-6 output; Stage-2 scoring results before completion; §8. No other S2 role.

### Party 6 — Adjudicator B — `GEMINI-CLEAN-P6-01`

Receives the same frozen blind adjudication package as Party 5, in a separate isolated session. Same prohibitions, with Party-5 output withheld. No other S2 role.

### Party 7 — Gate Party

Actor: existing context-isolated Gemini Party-7.

**Prior authorized work:** G1 Specification Gate on v0.11; G2 Pre-Execution Artifact-Conformity Gate on the `F2`/`F3` package, including the re-review after remediation.

Frozen §12 defines a single Gate Party performing review and gating; the frozen text does not require distinct instances for successive passes. A separate governance document proposing distinct fresh G1/G2 instances remained `RATIFICATION_CANDIDATE` and was not incorporated into the Operator-ratified L3 Decisions 1–10. **No deviation from the governing frozen instance is recorded.**

Party 7 is excluded from Parties 1–6 and performs no corpus authorship, bank validation, fidelity execution or adjudication.

---

## 4. Explicit exclusions

- **Fable / Claude** — Party 1 Constructor and S1 contributing reviewer. No Party 2–8 role. No gate authority; its reviews are recorded as `ADVERSARIAL_REVIEW`, never as a gate verdict.
- **Sol** — prior S1 instrument, sampling, calibration and decision-rule involvement. No Party 2–8 role.
- **Ivan / VolMax Studio Lab** — Operator and ratifier. No Party 2–8 evaluative or execution role.
- **Existing Gemini Party-7** — gate only. No Party 1–6 role.
- Any instance exposed to another party's hidden inputs or outputs becomes ineligible for that role.

---

## 5. Conflict matrix

|    | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|----|----|----|----|----|----|----|----|
| P1 | — | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT |
| P2 | DISJOINT | — | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT |
| P3 | DISJOINT | DISJOINT | — | DISJOINT | DISJOINT | DISJOINT | DISJOINT |
| P4 | DISJOINT | DISJOINT | DISJOINT | — | DISJOINT | DISJOINT | DISJOINT |
| P5 | DISJOINT | DISJOINT | DISJOINT | DISJOINT | — | DISJOINT | DISJOINT |
| P6 | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT | — | DISJOINT |
| P7 | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT | DISJOINT | — |

The matrix asserts disjointness over Parties 1–7 as defined by §12. It makes no claim about the historical `F2`/`F3` implementation actor, which §2 addresses separately.

---

## 6. Session-isolation declaration

For Parties 2–6:

- each actor is instantiated in a separate clean chat/session;
- no actor is reused for another party;
- no cross-party conversation history is supplied;
- only the role-specific frozen package is supplied;
- outputs from one party are withheld from other parties unless the frozen execution order explicitly requires them.

Use of the same model provider does not constitute **role overlap**. Separation is defined by actor/session identity, authorized inputs and role boundaries. This statement addresses role overlap only; the separate question of correlated behaviour between same-family adjudicators is addressed in §7 and is not answered by it.

---

## 7. `F4-DECISION-SEMANTIC-STABILITY-001`

```text
F4-DECISION-SEMANTIC-STABILITY-001

P5 and P6 may use separate clean instances of the same model family
and the same pinned sampling configuration required by frozen F3.

No per-adjudicator seed or sampling divergence is introduced.

The Stage-2 semantic-stability threshold remains mechanically binding
exactly as frozen.

For this run, semantic stability is NOT interpreted as evidence of
independent replication, independent reasoning, or independent error sources.

Because P5 and P6 may share model family, version, prompt structure and
sampling configuration, high or even perfect semantic stability may have
limited discriminatory value and must be reported with that limitation.

K2 remains a within-adjudicator repeatability prerequisite:
each adjudicator must independently recreate its own output byte-identically.

Cross-adjudicator identity is neither assumed nor required by K2.

OPERATOR DECISION:
semantic stability remains a frozen gating condition, but its epistemic
interpretation in this run is consciously limited as stated above.

STATUS: RESOLVED AT F4.
```

### 7.1 Basis and the correction it incorporates

The `F3` sidecar pins `temperature = 0.0`, `top_p = 1.0`, `top_k = 1`, `seed = 20260912`. Introducing per-adjudicator seed or sampling divergence would modify a G2-passed `F3` artifact and is refused.

An earlier adversarial review asserted that identical `P5`/`P6` output is guaranteed by construction under this configuration. That assertion is withdrawn: `K2` exists precisely to test within-channel determinism empirically, and if determinism were axiomatic `K2` would be vacuous. Two separate instances may still produce different semantic decisions.

What holds is narrower: shared model family, version, prompt structure and sampling configuration make semantic stability **potentially low-discrimination** as evidence of agreement between independent channels. Whether its discriminatory power is in fact low is an empirical question about this run and is not decided here.

### 7.2 Reporting obligation

If `P5` and `P6` return identical semantic verdicts on all or nearly all 330 parameter-cells, the final artifact must state that the stability condition had **zero or near-zero empirical discriminatory power in this run**, with the observed figure. The limitation clause of the decision above is reproduced in any output that reports a stability figure, alongside the frozen §7 text on what agreement does not prove.

---

## 8. `K5` determination

The seven mandatory roles are staffed with mutually disjoint actors under frozen role boundaries.

```text
K5_PREREQUISITE_SATISFIED = YES
F4_STATUS                 = RATIFIED ON OPERATOR COMMIT
F5_BANK_AUTHORING         = AUTHORIZED ON OPERATOR COMMIT
```

No `F5` work may begin before this record is committed to `main`.

---

## 9. Operator ratification

Operator: **Ivan / VolMax Studio Lab**

By committing this record to `main`, the Operator ratifies the role assignments above, the provenance disclosure in §2, the Party-8 halt consequence in §1.1, and `F4-DECISION-SEMANTIC-STABILITY-001` in §7, and confirms that Parties 2–6 will be instantiated as separate clean sessions before receiving their respective role packages.

Merge to `main` is the ratification act. No party other than the Operator may perform it.

Any later role substitution must be recorded before the substitute receives protected inputs and must preserve all frozen §12 separation constraints.

---

**Status:** drafted by Party 1. `F4_STATUS = RATIFIED` and `F5_BANK_AUTHORING = AUTHORIZED` take effect on the Operator's merge, not on this file's existence.
