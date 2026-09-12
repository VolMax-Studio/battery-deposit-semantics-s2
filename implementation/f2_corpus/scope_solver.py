"""
Deterministic Scope-Assignment Constraint Solver for all 11 parameters.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.1, §5.2).

Satisfies all frozen §5.1 constraints:
1. for every parameter: class counts == [5,5,5,5,5,5] (exact)
2. for every parameter: scope counts differ by at most 1
3. for every parameter: class x scope table: max cell - min cell <= 1
4. for every parameter with s > 1: no scope occurs with fewer than 2 distinct classes
5. for every parameter with s > 1: no class occurs with fewer than 2 distinct scopes
6. for every bundle: max class count <= 3
7. for every (parameter, fold): class counts == [1,1,1,1,1,1]
8. for every (bundle, parameter): exactly one scope from applicable set
9. for every (parameter, scope): admits >= 2 legal semantic values (SCOPE-2)
10. COVERAGE FEASIBILITY (E8a):
    standalone determining cells: current >= 4, voltage >= 4, A >= 2, mA >= 2, V >= 2, mV >= 2.
"""

import json
from typing import Dict, List, Tuple
from .constants import (
    PARAMETERS,
    APPLICABLE_SCOPES,
    COVERAGE_CATEGORIES,
    NUM_BUNDLES,
    NUM_PARAMETERS,
    STANDALONE_DETERMINING_CLASS_IDS,
)
from .class_assignment import get_class_id
from .e8a_joint_solver import solve_e8a_joint, E8aWitness


def solve_parameter_scopes(param: str) -> List[str]:
    """
    Solve scope assignment for a single parameter across 30 bundles.
    """
    param_idx = PARAMETERS.index(param)
    scopes = APPLICABLE_SCOPES[param]
    s = len(scopes)
    
    # E7b is scope-free (s = 1: dataset)
    if s == 1:
        return [scopes[0]] * NUM_BUNDLES

    # E8a is solved jointly via e8a_joint_solver (default split 5/5)
    if param == "E8a":
        witness = solve_e8a_joint(target_standalone_split=(5, 5))
        return witness.scope_assignment

    # For other parameters, we distribute bundles to scopes to guarantee:
    # 1. Total scope counts differ by at most 1.
    # 2. In each class (5 bundles), scopes are distributed evenly (cells differ by at most 1).
    # Group bundle indices by class id
    bundles_by_class: Dict[int, List[int]] = {c: [] for c in range(6)}
    for i in range(NUM_BUNDLES):
        cls_id = get_class_id(i, param_idx)
        bundles_by_class[cls_id].append(i)

    # Class x Scope assignment matrix: class_id -> list of scopes for its 5 bundles
    # We rotate the scope offset across classes to balance the column totals.
    scope_assignment = [""] * NUM_BUNDLES
    
    # We assign scopes cyclically within each class, starting at an offset that shifts with class c
    # For s=2 (E1): c=0..5, class c gets 2 or 3 of scope 0.
    # For s=3 (E7a): class c gets 2, 2, 1 or 2, 1, 2 etc.
    # For s=4 (E2, E3, E4a, E4b, E5, E6): class c gets 2, 1, 1, 1 (one scope gets 2, three get 1).
    # For s=8 (E8b): class c gets five 1s and three 0s.
    
    scope_offset = 0
    for c in range(6):
        b_list = bundles_by_class[c]  # 5 bundles
        for idx in range(5):
            assigned_scope = scopes[(scope_offset + idx) % s]
            scope_assignment[b_list[idx]] = assigned_scope
        # Shift offset for next class
        # For s=2: shift by 1 (alternates which scope gets 3)
        # For s=3: shift by 2
        # For s=4: shift by 1 (5 mod 4 = 1)
        # For s=8: shift by 5 (5 mod 8 = 5)
        scope_offset = (scope_offset + 5) % s

    return scope_assignment


def generate_frozen_scope_table() -> Dict[str, Dict]:
    """
    Generate and return complete frozen scope table for all 11 parameters across 30 bundles,
    including E8a standalone unit assignments.
    """
    table: Dict[str, Dict] = {}
    
    # Solve E8a with explicit witness
    e8a_witness = solve_e8a_joint(target_standalone_split=(5, 5))
    
    for param in PARAMETERS:
        if param == "E8a":
            scopes = e8a_witness.scope_assignment
            units = e8a_witness.unit_assignment
        else:
            scopes = solve_parameter_scopes(param)
            units = {}
            
        table[param] = {
            "scopes": scopes,
            "standalone_units": {str(k): v for k, v in units.items()},
        }
        
    return table
