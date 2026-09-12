"""
Deterministic class-assignment implementation from §5.1.
class(i, j) = (i + j) mod 6     i = 0..29, j = 0..10   (closed form, frozen)
"""

from typing import List, Dict
from .constants import (
    PARAMETERS,
    CLASSES,
    CLASS_TO_ID,
    ID_TO_CLASS,
    NUM_BUNDLES,
    NUM_PARAMETERS,
)


def get_class_id(bundle_idx: int, param_idx: int) -> int:
    """Compute class ID for bundle i and parameter j using closed form."""
    if not (0 <= bundle_idx < NUM_BUNDLES):
        raise ValueError(f"bundle_idx must be in [0, {NUM_BUNDLES - 1}], got {bundle_idx}")
    if not (0 <= param_idx < NUM_PARAMETERS):
        raise ValueError(f"param_idx must be in [0, {NUM_PARAMETERS - 1}], got {param_idx}")
    return (bundle_idx + param_idx) % 6


def get_class_name(bundle_idx: int, param_idx: int) -> str:
    """Compute class name for bundle i and parameter j."""
    return ID_TO_CLASS[get_class_id(bundle_idx, param_idx)]


def get_class_matrix() -> List[List[int]]:
    """Return 30x11 matrix of class IDs."""
    return [
        [get_class_id(i, j) for j in range(NUM_PARAMETERS)]
        for i in range(NUM_BUNDLES)
    ]


def verify_class_constraints() -> Dict[str, bool]:
    """
    Verify §5.1 frozen assertions for the class assignment:
    1. For every parameter: class counts == [5, 5, 5, 5, 5, 5] (exact).
    2. For every bundle: max class count <= 3.
    3. For every (parameter, fold): class counts == [1, 1, 1, 1, 1, 1] (fold = i mod 5).
    """
    matrix = get_class_matrix()
    
    # 1. Per parameter exact 5 in each class
    for j in range(NUM_PARAMETERS):
        counts = [0] * 6
        for i in range(NUM_BUNDLES):
            counts[matrix[i][j]] += 1
        if counts != [5, 5, 5, 5, 5, 5]:
            return {"valid": False, "reason": f"Param {j} ({PARAMETERS[j]}) class counts {counts} != [5,5,5,5,5,5]"}
            
    # 2. Per bundle max class count <= 3
    for i in range(NUM_BUNDLES):
        counts = [0] * 6
        for j in range(NUM_PARAMETERS):
            counts[matrix[i][j]] += 1
        if max(counts) > 3:
            return {"valid": False, "reason": f"Bundle {i} max class count {max(counts)} > 3"}
            
    # 3. Per (parameter, fold) where fold = i mod 5
    # Since 30 bundles divided into 5 folds of 6 bundles each:
    # fold f contains bundles i where i % 5 == f: i = f, f+5, f+10, f+15, f+20, f+25.
    # For a fixed parameter j:
    # class(f + 5k, j) = (f + 5k + j) mod 6 = (f + j - k) mod 6.
    # As k ranges 0..5, (f + j - k) mod 6 takes each value in {0..5} exactly once!
    for j in range(NUM_PARAMETERS):
        for fold in range(5):
            fold_bundles = [f for f in range(NUM_BUNDLES) if f % 5 == fold]
            counts = [0] * 6
            for i in fold_bundles:
                counts[matrix[i][j]] += 1
            if counts != [1, 1, 1, 1, 1, 1]:
                return {"valid": False, "reason": f"Param {j} fold {fold} class counts {counts} != [1,1,1,1,1,1]"}
                
    return {"valid": True, "reason": "All §5.1 class constraints strictly verified"}
