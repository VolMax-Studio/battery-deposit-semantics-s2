"""
Frozen constants and definitions for S2 CVD qualification.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (Freeze commit: 97410ca512d0c87571b4f321712c4c7c564a6a82)
"""

from typing import Dict, List, Set

# §4.1 The eleven parameters in frozen order
PARAMETERS: List[str] = [
    "E1",
    "E2",
    "E3",
    "E4a",
    "E4b",
    "E5",
    "E6",
    "E7a",
    "E7b",
    "E8a",
    "E8b",
]

# §5.2 Item classes (0..5)
CLASSES: List[str] = [
    "POS-EXPLICIT",      # 0
    "POS-BURIED",        # 1
    "NEG-ABSENT",         # 2
    "NEG-ADJACENT",       # 3
    "AMBIG-CONSTRUCTED",  # 4
    "NA-CONSTRUCTED",     # 5
]

CLASS_TO_ID: Dict[str, int] = {c: idx for idx, c in enumerate(CLASSES)}
ID_TO_CLASS: Dict[int, str] = {idx: c for idx, c in enumerate(CLASSES)}

# Standalone determining classes (§5.2.2)
STANDALONE_DETERMINING_CLASSES: Set[str] = {"POS-EXPLICIT", "POS-BURIED"}
STANDALONE_DETERMINING_CLASS_IDS: Set[int] = {0, 1}

# §4.2 Scope vocabulary and semantics-first subsets
APPLICABLE_SCOPES: Dict[str, List[str]] = {
    "E1": ["current", "power"],
    "E2": ["current", "voltage", "power", "temperature"],
    "E3": ["capacity_charge", "capacity_discharge", "energy", "time"],
    "E4a": ["current", "voltage", "power", "temperature"],
    "E4b": ["current", "voltage", "power", "temperature"],
    "E5": ["current", "voltage", "power", "temperature"],
    "E6": ["current", "voltage", "power", "temperature"],
    "E7a": ["step_index", "cycle_index", "test_index"],
    "E7b": ["dataset"],
    "E8a": ["current", "voltage"],
    "E8b": [
        "current",
        "voltage",
        "power",
        "capacity_charge",
        "capacity_discharge",
        "energy",
        "temperature",
        "time",
    ],
}

# §5.2.1 Frozen coverage categories per parameter
COVERAGE_CATEGORIES: Dict[str, List[str]] = {
    "E1": ["charge_positive", "discharge_positive"],
    "E2": ["measured", "placeholder"],
    "E3": ["step", "cycle", "test", "never"],
    "E4a": ["start", "end", "midpoint"],
    "E4b": ["closed_closed", "open_open", "closed_open", "open_closed"],
    "E5": [
        "fixed",
        "event_driven(delta_voltage)",
        "event_driven(delta_current)",
        "event_driven(step_transition)",
    ],
    "E6": [
        "completeness_counter",
        "expected_count_comparison",
        "gap_flag_column",
        "acquisition_log_reconciliation",
    ],
    "E7a": [
        "explicit_index_column",
        "filename_encoding",
        "time_segmentation_rule",
        "row_grouping_marker",
    ],
    "E7b": [
        "step_type_column",
        "current_sign",
        "separate_state_column",
        "mode_code_enum",
    ],
    "E8a": ["A", "mA", "V", "mV"],
    "E8b": ["none", "factor", "affine"],
}

# E8a scope-partitioned categories (§4.1, §5.2.2)
E8A_SCOPE_CATEGORIES: Dict[str, List[str]] = {
    "current": ["A", "mA"],
    "voltage": ["V", "mV"],
}

# Strata (§2)
STRATA: List[str] = ["S-DOC", "S-FILE"]

# Counts
NUM_BUNDLES: int = 30
NUM_PARAMETERS: int = 11
NUM_CELLS: int = 330
NUM_CLASSES: int = 6
CELLS_PER_CLASS_PER_PARAM: int = 5
STANDALONE_CELLS_PER_PARAM: int = 10  # 5 POS-EXPLICIT + 5 POS-BURIED
