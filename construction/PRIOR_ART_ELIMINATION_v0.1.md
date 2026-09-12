# Prior Art Elimination v0.1

**Instance:** `battery-deposit-semantics-s2`
**Phase:** 0 — precedes `INSTRUMENT.md`
**Author:** Claude ("Fable"), methodology drafter; S1 conflict declared in `construction/S2_ADMISSIBILITY_ASSESSMENT_FABLE_v0.1.md`
**Date of search:** 2026-09-12
**Status:** `SPREMNO ZA GEJT` — not ratified
**Layer convention:** unmarked = L1; `[L2]` = inference; no L3 selections made.

---

## 1. Verdict

Not `S2_NOT_JUSTIFIED_ALREADY_ANSWERED`, but not a clean pass either. Two separate verdicts are required because the question and the method have different prior-art status:

```text
RESEARCH_QUESTION (export-semantics resolvability of public battery deposits)
NOT_ANSWERED — but the unoccupied ground is materially narrower
than the S1 framing assumed. See §6.

S2 AS SPECIFIED (instrument validation on a constructed corpus)
METHOD_FULLY_ANTICIPATED — every architectural element of the S2
candidate is established prior art published between Dec 2025 and
Jul 2026. S2 has no research novelty and must be reclassified as
INTERNAL_QUALIFICATION, not a publishable instance. See §5, §7.
```

The honest summary: the thing we were going to build has been built; the thing we were going to measure has not been measured.

---

## 2. Method and boundaries of this search

Searched: FAIR assessment literature and tooling; battery data ontologies and standards; battery dataset reviews; agentic/LLM curation of scientific data; synthetic-ground-truth benchmark construction; abstention evaluation. English-language, web-accessible, as of 2026-09-12.

Deliberately **not** opened, to preserve S3 sampling:
- any row-level content of the dos Reis Table 2 frame;
- the documentation, landing page, or files of any candidate deposit;
- BatteryLake's released per-dataset curation records (see §5.4 — this is a live exposure question, not an oversight).

Not covered, and therefore not eliminated: paywalled full texts beyond abstracts and open HTML; non-English literature; conference proceedings not indexed by the search engines used; anything published after 2026-09-12.

---

## 3. Finding A — the measurand is not occupied by the FAIR literature

The FAIR assessment family (F-UJI / FAIRsFAIR metrics, FAIR-Checker, FAIRshake, FAIR-enough) evaluates machine-checkable indicators: persistent identifiers, protocol support, machine-readable licensing, schema use, provenance fields. Their own documentation states the limit plainly: F-UJI assesses what is machine-discoverable at the moment of the test and cannot judge whether documentation is actually clear to a human reader, nor discipline-specific FAIRness its generic metrics do not capture. A repository-level assessment presentation makes the same point: automated assessment cannot capture FAIR aspects requiring human interpretation, including domain-specific semantics.

This is a clean negative. FAIR scoring asks *is there metadata*; the S3 question asks *does the documentation determine a specific physical interpretation*. A deposit can score well on FAIR while leaving the sign convention unstated, and a deposit can score badly while stating it in the README.

Two adjacent 2026 items are worth registering but do not close the gap: the Dataset Friction Framework (arXiv 2606.23660), which proposes user-facing friction as a complement to FAIR and explicitly flags inter-reviewer variance as a known limitation of its reviewer-applied scoring; and AgentFAIR (arXiv 2607.15781), a multi-agent FAIRness evaluator for geospatial datasets. Both operate at the FAIR-indicator level, not at the level of a named physical convention.

---

## 4. Finding B — prescription is not measurement

Three bodies of work define what battery data *should* look like:

- **BattINFO / EMMO** (BIG-MAP, Battery2030+): a domain ontology for semantic annotation of battery experiments, with converter tooling and JSON-LD/RDF output.
- **Battery Data Format (BDF)**, released by the LF Energy Battery Data Alliance on 2025-12-22: a fixed table schema for cycler time-series data plus an ontology-aligned metadata layer, BattINFO-aligned, with converters for vendor formats.
- **BatteryML** (Zhang et al., ICLR 2024) and **BEEP** (Herring et al.): processing and benchmark toolkits that impose their own canonical representations.

None of these measures the documentation state of the existing corpus. A schema that specifies where a sign convention goes does not tell you how many published deposits stated theirs. Prescriptive standards and retrospective measurement are different acts, and the existence of the former is an argument *for* the latter, not against it.

`[L2]` BDF's arrival does change the practical relevance of the S3 question over time: if BDF adoption grows, the measured deficit becomes a statement about a legacy corpus rather than about current practice. That is a framing constraint for S3, not a reason to abandon it.

---

## 5. Finding C — BatteryLake is the near-miss, and it is very near

