"""
Adjudication Output Schema and Validation.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§6.1, §6.4).
"""

from typing import Dict, Any, List
from f2_corpus.constants import PARAMETERS, APPLICABLE_SCOPES, STRATA

VERDICT_CLASSES = {"EXPLICIT_DOC", "EXPLICIT_FILE", "AMBIGUOUS", "ABSENT", "NOT_APPLICABLE"}

ADJUDICATION_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["parameter_id", "scope", "verdict_class", "readings"],
    "properties": {
        "parameter_id": {"type": "string", "enum": PARAMETERS},
        "scope": {"type": "string"},
        "verdict_class": {"type": "string", "enum": list(VERDICT_CLASSES)},
        "readings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "semantic_value",
                    "evidence_stratum",
                    "artifact_sha256",
                    "locator",
                    "verbatim_excerpt",
                ],
                "properties": {
                    "semantic_value": {},
                    "evidence_stratum": {"type": "string", "enum": STRATA},
                    "artifact_sha256": {"type": "string", "minLength": 64, "maxLength": 64},
                    "locator": {"type": "string"},
                    "verbatim_excerpt": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
        "traversal_record": {
            "type": "object",
        },
    },
    "additionalProperties": False,  # Prohibits note_text, timestamps, etc.
}


def validate_adjudication_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate adjudication record according to §6.1:
    - No note_text allowed.
    - Parameter ID and scope must be valid.
    - Verdict class matches reading counts:
      - EXPLICIT_DOC: exactly 1 reading, S-DOC
      - EXPLICIT_FILE: exactly 1 reading, S-FILE
      - AMBIGUOUS: >= 2 readings
      - ABSENT: 0 readings, traversal_record required
      - NOT_APPLICABLE: 0 readings, traversal_record required
    """
    if "note_text" in record:
        return {"valid": False, "error": "note_text is prohibited (§6.1)"}

    param = record.get("parameter_id")
    if param not in PARAMETERS:
        return {"valid": False, "error": f"Invalid parameter_id: {param}"}

    scope = record.get("scope")
    if scope not in APPLICABLE_SCOPES.get(param, []):
        return {"valid": False, "error": f"Invalid scope '{scope}' for parameter {param}"}

    vc = record.get("verdict_class")
    if vc not in VERDICT_CLASSES:
        return {"valid": False, "error": f"Invalid verdict_class: {vc}"}

    readings = record.get("readings", [])
    if not isinstance(readings, list):
        return {"valid": False, "error": "readings must be a list"}

    if vc == "EXPLICIT_DOC":
        if len(readings) != 1:
            return {"valid": False, "error": f"EXPLICIT_DOC requires exactly 1 reading, got {len(readings)}"}
        if readings[0].get("evidence_stratum") != "S-DOC":
            return {"valid": False, "error": "EXPLICIT_DOC reading must have evidence_stratum = 'S-DOC'"}

    elif vc == "EXPLICIT_FILE":
        if len(readings) != 1:
            return {"valid": False, "error": f"EXPLICIT_FILE requires exactly 1 reading, got {len(readings)}"}
        if readings[0].get("evidence_stratum") != "S-FILE":
            return {"valid": False, "error": "EXPLICIT_FILE reading must have evidence_stratum = 'S-FILE'"}

    elif vc == "AMBIGUOUS":
        if len(readings) < 2:
            return {"valid": False, "error": f"AMBIGUOUS requires >= 2 readings, got {len(readings)}"}

    elif vc in ("ABSENT", "NOT_APPLICABLE"):
        if len(readings) != 0:
            return {"valid": False, "error": f"{vc} requires exactly 0 readings, got {len(readings)}"}
        if "traversal_record" not in record:
            return {"valid": False, "error": f"{vc} requires 'traversal_record' (§6.4)"}

    return {"valid": True, "error": None}
