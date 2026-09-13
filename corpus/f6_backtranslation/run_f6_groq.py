#!/usr/bin/env python3
"""
F6 Back-Translation Runner via Groq Cloud API
Party: GROQ-CLEAN-P3-01
Model: qwen/qwen3.8-27b

Reads: corpus/f6_backtranslation/F6_BLIND_INPUT.jsonl
Writes: corpus/f6_backtranslation/F6_BACKTRANSLATION_RESPONSE_01.jsonl
"""

import json
import os
import sys
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
F6_DIR = ROOT / "corpus/f6_backtranslation"
BLIND_INPUT = F6_DIR / "F6_BLIND_INPUT.jsonl"
OUTPUT_JSONL = F6_DIR / "F6_BACKTRANSLATION_RESPONSE_01.jsonl"
SIDECAR = F6_DIR / "F6_GROQ_EXECUTION_SIDECAR_01.json"
RAW_DIR = F6_DIR / "raw_groq"
RAW_DIR.mkdir(parents=True, exist_ok=True)

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    sys.exit("HALT: GROQ_API_KEY environment variable is not set.")

if not BLIND_INPUT.exists():
    sys.exit(f"HALT: missing {BLIND_INPUT}\nBuild the frozen F6 blind package before protected exposure.")

blind_rows = [json.loads(line) for line in BLIND_INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
if len(blind_rows) != 330:
    sys.exit(f"HALT: expected 330 blind records, got {len(blind_rows)}")

expected_ids = [x["blind_id"] for x in blind_rows]
if len(set(expected_ids)) != 330:
    sys.exit("HALT: blind_id values are not unique.")

for row in blind_rows:
    if set(row.keys()) != {"blind_id", "entry_text"}:
        sys.exit(f"HALT: protected metadata leakage in blind input at {row.get('blind_id')}")

MODEL = "qwen/qwen3.8-27b"
PARTY = "GROQ-CLEAN-P3-01"
SOURCE_F5_SHA = "e9b93b7baefee365b93d59002c225a6d22f09b6a"
ROLE_SUBSTITUTION_SHA = "b72024073649f65e854349eedb06b6cad9c1fe50"
TEMPERATURE = 0.0
RANDOM_SEED = 20260913
BATCH_SIZE = 33
BATCH_COUNT = 10
MAX_TOKENS_PER_BATCH = 4096
INTER_BATCH_SECONDS = 30

PARAMETERS = [
    "E1", "E2", "E3", "E4a", "E4b",
    "E5", "E6", "E7a", "E7b", "E8a", "E8b"
]

SCOPES = [
    "current", "voltage", "power",
    "capacity_charge", "capacity_discharge",
    "energy", "temperature", "time",
    "step_index", "cycle_index", "test_index", "dataset"
]

STRATA = ["S-DOC", "S-FILE"]

ROLES = [
    "determining",
    "non_determining_adjacent",
    "non_applicable"
]

RECORD_SCHEMA = {
    "type": "object",
    "properties": {
        "blind_id": {"type": "string"},
        "parameter": {"type": "string", "enum": PARAMETERS},
        "scope": {"type": "string", "enum": SCOPES},
        "evidence_stratum": {"type": "string", "enum": STRATA},
        "semantic_role": {"type": "string", "enum": ROLES},
        "semantic_value": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
                {"type": "null"}
            ]
        },
        "exclusive_assertion": {"type": "boolean"}
    },
    "required": [
        "blind_id", "parameter", "scope",
        "evidence_stratum", "semantic_role",
        "semantic_value", "exclusive_assertion"
    ],
    "additionalProperties": False
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "records": {
            "type": "array",
            "minItems": BATCH_SIZE,
            "maxItems": BATCH_SIZE,
            "items": RECORD_SCHEMA
        }
    },
    "required": ["records"],
    "additionalProperties": False
}

