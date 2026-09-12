"""
E8a Joint Scope and Unit Assignment Solver.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.1, §5.2.2, §5.2.5).

E8a (parameter index 9, or E8a):
30 bundles, class(i, 9) = (i + 9) mod 6.
Applicable scopes: current, voltage.
Categories for current: A, mA.
Categories for voltage: V, mV.
Standalone determining classes: POS-EXPLICIT (0) and POS-BURIED (1).

Admissible standalone determining allocations:
- 4 current / 6 voltage (zero-slack for current: 2 A + 2 mA)
- 5 current / 5 voltage
- 6 current / 4 voltage (zero-slack for voltage: 2 V + 2 mV)

This module constructively solves the joint constraint problem and provides
explicit witnesses for all three cases.
"""

from typing import Dict, List, Tuple, Optional
from .constants import (
    NUM_BUNDLES,
    CLASS_TO_ID,
    STANDALONE_DETERMINING_CLASS_IDS,
)
from .class_assignment import get_class_id


class E8aWitness:
    def __init__(
        self,
        case_name: str,
        scope_assignment: List[str],  # length 30: 'current' or 'voltage'
        unit_assignment: Dict[int, str],  # bundle_idx -> unit ('A', 'mA', 'V', 'mV') for standalone cells
    ):
        self.case_name = case_name
        self.scope_assignment = scope_assignment
        self.unit_assignment = unit_assignment

    def to_dict(self) -> Dict:
        standalone_details = []
        for i in range(NUM_BUNDLES):
            cls_id = get_class_id(i, 9)
            if cls_id in STANDALONE_DETERMINING_CLASS_IDS:
                standalone_details.append({
                    "bundle_idx": i,
                    "class_id": cls_id,
                    "class_name": "POS-EXPLICIT" if cls_id == 0 else "POS-BURIED",
                    "scope": self.scope_assignment[i],
                    "assigned_unit": self.unit_assignment.get(i),
                })
        return {
            "case": self.case_name,
            "scope_counts": {
                "current": self.scope_assignment.count("current"),
                "voltage": self.scope_assignment.count("voltage"),
            },
            "standalone_details": standalone_details,
        }


def solve_e8a_joint(
    target_standalone_split: Tuple[int, int] = (5, 5),
    seed: int = 20260912,
) -> E8aWitness:
    """
    Constructively solve the joint scope and unit assignment for E8a.
    target_standalone_split must be one of (4, 6), (5, 5), or (6, 4).
    
    Constraints enforced:
    1. Overall scope counts: exactly 15 current, 15 voltage.
    2. Class x Scope table: row sums 5, cells in {2, 3}.
       Exactly three classes have 3 current, three classes have 2 current.
    3. Standalone classes (0: POS-EXPLICIT, 1: POS-BURIED):
       Sum of current across classes 0 and 1 equals target_standalone_split[0].
    4. Unit assignment for standalone determining cells:
       - If scope == 'current': unit in {'A', 'mA'}.
         Count of 'A' >= 2, Count of 'mA' >= 2.
       - If scope == 'voltage': unit in {'V', 'mV'}.
         Count of 'V' >= 2, Count of 'mV' >= 2.
    """
    curr_standalone, volt_standalone = target_standalone_split
    if (curr_standalone, volt_standalone) not in [(4, 6), (5, 5), (6, 4)]:
        raise ValueError(f"Invalid target standalone split: {target_standalone_split}. Must be (4, 6), (5, 5), or (6, 4).")

    # Determine class-level current counts for each of the 6 classes.
    # Each class gets 2 or 3 current. Exactly 3 classes get 3 current.
    # Classes 0 and 1 are standalone.
    # If target is (4, 6): class 0 gets 2, class 1 gets 2.
    #   Remaining 4 classes (2, 3, 4, 5) must contain three 3s and one 2 (sum = 2+2+3+3+3+2 = 15).
    # If target is (5, 5): class 0 gets 3, class 1 gets 2 (or vice versa).
    #   Remaining 4 classes must contain two 3s and two 2s (sum = 3+2+3+3+2+2 = 15).
    # If target is (6, 4): class 0 gets 3, class 1 gets 3.
    #   Remaining 4 classes must contain one 3 and three 2s (sum = 3+3+3+2+2+2 = 15).

    class_curr_counts = [0] * 6
    if (curr_standalone, volt_standalone) == (4, 6):
        class_curr_counts[0] = 2
        class_curr_counts[1] = 2
        class_curr_counts[2] = 3
        class_curr_counts[3] = 3
        class_curr_counts[4] = 3
        class_curr_counts[5] = 2
    elif (curr_standalone, volt_standalone) == (5, 5):
        class_curr_counts[0] = 3
        class_curr_counts[1] = 2
        class_curr_counts[2] = 3
        class_curr_counts[3] = 3
        class_curr_counts[4] = 2
        class_curr_counts[5] = 2
    else:  # (6, 4)
        class_curr_counts[0] = 3
        class_curr_counts[1] = 3
        class_curr_counts[2] = 3
        class_curr_counts[3] = 2
        class_curr_counts[4] = 2
        class_curr_counts[5] = 2

    # Group bundle indices by class id for parameter 9 (E8a)
    bundles_by_class: Dict[int, List[int]] = {c: [] for c in range(6)}
    for i in range(NUM_BUNDLES):
        cls_id = get_class_id(i, 9)
        bundles_by_class[cls_id].append(i)

    # For each class, pick class_curr_counts[c] bundles to be 'current', others 'voltage'
    # Deterministic choice based on bundle index order
    scope_assignment = [""] * NUM_BUNDLES
    for c in range(6):
        k = class_curr_counts[c]
        b_list = bundles_by_class[c]  # exactly 5 bundles
        # Assign first k to 'current', rest to 'voltage'
        for idx in range(k):
            scope_assignment[b_list[idx]] = "current"
        for idx in range(k, 5):
            scope_assignment[b_list[idx]] = "voltage"

    # Now solve unit assignment for standalone determining cells
    # Standalone cells are in bundles_by_class[0] and bundles_by_class[1]
    standalone_bundles = bundles_by_class[0] + bundles_by_class[1]
    
    current_standalone_bundles = [b for b in standalone_bundles if scope_assignment[b] == "current"]
    voltage_standalone_bundles = [b for b in standalone_bundles if scope_assignment[b] == "voltage"]

    assert len(current_standalone_bundles) == curr_standalone
    assert len(voltage_standalone_bundles) == volt_standalone

    unit_assignment: Dict[int, str] = {}

    # Assign current standalone units: A and mA (each >= 2)
    # If len == 4 (zero slack): exactly 2 'A', 2 'mA'
    # If len == 5: 3 'A', 2 'mA' (or 2 'A', 3 'mA')
    # If len == 6: 3 'A', 3 'mA'
    half_curr = len(current_standalone_bundles) // 2
    for idx, b in enumerate(current_standalone_bundles):
        if idx < half_curr:
            unit_assignment[b] = "A"
        else:
            unit_assignment[b] = "mA"

    # Assign voltage standalone units: V and mV (each >= 2)
    # If len == 4 (zero slack): exactly 2 'V', 2 'mV'
    # If len == 5: 3 'V', 2 'mV'
    # If len == 6: 3 'V', 3 'mV'
    half_volt = len(voltage_standalone_bundles) // 2
    for idx, b in enumerate(voltage_standalone_bundles):
        if idx < half_volt:
            unit_assignment[b] = "V"
        else:
            unit_assignment[b] = "mV"

    case_name = f"split_{curr_standalone}_{volt_standalone}"
    witness = E8aWitness(case_name, scope_assignment, unit_assignment)
    return witness


