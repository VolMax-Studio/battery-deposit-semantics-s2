#!/usr/bin/env python3
import json
import os
import sys
import hashlib
from pathlib import Path

try:
    from mistralai import Mistral
except ImportError:
    try:
        from mistralai.client import Mistral
    except ImportError:
        sys.exit("HALT: mistralai package not installed. Run: pip install -U mistralai")

try:
    from mistralai.models import JSONSchema, ResponseFormat
except ImportError:
    try:
        from mistralai.client.models import JSONSchema, ResponseFormat
    except ImportError:
        ResponseFormat = None
        JSONSchema = None

ROOT = Path(__file__).resolve().parents[2]
F6_DIR = ROOT / "corpus/f6_backtranslation"
BLIND_INPUT = F6_DIR / "F6_BLIND_INPUT.jsonl"
OUTPUT_JSONL = F6_DIR / "F6_BACKTRANSLATION_RESPONSE_01.jsonl"
RAW_RESPONSE = F6_DIR / "F6_MISTRAL_RAW_RESPONSE_01.json"
SIDECAR = F6_DIR / "F6_MISTRAL_EXECUTION_SIDECAR_01.json"

MODEL = "mistral-medium-2604"
PARTY = "MISTRAL-CLEAN-P3-01"
SOURCE_F5_SHA = "e9b93b7baefee365b93d59002c225a6d22f09b6a"
ROLE_SUBSTITUTION_SHA = "eadbb8d46d50f8bcf35239be84f3b511e69c4090"
TEMPERATURE = 0.0
RANDOM_SEED = 20260913
MAX_TOKENS = 50000

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
        "parameter": {
            "type": "string",
            "enum": PARAMETERS,
        },
        "scope": {
            "type": "string",
            "enum": SCOPES,
        },
        "evidence_stratum": {
            "type": "string",
            "enum": STRATA,
        },
        "semantic_role": {
            "type": "string",
            "enum": ROLES,
        },
        "semantic_value": {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {"type": "string"},
                },
                {"type": "null"},
            ]
        },
        "exclusive_assertion": {"type": "boolean"},
    },
    "required": [
        "blind_id",
        "parameter",
        "scope",
        "evidence_stratum",
        "semantic_role",
        "semantic_value",
        "exclusive_assertion",
    ],
    "additionalProperties": False,
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "records": {
            "type": "array",
            "minItems": 330,
            "maxItems": 330,
            "items": RECORD_SCHEMA,
        }
    },
    "required": ["records"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = r"""
You are MISTRAL-CLEAN-P3-01, Party 3 — Bank Validator.

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
Value: non-empty set over:
fixed(interval_seconds)
event_driven(delta_voltage)
event_driven(delta_current)
event_driven(step_transition)
Preserve the numeric interval_seconds stated in the text.

E6
Question: By what rule is the absence of unlogged gaps in this signal established?
Scopes: current, voltage, power, temperature
Value: non-empty set over:
completeness_counter
expected_count_comparison
gap_flag_column
acquisition_log_reconciliation

E7a
Question: By what rule does a record map to this operation identifier?
Scopes: step_index, cycle_index, test_index
Value: non-empty set over:
explicit_index_column
filename_encoding
time_segmentation_rule
row_grouping_marker

E7b
Question: By what rule is operational state (charge / discharge / rest) encoded in a record?
Scope: dataset
Value: non-empty set over:
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
Preserve numeric payloads from the text.

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
Do not provide explanations.
"""

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def object_to_dict(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if hasattr(obj, "dict"):
        return obj.dict()
    return {"repr": repr(obj)}

if not BLIND_INPUT.exists():
    sys.exit(
        f"HALT: missing {BLIND_INPUT}\n"
        "Build the frozen F6 blind package before protected exposure."
    )

api_key = os.environ.get("MISTRAL_API_KEY")
KEY_FILE = Path("/home/volmax-studio/Documents/Kljucevi/mistralapi.txt")
if not api_key and KEY_FILE.exists():
    api_key = KEY_FILE.read_text(encoding="utf-8").strip()

if not api_key:
    sys.exit("HALT: MISTRAL_API_KEY is not set.")

blind_rows = [
    json.loads(line)
    for line in BLIND_INPUT.read_text().splitlines()
    if line.strip()
]
if len(blind_rows) != 330:
    sys.exit(f"HALT: expected 330 blind records, got {len(blind_rows)}")

expected_ids = [x["blind_id"] for x in blind_rows]
if len(set(expected_ids)) != 330:
    sys.exit("HALT: blind_id values are not unique.")

for row in blind_rows:
    if set(row.keys()) != {"blind_id", "entry_text"}:
        sys.exit(
            f"HALT: protected metadata leakage in blind input "
            f"at {row.get('blind_id')}"
        )

user_payload = {
    "task": "Frozen F6 role-aware back-translation",
    "records": blind_rows,
}

client = Mistral(api_key=api_key)

print("=== F6 MISTRAL EXECUTION ===")
print("party:", PARTY)
print("model:", MODEL)
print("records:", len(blind_rows))
print("blind_sha256:", sha256(BLIND_INPUT))
print("temperature:", TEMPERATURE)
print("random_seed:", RANDOM_SEED)
print()
print("PROTECTED EXPOSURE STARTS WITH THIS API CALL")

# Construct response format
if ResponseFormat and JSONSchema:
    resp_fmt = ResponseFormat(
        type="json_schema",
        json_schema=JSONSchema(
            name="f6_backtranslation_response",
            schema_definition=RESPONSE_SCHEMA,
            strict=True,
        ),
    )
else:
    resp_fmt = {"type": "json_object"}

response = client.chat.complete(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": json.dumps(
                user_payload,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        },
    ],
    response_format=resp_fmt,
    temperature=TEMPERATURE,
    random_seed=RANDOM_SEED,
    max_tokens=MAX_TOKENS,
)

