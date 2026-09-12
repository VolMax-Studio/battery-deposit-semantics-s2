"""
Bank Schemas for Semantic and Placement Metadata.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.3).
"""

from typing import Dict, Any, Optional, List
from .constants import (
    PARAMETERS,
    APPLICABLE_SCOPES,
    CLASSES,
    STRATA,
)

SET_VALUED_PARAMETERS = {"E5", "E6", "E7a", "E7b"}
SEMANTIC_ROLES = {"determining", "non_determining_adjacent", "non_applicable"}
PLACEMENTS = {"prominent", "buried", "absent"}


def validate_semantic_bank_metadata(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate semantic bank metadata (§5.3):
    - parameter: valid parameter ID
    - scope: valid applicable scope for that parameter
    - evidence_stratum: S-DOC | S-FILE
    - semantic_role: determining | non_determining_adjacent | non_applicable
    - semantic_value: REQUIRED iff semantic_role = determining, else MUST be null
    - exclusive_assertion: true | false; may be true only for determining entries
      of set-valued parameters; MUST be false otherwise
    - entry_text: must be non-empty string naming its scope's signal explicitly
    """
    param = entry.get("parameter")
    if param not in PARAMETERS:
        return {"valid": False, "error": f"Invalid parameter: {param}"}

    scope = entry.get("scope")
    if scope not in APPLICABLE_SCOPES[param]:
        return {"valid": False, "error": f"Invalid scope '{scope}' for parameter {param}"}

    stratum = entry.get("evidence_stratum")
    if stratum not in STRATA:
        return {"valid": False, "error": f"Invalid stratum: {stratum}. Must be S-DOC or S-FILE"}

    role = entry.get("semantic_role")
    if role not in SEMANTIC_ROLES:
        return {"valid": False, "error": f"Invalid semantic_role: {role}"}

    value = entry.get("semantic_value")
    if role == "determining":
        if value is None:
            return {"valid": False, "error": "semantic_value is REQUIRED when semantic_role = 'determining'"}
    else:
        if value is not None:
            return {"valid": False, "error": f"semantic_value MUST be null when semantic_role = '{role}'"}

    exclusive = entry.get("exclusive_assertion", False)
    if not isinstance(exclusive, bool):
        return {"valid": False, "error": "exclusive_assertion must be a boolean"}
    if exclusive:
        if role != "determining" or param not in SET_VALUED_PARAMETERS:
            return {
                "valid": False,
                "error": f"exclusive_assertion may be true ONLY for determining entries of set-valued parameters ({SET_VALUED_PARAMETERS})",
            }

    text = entry.get("entry_text")
    if not isinstance(text, str) or len(text.strip()) == 0:
        return {"valid": False, "error": "entry_text must be a non-empty string"}

    return {"valid": True, "error": None}


def validate_placement_metadata(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate corpus placement metadata (§5.3):
    - class: valid class name
    - placement: prominent | buried | absent
    - bundle_idx: integer in [0, 29]
    - param_idx: integer in [0, 10]
    """
    cls = entry.get("class")
    if cls not in CLASSES:
        return {"valid": False, "error": f"Invalid class: {cls}"}

    placement = entry.get("placement")
    if placement not in PLACEMENTS:
        return {"valid": False, "error": f"Invalid placement: {placement}"}

    bundle_idx = entry.get("bundle_idx")
    if not isinstance(bundle_idx, int) or not (0 <= bundle_idx < 30):
        return {"valid": False, "error": f"bundle_idx must be int in 0..29, got {bundle_idx}"}

    param_idx = entry.get("param_idx")
    if not isinstance(param_idx, int) or not (0 <= param_idx < 11):
        return {"valid": False, "error": f"param_idx must be int in 0..10, got {param_idx}"}

    return {"valid": True, "error": None}
