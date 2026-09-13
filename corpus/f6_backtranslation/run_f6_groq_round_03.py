#!/usr/bin/env python3

import ast
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
F6 = ROOT / "corpus/f6_backtranslation"

BASE_RUNNER = F6 / "run_f6_groq.py"
BLIND_INPUT = F6 / "F6_BLIND_INPUT_ROUND_03.jsonl"

OUTPUT = F6 / "F6_BACKTRANSLATION_RESPONSE_ROUND_03.jsonl"
SIDECAR = F6 / "F6_GROQ_EXECUTION_SIDECAR_ROUND_03.json"

RAW_DIR = F6 / "raw_groq_round_03"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 8
INTER_BATCH_SECONDS = 30
MAX_RETRIES = 5

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def extract_constant(name):
    tree = ast.parse(BASE_RUNNER.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise RuntimeError(f"Cannot extract {name} from {BASE_RUNNER}")

MODEL = extract_constant("MODEL")
PARTY = extract_constant("PARTY")
TEMPERATURE = extract_constant("TEMPERATURE")
RANDOM_SEED = extract_constant("RANDOM_SEED")
MAX_TOKENS = extract_constant("MAX_TOKENS_PER_BATCH")
SYSTEM_PROMPT = extract_constant("SYSTEM_PROMPT")

if MODEL != "qwen/qwen3.8-27b":
    sys.exit(f"HALT: unexpected model inherited from Attempt 01: {MODEL}")

if PARTY != "GROQ-CLEAN-P3-01":
    sys.exit(f"HALT: unexpected Party-3 identity: {PARTY}")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    sys.exit("HALT: GROQ_API_KEY environment variable is not set.")

if not BLIND_INPUT.exists():
    sys.exit(f"HALT: missing {BLIND_INPUT}")

def load_jsonl(path):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

blind_rows = load_jsonl(BLIND_INPUT)

if len(blind_rows) != 16:
    sys.exit(f"HALT: expected 16 Attempt-03 blind records, got {len(blind_rows)}")

for row in blind_rows:
    if set(row) != {"blind_id", "entry_text"}:
        sys.exit(
            f"HALT: metadata leakage in Attempt-03 blind input at "
            f"{row.get('blind_id')}"
        )

expected_ids = [x["blind_id"] for x in blind_rows]

if len(set(expected_ids)) != 16:
    sys.exit("HALT: Attempt-03 blind IDs are not unique.")

if len({x["entry_text"] for x in blind_rows}) != 16:
    sys.exit("HALT: Attempt-03 blind texts are not unique.")

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

EXPECTED_FIELDS = {
    "blind_id",
    "parameter",
    "scope",
    "evidence_stratum",
    "semantic_role",
    "semantic_value",
    "exclusive_assertion",
}

def response_schema(n):
    return {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "minItems": n,
                "maxItems": n,
                "items": {
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
                        "exclusive_assertion": {
                            "type": "boolean"
                        },
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
                },
            }
        },
        "required": ["records"],
        "additionalProperties": False,
    }

def make_user_prompt(chunk):
    payload = "\n".join(
        json.dumps(x, ensure_ascii=False)
        for x in chunk
    )

    return f"""You receive a batch of {len(chunk)} blind entries.

For EACH entry independently reconstruct the six semantic fields
according to the frozen Party-3 instructions.

Return exactly one record for every supplied blind_id and preserve
the supplied record order.

Return ONLY the required JSON object.

BLIND INPUT BATCH:
{payload}
"""

def call_groq(chunk):
    payload = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "seed": RANDOM_SEED,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": make_user_prompt(chunk),
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "f6_round_03_batch",
                "strict": True,
                "schema": response_schema(len(chunk)),
            },
        },
        "max_tokens": MAX_TOKENS,
    }

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "VolMax-S2-F6-Round03/1.0",
        },
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))

def validate_records(records, expected):
    expected_chunk_ids = [x["blind_id"] for x in expected]

    if len(records) != len(expected):
        raise ValueError(
            f"Expected {len(expected)} records, got {len(records)}"
        )

    actual_ids = [x.get("blind_id") for x in records]

    if actual_ids != expected_chunk_ids:
        raise ValueError(
            f"blind_id/order mismatch:\n"
            f"expected={expected_chunk_ids}\n"
            f"actual={actual_ids}"
        )

    for r in records:
        bid = r["blind_id"]

        if set(r) != EXPECTED_FIELDS:
            raise ValueError(f"wrong fields for {bid}")

        if r["parameter"] not in PARAMETERS:
            raise ValueError(f"invalid parameter for {bid}")

        if r["scope"] not in SCOPES:
            raise ValueError(f"invalid scope for {bid}")

        if r["evidence_stratum"] not in STRATA:
            raise ValueError(f"invalid evidence_stratum for {bid}")

        if r["semantic_role"] not in ROLES:
            raise ValueError(f"invalid semantic_role for {bid}")

        if r["semantic_role"] != "determining":
            if r["semantic_value"] is not None:
                raise ValueError(
                    f"non-determining semantic_value != null for {bid}"
                )

        if r["exclusive_assertion"]:
            if r["semantic_role"] != "determining":
                raise ValueError(
                    f"exclusive_assertion with non-determining role: {bid}"
                )

            if r["parameter"] not in {
                "E5", "E6", "E7a", "E7b"
            }:
                raise ValueError(
                    f"exclusive_assertion illegal for {bid}"
                )

