"""
Structural Validators for S2 CVD Construction.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§4.3, §5.7).
"""

from typing import Dict, Any, List, Set
from .constants import PARAMETERS

SET_VALUED_PARAMETERS = {"E5", "E6", "E7a", "E7b"}
SINGLE_VALUED_PARAMETERS = set(PARAMETERS) - SET_VALUED_PARAMETERS


def check_incompatibility(
    param: str,
    scope: str,
    entry_1: Dict[str, Any],
    entry_2: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Verify §5.7 frozen incompatibility relation between two determining entries
    for an AMBIG-CONSTRUCTED parameter-cell:
    - Single-valued parameters: two distinct canonical semantic values legal for the same scope.
    - Set-valued parameters: BOTH entries must have exclusive_assertion = True,
      and their value sets must differ.
    """
    if entry_1.get("semantic_role") != "determining" or entry_2.get("semantic_role") != "determining":
        return {"incompatible": False, "reason": "Both entries must have semantic_role = 'determining'"}

    if entry_1.get("scope") != scope or entry_2.get("scope") != scope:
        return {"incompatible": False, "reason": "Both entries must match the parameter-cell's scope"}

    val1 = entry_1.get("semantic_value")
    val2 = entry_2.get("semantic_value")

    if param in SINGLE_VALUED_PARAMETERS:
        if val1 == val2:
            return {"incompatible": False, "reason": f"Single-valued {param}: values are identical ({val1})"}
        return {"incompatible": True, "reason": f"Single-valued {param}: distinct canonical values for same scope"}

    elif param in SET_VALUED_PARAMETERS:
        excl1 = entry_1.get("exclusive_assertion", False)
        excl2 = entry_2.get("exclusive_assertion", False)
        if not (excl1 and excl2):
            return {
                "incompatible": False,
                "reason": f"Set-valued {param}: incompatibility requires BOTH entries to carry exclusive_assertion=True",
            }
        
        # Values are sets
        set1 = set(val1) if isinstance(val1, list) else {val1}
        set2 = set(val2) if isinstance(val2, list) else {val2}
        if set1 == set2:
            return {"incompatible": False, "reason": f"Set-valued {param}: value sets are identical ({set1})"}
        return {"incompatible": True, "reason": f"Set-valued {param}: both exclusive and value sets differ"}

    return {"incompatible": False, "reason": f"Unknown parameter {param}"}


def validate_e3_structure(bundle_manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate §4.3 E3 structural requirements for bundles declaring E3:
    1. at least one cycle contains >= 2 steps (separates step from cycle)
    2. at least one test contains >= 2 cycles (separates cycle from test)
    3. the data contains >= 2 tests (separates test from never)
    """
    structure = bundle_manifest.get("e3_structure")
    if not structure:
        return {"valid": False, "reason": "Missing 'e3_structure' in bundle manifest"}

    num_tests = structure.get("num_tests", 0)
    if num_tests < 2:
        return {"valid": False, "reason": f"E3 structure: data contains {num_tests} tests (< 2)"}

    cycles_per_test = structure.get("cycles_per_test", [])
    if not any(c >= 2 for c in cycles_per_test):
        return {"valid": False, "reason": f"E3 structure: no test contains >= 2 cycles ({cycles_per_test})"}

    steps_per_cycle = structure.get("steps_per_cycle", [])
    if not any(s >= 2 for s in steps_per_cycle):
        return {"valid": False, "reason": f"E3 structure: no cycle contains >= 2 steps ({steps_per_cycle})"}

    return {"valid": True, "reason": "E3 hierarchical structure strictly validated"}


def validate_e4_positive_duration(bundle_manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate §4.3 E4a/E4b requirements:
    Every bundle carrying an E4a or E4b parameter-cell must declare records
    aggregating over an interval of strictly positive duration (duration > 0).
    """
    interval_duration = bundle_manifest.get("interval_duration_seconds")
    if interval_duration is None:
        return {"valid": False, "reason": "Missing 'interval_duration_seconds' in bundle manifest"}

    if interval_duration <= 0:
        return {
            "valid": False,
            "reason": f"E4 structure: interval duration must be strictly positive (> 0), got {interval_duration}",
        }

    return {"valid": True, "reason": "E4 positive interval duration strictly validated"}