SYSTEM_PROMPT = r"""You are GROQ-CLEAN-P3-01, Party 3 — Bank Validator.

Your role is limited exclusively to frozen F6 role-aware back-translation.

You did not author the bank. Do not perform corpus construction, adjudication, fidelity checking, scoring, gate review, or methodology redesign.

You receive shuffled entry texts stripped of authored semantic metadata.

For EACH entry independently reconstruct exactly these six semantic fields:

1. parameter
2. scope
3. evidence_stratum
4. semantic_role
5. semantic_value
6. exclusive_assertion

blind_id is transport metadata only.

FROZEN STRATA

S-DOC: Article-style text, README, data dictionary, or declared prose. It supports the proposition that the depositor stated a rule.
S-FILE: Declared in-file labels only: column names, header rows, declared unit strings, explicit legends, metadata labels, or explicit comment lines.

Do not infer semantics from numeric/value patterns.

FROZEN PARAMETERS

E1
Question: Which sign of this signal denotes charge?
Scopes: current, power
Values: charge_positive, discharge_positive

E2
Question: Does a zero in this signal denote a measured value or a placeholder for an unrecorded value?
Scopes: current, voltage, power, temperature
Values: measured, placeholder

E3
Question: What is the finest operational boundary at which this cumulative quantity resets to zero?
Scopes: capacity_charge, capacity_discharge, energy, time
Values: step, cycle, test, never

E4a
Question: Does this signal's interval timestamp denote start, end, or midpoint?
Scopes: current, voltage, power, temperature
Values: start, end, midpoint

E4b
Question: Which endpoint convention governs this signal's intervals?
Scopes: current, voltage, power, temperature
Values: closed_closed, open_open, closed_open, open_closed

E5
Question: What rule governs the interval between logged records of this signal?
Scopes: current, voltage, power, temperature
Value: non-empty set (JSON array of strings) over:
fixed(interval_seconds)
event_driven(delta_voltage)
event_driven(delta_current)
event_driven(step_transition)
Preserve the numeric interval_seconds stated in the text (e.g. "fixed(10 s)", "fixed(5 s)", "fixed(1 s)", "fixed(30 s)", "fixed(2 s)").

E6
Question: By what rule is the absence of unlogged gaps in this signal established?
Scopes: current, voltage, power, temperature
Value: non-empty set (JSON array of strings) over:
completeness_counter
expected_count_comparison
gap_flag_column
acquisition_log_reconciliation

E7a
Question: By what rule does a record map to this operation identifier?
Scopes: step_index, cycle_index, test_index
Value: non-empty set (JSON array of strings) over:
explicit_index_column
filename_encoding
time_segmentation_rule
row_grouping_marker

E7b
Question: By what rule is operational state (charge / discharge / rest) encoded in a record?
Scope: dataset
Value: non-empty set (JSON array of strings) over:
step_type_column
current_sign
separate_state_column
mode_code_enum

E8a
Question: In what physical unit is this signal reported?
current: A or mA
voltage: V or mV

E8b
Question: What scaling was applied to this signal?
Scopes: current, voltage, power, capacity_charge, capacity_discharge, energy, temperature, time
Canonical values:
none
factor(x), where x != 1
affine(factor, offset), where offset != 0
Preserve numeric payloads from the text (e.g. "factor(2)", "factor(10)", "affine(2, 1)", "affine(0.5, -1)", "factor(1000)", "affine(1.5, 0.5)", "factor(0.001)").

SEMANTIC ROLES

determining: The text itself determines a canonical semantic value. semantic_value MUST be non-null.
non_determining_adjacent: The text is related to the parameter but does not determine a canonical answer. semantic_value MUST be null.
non_applicable: The text establishes that the governed semantic question does not apply. semantic_value MUST be null.

EXCLUSIVE_ASSERTION

Return true only when:
- semantic_role = determining;
- parameter is E5, E6, E7a, or E7b;
- the text explicitly asserts that the stated set is exclusive.
Otherwise false.

Do not infer class, placement, bundle number, ground truth, corpus composition, or authored metadata.
Return exactly one record for every supplied blind_id.
Do not omit records.
Do not invent extra blind_ids.
Do not provide explanations outside JSON.
"""

