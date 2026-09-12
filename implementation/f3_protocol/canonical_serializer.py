"""
Canonical Serializer for S2 Deposit Semantics Adjudication.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§6.1, §6.6, §7).
"""

from typing import Any, Dict, List, Union
import json
import decimal
from decimal import Decimal


def serialize_canonical_numeric(val: Union[int, float, str, Decimal]) -> str:
    """
    §6.6 Canonical numeric serialization (frozen):
    - Decimal only, never exponent.
    - Integers with no decimal point and no trailing zeros (e.g. 10).
    - Non-integers to 6 significant digits, trailing zeros stripped (e.g. 1.5, 0.123456).
    - No leading '+'.
    - Single leading '-'.
    - No thousands separators.
    - '10', '10.0', and '1e1' are one byte value ("10").
    """
    if isinstance(val, str):
        val = val.strip().lstrip("+")
        d = Decimal(val)
    elif isinstance(val, (int, float, Decimal)):
        d = Decimal(str(val))
    else:
        raise TypeError(f"Unsupported numeric type: {type(val)}")

    # Check if exactly an integer
    if d == d.to_integral_value():
        int_val = int(d.to_integral_value())
        return str(int_val)

    # Format to 6 significant digits
    # Use context with precision 6
    ctx = decimal.Context(prec=6, rounding=decimal.ROUND_HALF_EVEN)
    d_sig = d.quantize(Decimal(1), context=ctx) if d == d.to_integral() else +d
    # Format with 6 sig digits in decimal notation (never exponential)
    formatted = f"{d:.6g}"
    if "e" in formatted.lower():
        # Expand scientific notation to plain decimal
        # Parse exponent
        d_val = Decimal(formatted)
        formatted = format(d_val, "f")

    # Strip trailing zeros and trailing decimal point
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")

    # Ensure no leading +
    formatted = formatted.lstrip("+")
    return formatted


def serialize_canonical_semantic_value(val: Any) -> str:
    """
    Serialize semantic value canonically.
    For sets: sort elements and serialize as sorted comma-separated list or JSON.
    For numeric payloads (e.g. fixed(10 s), factor(2), affine(2, 1)):
    Apply §6.6 to numeric fields.
    """
    if val is None:
        return "null"
    if isinstance(val, (int, float, Decimal)):
        return serialize_canonical_numeric(val)
    if isinstance(val, str):
        return val
    if isinstance(val, (list, set)):
        sorted_vals = sorted([serialize_canonical_semantic_value(x) for x in val])
        return "[" + ",".join(sorted_vals) + "]"
    if isinstance(val, dict):
        keys = sorted(val.keys())
        items = [f"{k}:{serialize_canonical_semantic_value(val[k])}" for k in keys]
        return "{" + ",".join(items) + "}"
    return str(val)


def serialize_adjudication_record(record: Dict[str, Any]) -> str:
    """
    §6.1 Adjudication record serializer:
    Fixed field order:
    - parameter_id
    - scope
    - verdict_class
    - readings: [ { semantic_value, evidence_stratum, artifact_sha256, locator, verbatim_excerpt } ]
    - traversal_record (optional, required for ABSENT and NOT_APPLICABLE)

    Prohibitions:
    - note_text is strictly prohibited.
    - No timestamps, no run IDs, no model-version strings.
    - Readings sorted lexicographically by canonical serialization of semantic_value.
    """
    if "note_text" in record:
        raise ValueError("note_text is strictly prohibited in adjudication records (§6.1)")

    output: Dict[str, Any] = {}
    
    # Enforce field order
    output["parameter_id"] = record["parameter_id"]
    output["scope"] = record["scope"]
    output["verdict_class"] = record["verdict_class"]

    readings = record.get("readings", [])
    formatted_readings = []
    for r in readings:
        r_entry = {
            "semantic_value": r.get("semantic_value"),
            "evidence_stratum": r.get("evidence_stratum"),
            "artifact_sha256": r.get("artifact_sha256"),
            "locator": r.get("locator"),
            "verbatim_excerpt": r.get("verbatim_excerpt"),
        }
        formatted_readings.append(r_entry)

    # Sort readings lexicographically by canonical serialization of semantic_value
    formatted_readings.sort(key=lambda x: serialize_canonical_semantic_value(x["semantic_value"]))
    output["readings"] = formatted_readings

    if "traversal_record" in record:
        output["traversal_record"] = record["traversal_record"]

    # Byte-deterministic JSON serialization: 2-space indent, sorted keys=False (we fixed order)
    return json.dumps(output, indent=2, ensure_ascii=False)