**Zhu, Wang, Wen (NTU). "BatteryLake: Agentic, Physics-Grounded Curation of Heterogeneous Battery Aging Data and Benchmarking." arXiv:2607.09762, 6 July 2026.**

This is the single most important item in this document. It must be read by anyone who continues this work.

### 5.1 What it shares with our design

BatteryLake formalises battery dataset onboarding as evidence-grounded extraction with explicit abstention. Concretely, it implements:

- an abstention symbol `⊥` rendered as "source page not stated" — our `ABSENT`;
- a grounding constraint requiring a verbatim evidence span for every non-abstained value, with a post-hoc string check that rejects any tuple whose quotation does not occur in the source text;
- a gold annotation that may itself be `⊥` when no source states the field — our `NEG-ABSENT` ground truth;
- an explicit named failure mode of *hallucination*, defined as producing a value where the gold annotation is `⊥` — our kill condition `K1`;
- an explicit prohibition on world-knowledge imputation (no inferring chemistry from a dataset name);
- a provenance-ranked, stratified documentary space: landing page first, companion paper second, with conflicts surfaced rather than silently resolved;
- reported calibration error **and inter-annotator agreement**.

Every one of these was presented in the S2 candidate specification as a derived design decision. They are prior art, published two months before this document. The derivations in the candidate spec remain correct; they are not original.

### 5.2 What it does not do

BatteryLake's extracted field set is **experiment metadata** — chemistry, electrode materials, nominal capacity and voltage, temperature, charge/discharge protocol, C-rate, cutoff voltages, form factor, manufacturer, license. It is not export semantics.

The export-semantics parameters are handled as an *engineering obstacle to be normalised away*, not as a measurand:

- sign convention is fixed by fiat in the canonical model (`I > 0` on charge) and enforced by unit conversion and sign normalisation inside a synthesised converter;
- consistency rules check for *a single current sign convention* in the converted output, not for whether the depositor documented one;
- the physical-plausibility dimension is described as the one that catches unit errors and sign-convention bugs — values that pass schema validation but are physically impossible.

That last point is the crux. BatteryLake resolves sign convention **from the data** via physical plausibility. Our `S-DOC` / `S-FILE` stratification exists precisely to keep those apart: BatteryLake's method answers *can this file be made usable*, not *did the depositor state the rule*. It deliberately collapses the distinction our instrument is built to preserve, because its goal is a working data lake, not a measurement of documentation.

Additionally, its attribute mapping is explicitly permitted to bind a raw column using header text, embedded units, **or value statistics** — file-intrinsic and value-derived evidence treated as interchangeable with documentary evidence.

### 5.3 Its stated limitations are our target

The paper's own §6 concedes: the grounding constraint prevents unsupported values but cannot detect a source page that is itself wrong; the residual-risk bound conditions on correct reviewer decisions and calibrated confidences; and because converters run on the contributor's machine, the platform verifies *reports* of validation rather than re-executing it, with server-side re-validation listed as future work.

`[L2]` This strengthens rather than weakens the case for validation work in this class. A 41-dataset public benchmark spanning 12 curated datasets and roughly 323K cycles is now being assembled on an extraction instrument whose accuracy is measured against gold annotations of undisclosed provenance and whose validation step is self-reported. Independent qualification of that class of instrument has more value after this paper than before it, not less.

### 5.4 Live exposure question

BatteryLake states that every curated dataset ships a processing manifest recording raw-file inventory, mapping rules, unit conversions, cycle segmentation logic, label definitions, and validator version. If those manifests are public and include per-field `⊥` labels, then a portion of the S3 prevalence question is already answered in public for BatteryLake's field set and its 41 registered datasets — and any deposit in that set is exposed to the entire world, not merely to us.

I did not open those records. Opening them is itself an inspection decision with sampling consequences and belongs to the operator, not to the constructor. It is listed in §10.

---

## 6. Finding D — adjacent empirical assessments, and how close they get

- **\"Analysis of Open Li-ion Battery Testing Datasets…\"** (System Research in Energy, Mar 2026) grades fifteen open datasets partly by *metadata completeness*, and reports that some legacy corpora omit test-condition details such that secondary literature is needed to reconstruct them. This is the closest published empirical assessment. Its measurand is experimental-condition completeness (protocols, temperature, DOD), not export semantics, and its method is expert narrative judgement rather than a validated instrument.
- **dos Reis et al. 2021** (the S1/S3 sampling frame) is a survey of which datasets exist and which test variables and data are provided. It characterises availability, not documentary resolvability. It does not answer the question and remains usable as a frame.
- **\"Completeness of Datasets Documentation on ML/AI repositories\"** (arXiv 2503.13463) applies a Documentation Test Sheet to 100 dataset documentations across four ML repositories and reports that process-of-creation and maintenance information is poorly documented. Methodological precedent for measuring documentation completeness at corpus scale, in a different domain, with a different instrument.