chunks = [
    blind_rows[i:i + BATCH_SIZE]
    for i in range(0, len(blind_rows), BATCH_SIZE)
]

print("=== F6 ATTEMPT 03 — GROQ PARTY 3 [FINAL] ===")
print("party:", PARTY)
print("model:", MODEL)
print("records:", len(blind_rows))
print("batches:", [len(x) for x in chunks])
print("temperature:", TEMPERATURE)
print("seed:", RANDOM_SEED)
print("blind_sha256:", sha256(BLIND_INPUT))
print()

by_id = {}
batch_metadata = []

for index, chunk in enumerate(chunks, start=1):
    expected_chunk_ids = [x["blind_id"] for x in chunk]

    raw_file = RAW_DIR / f"batch_{index:02d}.json"

    print(
        f"[{index}/{len(chunks)}] "
        f"{expected_chunk_ids[0]}..{expected_chunk_ids[-1]} "
        f"({len(chunk)} records) ... ",
        end="",
        flush=True,
    )

    records = None
    raw = None

    if raw_file.exists():
        try:
            raw = json.loads(
                raw_file.read_text(encoding="utf-8")
            )
            content = raw["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            candidate = parsed["records"]

            validate_records(candidate, chunk)

            records = candidate
            print("CACHED")
        except Exception:
            records = None
            raw = None

    if records is None:
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                raw = call_groq(chunk)

                content = raw["choices"][0]["message"]["content"]
                parsed = json.loads(content)

                records = parsed["records"]

                validate_records(records, chunk)

                raw_file.write_text(
                    json.dumps(
                        raw,
                        indent=2,
                        ensure_ascii=False,
                    ) + "\n",
                    encoding="utf-8",
                )

                print("OK")
                break

            except Exception as exc:
                last_error = exc

                if attempt == MAX_RETRIES - 1:
                    break

                wait = 30 + 15 * attempt

                print(
                    f"RETRY ({exc}) — {wait}s ... ",
                    end="",
                    flush=True,
                )

                time.sleep(wait)

        if records is None:
            sys.exit(
                f"\nHALT: batch {index} failed after "
                f"{MAX_RETRIES} attempts: {last_error}"
            )

    for record in records:
        bid = record["blind_id"]

        if bid in by_id:
            sys.exit(f"HALT: duplicate returned blind_id {bid}")

        by_id[bid] = record

    batch_metadata.append({
        "batch_index": index,
        "record_count": len(chunk),
        "first_blind_id": expected_chunk_ids[0],
        "last_blind_id": expected_chunk_ids[-1],
        "raw_file": str(raw_file.relative_to(ROOT)),
        "raw_file_sha256": sha256(raw_file),
        "usage": raw.get("usage"),
        "model_returned": raw.get("model"),
    })

    if index < len(chunks):
        next_raw = RAW_DIR / f"batch_{index + 1:02d}.json"
        if not next_raw.exists():
            time.sleep(INTER_BATCH_SECONDS)

if set(by_id) != set(expected_ids):
    missing = sorted(set(expected_ids) - set(by_id))
    extra = sorted(set(by_id) - set(expected_ids))

    sys.exit(
        f"HALT: final blind ID mismatch\n"
        f"missing={missing}\n"
        f"extra={extra}"
    )

canonical_records = [by_id[x] for x in expected_ids]

if len(canonical_records) != 16:
    sys.exit(
        f"HALT: expected final 16 records, "
        f"got {len(canonical_records)}"
    )

OUTPUT.write_text(
    "".join(
        json.dumps(
            x,
            ensure_ascii=False,
            separators=(",", ":"),
        ) + "\n"
        for x in canonical_records
    ),
    encoding="utf-8",
)

sidecar = {
    "stage": "F6",
    "attempt": 3,
    "party": PARTY,
    "model_requested": MODEL,
    "temperature": TEMPERATURE,
    "random_seed": RANDOM_SEED,
    "record_count": 16,
    "execution_transport": "sequential_batches",
    "batch_sizes": [len(x) for x in chunks],
    "inter_batch_seconds": INTER_BATCH_SECONDS,
    "blind_input_sha256": sha256(BLIND_INPUT),
    "output_sha256": sha256(OUTPUT),
    "base_party3_runner_sha256": sha256(BASE_RUNNER),
    "batches": batch_metadata,
    "note": (
        "Attempt-03 Party-3 validation receives only the "
        "16 final replacement blind texts. No private-key metadata "
        "is supplied to the provider."
    ),
}

SIDECAR.write_text(
    json.dumps(
        sidecar,
        indent=2,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print()
print("F6 ATTEMPT 03 BACK-TRANSLATION COMPLETE — 16 RECORDS")
print("output:", OUTPUT)
print("output_sha256:", sha256(OUTPUT))
print("sidecar:", SIDECAR)
print()
print("PRIVATE KEY HAS NOT BEEN LOADED BY THIS RUNNER.")
print("COMPARATOR HAS NOT BEEN RUN.")