def make_user_prompt(chunk):
    chunk_text = "\n".join(json.dumps(item, ensure_ascii=False) for item in chunk)
    return f"""You receive a batch of {len(chunk)} blind entries.
For EACH entry independently reconstruct the six semantic fields.

Output MUST be a single valid JSON object with top-level key "records" containing exactly {len(chunk)} items in matching order from {chunk[0]['blind_id']} to {chunk[-1]['blind_id']}.

Each object in "records" must have:
- "blind_id": "{chunk[0]['blind_id']}" etc.
- "parameter": "E1"|"E2"|"E3"|"E4a"|"E4b"|"E5"|"E6"|"E7a"|"E7b"|"E8a"|"E8b"
- "scope": one of the 12 frozen scopes
- "evidence_stratum": "S-DOC" or "S-FILE"
- "semantic_role": "determining"|"non_determining_adjacent"|"non_applicable"
- "semantic_value": canonical string, array of strings for sets, or null
- "exclusive_assertion": boolean (true/false)

BLIND INPUT BATCH:
{chunk_text}
"""

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def call_groq_batch(user_prompt):
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "seed": RANDOM_SEED,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "f6_batch",
                "strict": True,
                "schema": RESPONSE_SCHEMA
            }
        },
        "max_tokens": MAX_TOKENS_PER_BATCH
    }
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=req_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "VolMax-S2-F6-Runner/1.0"
        }
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("=== F6 GROQ EXECUTION ===")
print("party:", PARTY)
print("model:", MODEL)
print("records:", len(blind_rows))
print("blind_sha256:", sha256(BLIND_INPUT))
print("temperature:", TEMPERATURE)
print("random_seed:", RANDOM_SEED)
print(f"transport: {BATCH_COUNT} batches of {BATCH_SIZE} records")
print(f"inter_batch_delay: {INTER_BATCH_SECONDS}s")
print()
print("PROTECTED EXPOSURE STARTS WITH THIS API CALL")

expected_fields = {
    "blind_id", "parameter", "scope",
    "evidence_stratum", "semantic_role",
    "semantic_value", "exclusive_assertion",
}

by_id = {}
raw_batch_metadata = []