None of these measures whether a named export-semantics convention is resolvable from a deposit's pinned documentation. The measurand survives.

---

## 7. Finding E — the validation method is fully anticipated

The S2 candidate's governing design decision (§1.1 of that document: ground truth written before the documentary artifact, because an adjudication instrument cannot be validated on labels produced by adjudication) is an established and named paradigm:

- **RIKER** (arXiv 2601.08847, Dec 2025) calls it paradigm inversion — generating documents *from* known ground truth rather than extracting ground truth from documents — and argues it gives deterministic scoring without human annotation and resistance to contamination through regenerable corpora. It further reports, across 33 models, that grounding ability and hallucination resistance are distinct capabilities: models that excel at finding facts that exist may still fabricate facts that do not.
- **VAREX** (arXiv 2603.15118) names the same construction *Reverse Annotation*, generating documents from structured data with deterministic value-level ground truth.
- **DTBench** (KDD 2026, arXiv 2602.13812) uses a reverse Table2Doc paradigm with a capability taxonomy, explicitly to avoid the cost and limited capability coverage of human-annotated pairs.
- **PSEBench** (arXiv 2606.05463) builds by-construction ground truth from regulatory clauses and states that it naturally supports generating *missing information* and *uncertain* variants — our `NEG-ABSENT` and `AMBIG-CONSTRUCTED` classes.
- **AbstentionBench** evaluates abstention under uncertainty, ambiguity and underspecification as a first-class capability.

The consequence is specific and uncomfortable. RIKER's finding that grounding and hallucination-resistance are distinct capabilities is the published version of the S2 candidate's §6.2 point 3 and the justification for gating stability on discrimination. We would not be discovering it; we would be re-confirming it on our own instrument.

---

## 8. Consequence for S2

S2 as specified is a competent application of a solved methodology to our own instrument. That is a **qualification step**, not research.

Reclassification, proposed:

```text
S2
INTERNAL_QUALIFICATION
Not a publishable research instance.
Purpose: establish that our instrument discriminates, is stable
under adjudicator substitution, and is deterministic — a
precondition for S3, nothing more.
No novelty claim. Cites RIKER / VAREX / DTBench / PSEBench for
method and BatteryLake for the battery-domain instantiation.
```

Three follow-on consequences:

1. **The budget case changes.** If S2 produces no publishable result, the 36-bundle / 576-adjudication design should be weighed against cheaper qualification routes — adapting an existing public abstention benchmark, or reducing to the minimum that demonstrates discrimination. That is a resourcing decision (§10).
2. **The dual-adjudication channel survives the reclassification.** Inter-adjudicator agreement is reported by BatteryLake but is not, in the published work, gated on demonstrated discriminative power. Gating it is a small methodological refinement we can defend and should keep — refinement, not contribution.
3. **The gate's first question changes.** A gate should now ask whether S2 is the cheapest adequate qualification, not whether it is a good study.

---

## 9. Consequence for S3

S3's question survives, but its novelty claim is now narrow and must be stated against BatteryLake rather than against a vacuum. What remains genuinely unoccupied:

- treating export-semantics resolvability as the **measurand**, where the published work treats it as an obstacle to be normalised;
- keeping `S-DOC` and `S-FILE` **separate and unranked**, where the published work permits value statistics to bind columns and resolves conventions by physical plausibility;
- recording disagreement rather than **resolving** it, where the published work routes conflicts to a human reviewer whose decisions are assumed correct;
- reporting a measurement about the corpus rather than admitting data into a lake.

`[L2]` My assessment is that this is a real and defensible contribution, and that it is roughly one paper's worth rather than the several the S1 framing implied. Anyone continuing should expect a reviewer to ask \"how is this not BatteryLake?\" in the first round, and the answer above needs to be in the abstract, not the discussion.

---

## 10. L3 decisions this document raises

1. **Accept or reject the reclassification of S2 to `INTERNAL_QUALIFICATION`.**
2. **Whether to open BatteryLake's released curation records** (§5.4). Doing so may answer part of the S3 question for free and will expose the constructor to per-dataset outcomes for up to 41 datasets, with sampling consequences. Not doing so leaves a known, public, directly relevant body of evidence unexamined. Both have costs; the decision is not mine.
3. **Qualification budget**: full 36-bundle build versus a reduced or adapted design (§8.1).
4. **Whether S3's frame remains dos Reis Table 2**, given that BatteryLake's 41-dataset registry is now a competing and partially overlapping frame with published curation outcomes.
5. **Whether a paywalled-literature sweep is commissioned** before freeze, since this search covered only open-access and abstract-level material (§2).

---

**Status:** `SPREMNO ZA GEJT`. Written by the S2 methodology drafter, who has a declared S1 conflict and who specified the architecture that §7 shows to be anticipated. The section most likely to be self-serving is §9 — the argument that a contribution survives — and that is where a gate should start.
