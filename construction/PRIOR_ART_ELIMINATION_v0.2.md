# Prior Art Elimination v0.2

**Instance:** `battery-deposit-semantics-s2`
**Phase:** 0 — precedes `INSTRUMENT.md`
**Supersedes:** `PRIOR_ART_ELIMINATION_v0.1.md` (retained unmodified; this document does not rewrite it)
**Author:** Claude ("Fable"), constructor; S1 conflict declared in `S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Date:** 2026-09-12
**Status:** `SPREMNO ZA GEJT` — not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; no L3 selections made.

---

## 1. Status

```text
RESEARCH_QUESTION:
NOT_SHOWN_TO_BE_ALREADY_ANSWERED

PRIOR_ART_ELIMINATION:
INCOMPLETE

METHOD_STATUS:
CORE_COMPONENTS_ANTICIPATED
NO METHODOLOGICAL_NOVELTY CLAIM INTENDED FOR S2

OPEN_PRIOR_ART_ITEM:
BatteryLake public curation / processing manifests
NOT YET INSPECTED
INSPECTION REQUIRES L3 RATIFICATION
```

---

## 2. What changed from v0.1, and why

Three changes. Each is a correction of the constructor's error, not new evidence.

### 2.1 `NOT_ANSWERED` → `NOT_SHOWN_TO_BE_ALREADY_ANSWERED`

v0.1 §1 asserted that the research question is not answered, while v0.1 §2 simultaneously recorded that BatteryLake's released curation records were deliberately left unopened in order to preserve S3 sampling.

Those two statements cannot both stand. A negative existence claim made while declining to read the single most relevant known body of public evidence is not a finding; it is an assumption wearing a verdict's clothes. The defect is mine and it is the same class as the defects this project exists to catch.

The underlying error was conflating two activities that have different rules:

| Activity | Governing constraint |
|---|---|
| Prior-art review of published work | None. Published literature is public to everyone, including any future reviewer. |
| Inspection of a prospective confirmatory target | Prohibited before freeze; consumes the unit's blindness. |

Prior art takes precedence over blindness. Reading published work and then excluding the units it exposes from a future confirmatory pool costs frame size. Declining to read it costs the defensibility of the entire negative claim. The first cost is recoverable; the second is not.

### 2.2 `METHOD_FULLY_ANTICIPATED` → `CORE_COMPONENTS_ANTICIPATED`

v0.1 §1 overstated. The evidence in v0.1 §7 supports that the *components* are anticipated — constructed ground truth via reverse generation (RIKER, VAREX, DTBench, PSEBench), abstention as a first-class output, negative controls including missing-information variants, verbatim evidence grounding with quote verification, inter-annotator agreement reporting (BatteryLake). It does not support that the specific combination has been published as one protocol.

Specifically not found as a single published protocol: `S-DOC`/`S-FILE` stratification held **unranked**, disagreement **recorded rather than resolved**, and stability **gated on** demonstrated discrimination.

**This is recorded so that it cannot be resurrected later as a novelty argument.** Combination-novelty matters only to a contribution claim, and §3 states that S2 makes none. If a future participant cites this paragraph in support of publishing S2 as a methodological contribution, they are misreading it. The claim here is narrow: `FULLY` was wrong, and the correct word is `CORE_COMPONENTS`.

`[L2]` My assessment is that combination-novelty of this kind would not survive peer review as a contribution in any case, and that any future novelty argument belongs to S3's measurand, not to S2's architecture.

### 2.3 BatteryLake manifests promoted to a named open item

See §4.

---

## 3. Unchanged from v0.1

The following findings stand as written in `PRIOR_ART_ELIMINATION_v0.1.md` and are **not** restated here. That document is the source of truth for them.

- §3 — the FAIR assessment family does not occupy the measurand, on the tools' own stated limits.
- §4 — BattINFO, BDF and BatteryML are prescriptive infrastructure; prescription is not retrospective measurement.
- §5.1–§5.3 — what BatteryLake shares with our design, what it does not do, and why its stated limitations strengthen the case for independent qualification.
- §6 — adjacent empirical assessments and how close each gets.
- §7 — the component-level prior art for synthetic-ground-truth validation.

Also unchanged: the reclassification of S2 to `INTERNAL_QUALIFICATION`, which is the one item ratified by the operator to date.

---

## 4. Open prior-art item: BatteryLake curation and processing manifests

### 4.1 What exists

BatteryLake (arXiv:2607.09762) states that every curated dataset ships a processing manifest recording raw-file inventory, mapping rules, unit conversions, cycle segmentation logic, label definitions and validator version, and reports 41 registered datasets with 12 fully curated. It also reports calibration error and inter-annotator agreement for its extraction pipeline.

### 4.2 What inspection could change

Three distinct things, which should not be bundled into one decision:

1. **Whether part of the S3 prevalence question is already answered in public.** If the manifests expose per-field `⊥` ("not stated") labels across the registered datasets, a portion of the documentation-deficit measurement exists publicly for BatteryLake's field set. Their field set is experiment metadata, not export semantics (v0.1 §5.2), so overlap is expected to be partial — but "expected" is the word that got v0.1 into trouble.
2. **Whether their gold annotations have disclosed provenance.** If the gold labels were produced by the same parties who built the extractor, their accuracy figures inherit the circularity our design exists to avoid, and that is directly relevant to how much independent qualification is worth. If the provenance is disclosed and independent, the opposite.
3. **The size of the S3 frame.** Any dataset whose semantic disposition becomes known through this review is exposed and leaves the confirmatory pool permanently.

### 4.3 Constraints on the inspection, if ratified

- It is a **prior-art review**, recorded as `PRIOR_ART_EXPOSURE`, not an S2 or S3 evidence-collection step. No S2 artifact may cite it as data.
- Exposed units are named and permanently excluded from any future confirmatory pool, in the exposure ledger, before the review closes.
- It does not authorise opening any deposit's own documentation, landing page, or files. The object is BatteryLake's published records, nothing beyond them.
- Output is `PRIOR_ART_ELIMINATION_v0.3.md`, which either closes the item or states what remains open.

### 4.4 Why this is not a reason to delay S2 qualification

S2 as specified touches no real deposit. Its corpus is constructed. Nothing in this open item can invalidate an instrument-qualification result, because qualification measures the instrument, not the corpus of deposits.

The item blocks the *epistemic status of the project*, not the *qualification run*. Those can proceed in parallel. What it does block is any public statement of the form "this has not been measured before."

---

## 5. What this search still has not eliminated

Unchanged from v0.1 §2, restated because it governs the status line:

- Paywalled full texts beyond abstracts and open HTML.
- Non-English literature.
- Proceedings not indexed by the search engines used.
- Anything published after 2026-09-12.
- The open item in §4.

`PRIOR_ART_ELIMINATION` remains `INCOMPLETE` until at minimum §4 closes. A paywalled sweep is not required for internal qualification but is required before any public statement about what has or has not been measured in this domain.

---

## 6. L3 decisions open on this document

1. **Ratify or decline the BatteryLake manifest review** (§4), under the constraints in §4.3.
2. **Ratify or decline a paywalled / non-English sweep**, and if declined, accept that no public novelty or absence claim may be made until it is run.
3. **Frame decision for S3** — dos Reis Table 2 remains a candidate frame; the BatteryLake registry is now a partially overlapping alternative. Not decidable before §4 closes.

None of these blocks S2 qualification (§4.4).

---

**Status:** `SPREMNO ZA GEJT`. Written by the S2 constructor. The section most likely to be self-serving is §2.2, where the author softens his own earlier verdict against his own architecture; it is written to be unusable as a novelty argument, and a gate should check that it succeeds at that.
