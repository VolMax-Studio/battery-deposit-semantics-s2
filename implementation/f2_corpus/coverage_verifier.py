"""
Coverage Verifier: Rigorous verification of all §5.1 assertions and §5.2 requirements.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md.
"""

from typing import Dict, List, Tuple
from .constants import (
    PARAMETERS,
    APPLICABLE_SCOPES,
    COVERAGE_CATEGORIES,
    E8A_SCOPE_CATEGORIES,
    NUM_BUNDLES,
    NUM_PARAMETERS,
    STANDALONE_DETERMINING_CLASS_IDS,
)
from .class_assignment import get_class_id, verify_class_constraints


def verify_all_assertions(scope_table: Dict[str, Dict]) -> Dict[str, bool]:
    """
    Formally verify all §5.1 frozen assertions against the generated scope table.
    """
    # 1. Class constraints
    cls_res = verify_class_constraints()
    if not cls_res["valid"]:
        return cls_res

    # 2. Scope constraints per parameter
    for j, param in enumerate(PARAMETERS):
        if param not in scope_table:
            return {"valid": False, "reason": f"Missing parameter {param} in scope table"}
        
        scopes = scope_table[param]["scopes"]
        if len(scopes) != NUM_BUNDLES:
            return {"valid": False, "reason": f"{param}: expected {NUM_BUNDLES} scopes, got {len(scopes)}"}
            
        applicable = APPLICABLE_SCOPES[param]
        s = len(applicable)
        
        # Check that every scope belongs to applicable set
        for i, sc in enumerate(scopes):
            if sc not in applicable:
                return {"valid": False, "reason": f"{param} bundle {i}: scope {sc} not in applicable {applicable}"}

        # Check: scope counts differ by at most 1
        counts = [scopes.count(sc) for sc in applicable]
        if max(counts) - min(counts) > 1:
            return {"valid": False, "reason": f"{param}: scope counts diff > 1: {dict(zip(applicable, counts))}"}

        # Check: class x scope table: max cell - min cell <= 1
        cls_scope_counts = {c: {sc: 0 for sc in applicable} for c in range(6)}
        for i in range(NUM_BUNDLES):
            cls_id = get_class_id(i, j)
            cls_scope_counts[cls_id][scopes[i]] += 1
            
        # Over the whole parameter table, max cell - min cell <= 1
        all_cells = [cls_scope_counts[c][sc] for c in range(6) for sc in applicable]
        if max(all_cells) - min(all_cells) > 1:
            return {"valid": False, "reason": f"{param}: class x scope table max-min > 1: max={max(all_cells)}, min={min(all_cells)}"}

        if s > 1:
            # Check: no scope occurs with fewer than 2 distinct classes
            for sc in applicable:
                classes_with_sc = [c for c in range(6) if cls_scope_counts[c][sc] > 0]
                if len(classes_with_sc) < 2:
                    return {"valid": False, "reason": f"{param}: scope {sc} appears in only {len(classes_with_sc)} classes"}
                    
            # Check: no class occurs with fewer than 2 distinct scopes
            for c in range(6):
                scopes_in_c = [sc for sc in applicable if cls_scope_counts[c][sc] > 0]
                if len(scopes_in_c) < 2:
                    return {"valid": False, "reason": f"{param}: class {c} contains only {len(scopes_in_c)} scopes"}

        # Check: SCOPE-2 verification (§3.2):
        # For every (parameter, scope), CVD answer space admits >= 2 legal semantic values
        if param == "E8a":
            for sc in applicable:
                if len(E8A_SCOPE_CATEGORIES[sc]) < 2:
                    return {"valid": False, "reason": f"SCOPE-2 failed for {param} scope {sc}"}
        else:
            cats = COVERAGE_CATEGORIES[param]
            if len(cats) < 2:
                return {"valid": False, "reason": f"SCOPE-2 failed for {param}: categories {cats} < 2"}

    # 3. E8a COVERAGE FEASIBILITY and Standalone Unit Constraints (§5.1, §5.2.2)
    e8a_scopes = scope_table["E8a"]["scopes"]
    e8a_units = scope_table["E8a"]["standalone_units"]
    
    e8a_param_idx = PARAMETERS.index("E8a")
    standalone_cells = [i for i in range(NUM_BUNDLES) if get_class_id(i, e8a_param_idx) in STANDALONE_DETERMINING_CLASS_IDS]
    
    standalone_curr = [i for i in standalone_cells if e8a_scopes[i] == "current"]
    standalone_volt = [i for i in standalone_cells if e8a_scopes[i] == "voltage"]
    
    if len(standalone_curr) < 4:
        return {"valid": False, "reason": f"E8a count(scope=current) standalone {len(standalone_curr)} < 4"}
    if len(standalone_volt) < 4:
        return {"valid": False, "reason": f"E8a count(scope=voltage) standalone {len(standalone_volt)} < 4"}

    curr_units = [e8a_units.get(str(i)) for i in standalone_curr]
    volt_units = [e8a_units.get(str(i)) for i in standalone_volt]

    if curr_units.count("A") < 2 or curr_units.count("mA") < 2:
        return {"valid": False, "reason": f"E8a current units failed: A={curr_units.count('A')}, mA={curr_units.count('mA')}"}
    if volt_units.count("V") < 2 or volt_units.count("mV") < 2:
        return {"valid": False, "reason": f"E8a voltage units failed: V={volt_units.count('V')}, mV={volt_units.count('mV')}"}

    return {"valid": True, "reason": "All §5.1 assertions and coverage contracts strictly verified"}