raw_dump = object_to_dict(response)
RAW_RESPONSE.write_text(
    json.dumps(raw_dump, indent=2, ensure_ascii=False) + "\n"
)

content = response.choices[0].message.content
if not isinstance(content, str):
    sys.exit(
        "HALT: expected textual JSON content in assistant response."
    )

try:
    parsed = json.loads(content)
except json.JSONDecodeError as exc:
    sys.exit(f"HALT: response is not valid JSON: {exc}")

records = parsed.get("records")
if not isinstance(records, list):
    sys.exit("HALT: response has no records array.")

if len(records) != 330:
    sys.exit(f"HALT: expected 330 output records, got {len(records)}")

returned_ids = [r.get("blind_id") for r in records]
if len(set(returned_ids)) != 330:
    sys.exit("HALT: duplicate blind_id in Mistral output.")

if set(returned_ids) != set(expected_ids):
    missing = sorted(set(expected_ids) - set(returned_ids))
    extra = sorted(set(returned_ids) - set(expected_ids))
    sys.exit(
        f"HALT: blind_id set mismatch.\n"
        f"missing={missing}\nextra={extra}"
    )

expected_fields = {
    "blind_id",
    "parameter",
    "scope",
    "evidence_stratum",
    "semantic_role",
    "semantic_value",
    "exclusive_assertion",
}

by_id = {}
for record in records:
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
            sys.exit(
                f"HALT: non-determining/non-applicable "
                f"semantic_value must be null for {bid}"
            )
    if record["exclusive_assertion"]:
        if record["semantic_role"] != "determining":
            sys.exit(f"HALT: invalid exclusive_assertion for {bid}")
        if record["parameter"] not in {"E5", "E6", "E7a", "E7b"}:
            sys.exit(f"HALT: exclusive_assertion illegal for {bid}")
    by_id[bid] = record

# Canonical transport order = original blind-input order.
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
    "model_returned": getattr(response, "model", None),
    "source_f5_commit": SOURCE_F5_SHA,
    "role_substitution_commit": ROLE_SUBSTITUTION_SHA,
    "blind_input_sha256": sha256(BLIND_INPUT),
    "output_sha256": sha256(OUTPUT_JSONL),
    "raw_response_sha256": sha256(RAW_RESPONSE),
    "record_count": len(canonical_records),
    "temperature": TEMPERATURE,
    "random_seed": RANDOM_SEED,
    "max_tokens": MAX_TOKENS,
    "response_format": "json_schema strict",
    "usage": object_to_dict(getattr(response, "usage", None)),
    "note": (
        "Party-3 protected exposure began at the API call. "
        "No F5 private key or authored semantic metadata was supplied."
    ),
}

SIDECAR.write_text(
    json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n"
)

print()
print("F6 BACK-TRANSLATION RESPONSE 01 COMPLETE — 330 RECORDS.")
print("output:", OUTPUT_JSONL)
print("output_sha256:", sha256(OUTPUT_JSONL))
print("raw_response:", RAW_RESPONSE)
print("sidecar:", SIDECAR)
print()
print("IMPORTANT: comparator has NOT been run.")
print("Mistral has NOT seen F6_PRIVATE_KEY.jsonl.")