def verify_e8a_witness(witness: E8aWitness) -> Dict[str, bool]:
    """
    Formally verify all §5.1 and §5.2.2 requirements on an E8a witness:
    - 30 cells total.
    - Scope counts: exactly 15 current, 15 voltage.
    - Class x Scope table: row sums 5, max cell - min cell <= 1.
    - Every scope sees all 6 classes (each class has at least 2 current and at least 2 voltage).
    - Every class sees both scopes.
    - Standalone determining cells (classes 0 and 1):
      - count(current) >= 4
      - count(voltage) >= 4
      - within current: count(A) >= 2, count(mA) >= 2
      - within voltage: count(V) >= 2, count(mV) >= 2
    """
    scopes = witness.scope_assignment
    if len(scopes) != NUM_BUNDLES:
        return {"valid": False, "reason": f"Expected {NUM_BUNDLES} cells, got {len(scopes)}"}
        
    n_curr = scopes.count("current")
    n_volt = scopes.count("voltage")
    if n_curr != 15 or n_volt != 15:
        return {"valid": False, "reason": f"Marginals not 15/15: got current={n_curr}, voltage={n_volt}"}

    # Class x Scope
    cls_scope_counts = {c: {"current": 0, "voltage": 0} for c in range(6)}
    for i in range(NUM_BUNDLES):
        cls_id = get_class_id(i, 9)
        s = scopes[i]
        cls_scope_counts[cls_id][s] += 1

    for c in range(6):
        row = cls_scope_counts[c]
        if row["current"] + row["voltage"] != 5:
            return {"valid": False, "reason": f"Class {c} row sum {row['current'] + row['voltage']} != 5"}
        if abs(row["current"] - row["voltage"]) > 1:
            return {"valid": False, "reason": f"Class {c} max-min > 1: {row}"}
        if row["current"] < 1 or row["voltage"] < 1:
            return {"valid": False, "reason": f"Class {c} does not span both scopes: {row}"}

    # Standalone cells (classes 0 and 1)
    standalone_cells = [i for i in range(NUM_BUNDLES) if get_class_id(i, 9) in STANDALONE_DETERMINING_CLASS_IDS]
    if len(standalone_cells) != 10:
        return {"valid": False, "reason": f"Expected 10 standalone cells, got {len(standalone_cells)}"}

    standalone_curr = [i for i in standalone_cells if scopes[i] == "current"]
    standalone_volt = [i for i in standalone_cells if scopes[i] == "voltage"]

    if len(standalone_curr) < 4:
        return {"valid": False, "reason": f"count(current) standalone {len(standalone_curr)} < 4"}
    if len(standalone_volt) < 4:
        return {"valid": False, "reason": f"count(voltage) standalone {len(standalone_volt)} < 4"}

    units = witness.unit_assignment
    curr_units = [units.get(i) for i in standalone_curr]
    volt_units = [units.get(i) for i in standalone_volt]

    count_A = curr_units.count("A")
    count_mA = curr_units.count("mA")
    count_V = volt_units.count("V")
    count_mV = volt_units.count("mV")

    if count_A < 2:
        return {"valid": False, "reason": f"count(A) {count_A} < 2"}
    if count_mA < 2:
        return {"valid": False, "reason": f"count(mA) {count_mA} < 2"}
    if count_V < 2:
        return {"valid": False, "reason": f"count(V) {count_V} < 2"}
    if count_mV < 2:
        return {"valid": False, "reason": f"count(mV) {count_mV} < 2"}

    return {"valid": True, "reason": "All E8a joint constraints strictly satisfied"}