for b_idx in range(BATCH_COUNT):
    start_idx = b_idx * BATCH_SIZE
    end_idx = (b_idx + 1) * BATCH_SIZE
    chunk = blind_rows[start_idx:end_idx]
    chunk_expected_ids = [r["blind_id"] for r in chunk]
    raw_file = RAW_DIR / f"batch_{b_idx+1:02d}.json"

    print(f"[{b_idx+1}/{BATCH_COUNT}] Processing {chunk_expected_ids[0]}..{chunk_expected_ids[-1]} ({len(chunk)} items)... ", end="", flush=True)

    parsed_records = None
    if raw_file.exists():
        try:
            cached_dump = json.loads(raw_file.read_text(encoding="utf-8"))
            content = cached_dump["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            recs = parsed.get("records", [])
            if len(recs) == BATCH_SIZE and [r.get("blind_id") for r in recs] == chunk_expected_ids:
                parsed_records = recs
                raw_dump = cached_dump
                print("CACHED")
        except Exception:
            parsed_records = None

    if parsed_records is None:
        user_prompt = make_user_prompt(chunk)
        max_retries = 5
        for attempt in range(max_retries):
            try:
                raw_dump = call_groq_batch(user_prompt)
                content = raw_dump["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                recs = parsed.get("records")
                if not recs and isinstance(parsed, list):
                    recs = parsed
                if not recs:
                    for v in parsed.values():
                        if isinstance(v, list):
                            recs = v
                            break
                if len(recs) != BATCH_SIZE:
                    raise ValueError(f"Expected {BATCH_SIZE} records, got {len(recs)}")
                recs_ids = [r.get("blind_id") for r in recs]
                if recs_ids != chunk_expected_ids:
                    raise ValueError(f"blind_id mismatch: {recs_ids} vs {chunk_expected_ids}")

                raw_file.write_text(json.dumps(raw_dump, indent=2, ensure_ascii=False) + "\n")
                parsed_records = recs
                print("OK")
                break
            except Exception as e:
                err_str = str(e)
                wait_time = 30 + attempt * 15
                print(f"RETRY ({e}), waiting {wait_time}s... ", end="", flush=True)
                time.sleep(wait_time)
        else:
            sys.exit(f"\nHALT: Failed batch {b_idx+1} after {max_retries} retries.")

    for record in parsed_records:
        bid = record["blind_id"]
        if set(record.keys()) != expected_fields:
            sys.exit(f"HALT: wrong fields for {bid}")
        if record["parameter"] not in PARAMETERS:
            sys.exit(f"HALT: invalid parameter for {bid}")
        if record["scope"] not in SCOPES:
            sys.exit(f"HALT: invalid scope for {bid}")
        if record["evidence_stratum"] not in STRATA:
            sys.exit(f"HALT: invalid evidence_stratum for {bid}")
        if record["semantic_role"] not in ROLES:
            sys.exit(f"HALT: invalid semantic_role for {bid}")
        if record["semantic_role"] != "determining":
            if record["semantic_value"] is not None:
                sys.exit(f"HALT: non-determining/non-applicable semantic_value must be null for {bid}")
        if record["exclusive_assertion"]:
            if record["semantic_role"] != "determining":
                sys.exit(f"HALT: invalid exclusive_assertion for {bid}")
            if record["parameter"] not in {"E5", "E6", "E7a", "E7b"}:
                sys.exit(f"HALT: exclusive_assertion illegal for {bid}")
        by_id[bid] = record

    raw_batch_metadata.append({
        "batch_index": b_idx + 1,
        "raw_file": str(raw_file.relative_to(ROOT)),
        "raw_file_sha256": sha256(raw_file),
        "usage": raw_dump.get("usage"),
    })

    if b_idx < BATCH_COUNT - 1:
        next_file = RAW_DIR / f"batch_{b_idx+2:02d}.json"
        if not next_file.exists():
            time.sleep(INTER_BATCH_SECONDS)

assert len(by_id) == 330, f"Expected 330 records, got {len(by_id)}"
canonical_records = [by_id[bid] for bid in expected_ids]

OUTPUT_JSONL.write_text(
    "".join(
        json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n"
        for r in canonical_records
    )
)

sidecar = {
    "stage": "F6",
    "party": PARTY,
    "model_requested": MODEL,
    "source_f5_commit": SOURCE_F5_SHA,
    "blind_input_sha256": sha256(BLIND_INPUT),
    "output_sha256": sha256(OUTPUT_JSONL),
    "record_count": len(canonical_records),
    "temperature": TEMPERATURE,
    "random_seed": RANDOM_SEED,
    "execution_transport": "sequential_batches",
    "batch_size": BATCH_SIZE,
    "batch_count": BATCH_COUNT,
    "inter_batch_seconds": INTER_BATCH_SECONDS,
    "max_tokens_per_batch": MAX_TOKENS_PER_BATCH,
    "response_format": "json_schema strict",
    "batches": raw_batch_metadata,
    "note": (
        "Party-3 protected exposure began at the API call. "
        "No F5 private key or authored semantic metadata was supplied."
    ),
}

SIDECAR.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")

print()
print("F6 BACK-TRANSLATION RESPONSE 01 COMPLETE — 330 RECORDS.")
print("output:", OUTPUT_JSONL)
print("output_sha256:", sha256(OUTPUT_JSONL))
print("sidecar:", SIDECAR)
print()
print("IMPORTANT: comparator has NOT been run.")
print("Groq has NOT seen F6_PRIVATE_KEY.jsonl.")
