"""
Canonical Serializer for S2 Deposit Semantics Adjudication.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§6.1, §6.6, §7).
"""

from typing import Any, Dict, List, Union
import json
import re
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

    # Format with 6 sig digits in decimal notation (never exponential)
    formatted = f"{d:.6g}"
    if "e" in formatted.lower():
        d_val = Decimal(formatted)
        formatted = format(d_val, "f")

    # Strip trailing zeros and trailing decimal point
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")

    formatted = formatted.lstrip("+")
    return formatted


def canonicalize_frozen_typed_payload(val_str: str) -> str:
    """
    Strict canonicalization restricted ONLY to frozen typed forms from §4.1, §4.3, §5.2.1:
    - fixed(<interval_seconds> s) or fixed(<interval_seconds>)
    - factor(<factor_value>)
    - affine(<factor_value>, <offset_value>)
    Arbitrary strings are returned verbatim.
    """
    # 1. fixed(...) pattern
    m_fixed = re.match(r"^fixed\(\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*(s)?\s*\)$", val_str.strip())
    if m_fixed:
        num_part = m_fixed.group(1)
        has_s = m_fixed.group(2) is not None
        canon_num = serialize_canonical_numeric(num_part)
        return f"fixed({canon_num} s)" if has_s else f"fixed({canon_num})"

    # 2. factor(...) pattern
    m_factor = re.match(r"^factor\(\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*\)$", val_str.strip())
    if m_factor:
        num_part = m_factor.group(1)
        canon_num = serialize_canonical_numeric(num_part)
        return f"factor({canon_num})"

    # 3. affine(...) pattern
    m_affine = re.match(
        r"^affine\(\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*,\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*\)$",
        val_str.strip(),
    )
    if m_affine:
        fac_part = m_affine.group(1)
        off_part = m_affine.group(2)
        canon_fac = serialize_canonical_numeric(fac_part)
        canon_off = serialize_canonical_numeric(off_part)
        return f"affine({canon_fac}, {canon_off})"

    # Return any other string verbatim (do NOT canonicalize arbitrary text or numbers)
    return val_str


def canonicalize_semantic_value(val: Any) -> Any:
    """
    Canonicalize semantic_value BEFORE placing it in the serialized output record:
    - Scalar numbers (int, float, Decimal): serialized via §6.6 as canonical string bytes (no int/float cast).
    - Strings: strictly restricted to frozen typed forms (fixed, factor, affine), else verbatim.
    - Lists and sets: recursively canonicalized and sorted canonically.
    - Dicts: keys sorted, values recursively canonicalized.
    """
    if val is None:
        return None

    # Scalar numbers: convert directly to §6.6 canonical string. No int() or float() conversion!
    if isinstance(val, (int, float, Decimal)):
        return serialize_canonical_numeric(val)

    if isinstance(val, str):
        return canonicalize_frozen_typed_payload(val)

    if isinstance(val, (list, set)):
        canon_elements = [canonicalize_semantic_value(x) for x in val]
        return sorted(canon_elements, key=lambda x: serialize_canonical_semantic_value_string(x))

    if isinstance(val, dict):
        canon_dict = {}
        for k in sorted(val.keys()):
            canon_dict[k] = canonicalize_semantic_value(val[k])
        return canon_dict

    return val


def serialize_canonical_semantic_value_string(val: Any) -> str:
    """
    Produce a canonical string representation used for lexicographical sorting of readings.
    """
    canon_val = canonicalize_semantic_value(val)
    if canon_val is None:
        return "null"
    if isinstance(canon_val, str):
        return canon_val
    if isinstance(canon_val, list):
        items = [serialize_canonical_semantic_value_string(x) for x in canon_val]
        return "[" + ",".join(items) + "]"
    if isinstance(canon_val, dict):
        items = [f"{k}:{serialize_canonical_semantic_value_string(canon_val[k])}" for k in sorted(canon_val.keys())]
        return "{" + ",".join(items) + "}"
    return str(canon_val)


def serialize_adjudication_record(record: Dict[str, Any]) -> str:
    """
    §6.1 Adjudication record serializer:
    Fixed field order:
    - parameter_id
    - scope
    - verdict_class
    - readings: [ { semantic_value, evidence_stratum, artifact_sha256, locator, verbatim_excerpt } ]
    - traversal_record (optional, required for ABSENT and NOT_APPLICABLE)

    Enforces:
    - semantic_value in output is CANONICALIZED before placement.
    - Set/list values are themselves sorted canonically.
    - Readings sorted lexicographically by canonical string of semantic_value.
    - note_text is strictly prohibited (§6.1).
    - No timestamps, no run IDs, no model-version strings.
    """
    if "note_text" in record:
        raise ValueError("note_text is strictly prohibited in adjudication records (§6.1)")

    output: Dict[str, Any] = {}

    output["parameter_id"] = record["parameter_id"]
    output["scope"] = record["scope"]
    output["verdict_class"] = record["verdict_class"]

    readings = record.get("readings", [])
    formatted_readings = []
    for r in readings:
        canon_val = canonicalize_semantic_value(r.get("semantic_value"))
        r_entry = {
            "semantic_value": canon_val,
            "evidence_stratum": r.get("evidence_stratum"),
            "artifact_sha256": r.get("artifact_sha256"),
            "locator": r.get("locator"),
            "verbatim_excerpt": r.get("verbatim_excerpt"),
        }
        formatted_readings.append(r_entry)

    # Sort readings lexicographically by canonical string representation of semantic_value
    formatted_readings.sort(key=lambda x: serialize_canonical_semantic_value_string(x["semantic_value"]))
    output["readings"] = formatted_readings

    if "traversal_record" in record:
        output["traversal_record"] = record["traversal_record"]

    # Byte-deterministic JSON serialization: 2-space indent, sorted keys=False
    return json.dumps(output, indent=2, ensure_ascii=False)
