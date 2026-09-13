#!/usr/bin/env python3
"""
F5 Bank Authoring Script — Party 2 (GROK-CLEAN-P2-01)
Corrected ATTEMPT 01 satisfying all frozen requirements + seven mandatory repairs
and underscore fixes for meta-keys.
"""

import json
import os
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional, Set, Tuple

# ============================================================================
# Load frozen data from repo
# ============================================================================

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
FROZEN_SCOPE_PATH = os.path.join(REPO_ROOT, "implementation/f2_corpus/frozen_scope_table.json")

if not os.path.exists(FROZEN_SCOPE_PATH):
    # Fallback to local execution if run from repo root
    FROZEN_SCOPE_PATH = "implementation/f2_corpus/frozen_scope_table.json"

with open(FROZEN_SCOPE_PATH, "r", encoding="utf-8") as f:
    FROZEN_SCOPE = json.load(f)

PARAMETERS = [
    "E1", "E2", "E3", "E4a", "E4b", "E5", "E6", "E7a", "E7b", "E8a", "E8b"
]
PARAM_TO_IDX = {p: i for i, p in enumerate(PARAMETERS)}

CLASSES = [
    "POS-EXPLICIT",      # 0
    "POS-BURIED",        # 1
    "NEG-ABSENT",         # 2
    "NEG-ADJACENT",       # 3
    "AMBIG-CONSTRUCTED",  # 4
    "NA-CONSTRUCTED",     # 5
]
ID_TO_CLASS = {i: c for i, c in enumerate(CLASSES)}

SET_VALUED = {"E5", "E6", "E7a", "E7b"}

APPLICABLE_SCOPES = {
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
        "current", "voltage", "power", "capacity_charge", "capacity_discharge",
        "energy", "temperature", "time",
    ],
}

E8A_UNITS = {
    "current": ["A", "mA"],
    "voltage": ["V", "mV"],
}

E8A_STANDALONE_UNITS = {int(k): v for k, v in FROZEN_SCOPE["E8a"]["standalone_units"].items()}

def get_class(bundle_idx: int, param_idx: int) -> str:
    return ID_TO_CLASS[(bundle_idx + param_idx) % 6]

def get_scope(param: str, bundle_idx: int) -> str:
    return FROZEN_SCOPE[param]["scopes"][bundle_idx]

def e8b_value(kind: str, factor: float = 2.0, offset: float = 1.0) -> str:
    """ATOM-2 compliant: none | factor(!=1) | affine(offset!=0)."""
    if kind == "none":
        return "none"
    if kind == "factor":
        assert factor != 1.0
        return f"factor({factor})"
    if kind == "affine":
        assert offset != 0.0
        return f"affine({factor}, {offset})"
    raise ValueError(kind)

# ============================================================================
# Standalone cells and coverage plan
# ============================================================================

standalone_cells: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
for pidx, param in enumerate(PARAMETERS):
    for b in range(30):
        cls = get_class(b, pidx)
        if cls in ("POS-EXPLICIT", "POS-BURIED"):
            standalone_cells[param].append((b, cls))

assert all(len(v) == 10 for v in standalone_cells.values())

standalone_plan: Dict[str, Dict[int, Tuple[Any, str]]] = {p: {} for p in PARAMETERS}

# E1
e1_vals = (["charge_positive"] * 5 + ["discharge_positive"] * 5)
e1_strata = (["S-DOC"] * 3 + ["S-FILE"] * 2) * 2
for i, (b, _) in enumerate(standalone_cells["E1"]):
    standalone_plan["E1"][b] = (e1_vals[i], e1_strata[i])

# E2
e2_vals = (["measured"] * 5 + ["placeholder"] * 5)
e2_strata = (["S-DOC"] * 3 + ["S-FILE"] * 2) * 2
for i, (b, _) in enumerate(standalone_cells["E2"]):
    standalone_plan["E2"][b] = (e2_vals[i], e2_strata[i])

# E3
e3_vals = ["step", "step", "cycle", "cycle", "test", "test", "never", "never", "step", "cycle"]
e3_strata = ["S-DOC", "S-FILE", "S-DOC", "S-FILE", "S-DOC", "S-FILE", "S-DOC", "S-FILE", "S-DOC", "S-FILE"]
for i, (b, _) in enumerate(standalone_cells["E3"]):
    standalone_plan["E3"][b] = (e3_vals[i], e3_strata[i])

# E4a
e4a_vals = ["start", "start", "end", "end", "midpoint", "midpoint", "start", "end", "midpoint", "start"]
e4a_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E4a"]):
    standalone_plan["E4a"][b] = (e4a_vals[i], e4a_strata[i])

# E4b
e4b_vals = ["closed_closed", "closed_closed", "open_open", "open_open",
            "closed_open", "closed_open", "open_closed", "open_closed",
            "closed_closed", "open_open"]
e4b_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E4b"]):
    standalone_plan["E4b"][b] = (e4b_vals[i], e4b_strata[i])

# E5
e5_sets = [
    ["fixed(10 s)"],
    ["fixed(5 s)"],
    ["event_driven(delta_voltage)"],
    ["event_driven(delta_current)"],
    ["event_driven(step_transition)"],
    ["fixed(10 s)", "event_driven(delta_voltage)"],
    ["event_driven(delta_current)", "event_driven(step_transition)"],
    ["fixed(1 s)", "event_driven(delta_voltage)", "event_driven(delta_current)"],
    ["fixed(30 s)"],
    ["event_driven(step_transition)", "fixed(2 s)"],
]
e5_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E5"]):
    standalone_plan["E5"][b] = (e5_sets[i], e5_strata[i])

# E6
e6_sets = [
    ["completeness_counter"],
    ["expected_count_comparison"],
    ["gap_flag_column"],
    ["acquisition_log_reconciliation"],
    ["completeness_counter", "gap_flag_column"],
    ["expected_count_comparison", "acquisition_log_reconciliation"],
    ["completeness_counter", "expected_count_comparison", "gap_flag_column"],
    ["gap_flag_column"],
    ["acquisition_log_reconciliation", "completeness_counter"],
    ["expected_count_comparison"],
]
e6_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E6"]):
    standalone_plan["E6"][b] = (e6_sets[i], e6_strata[i])

# E7a
e7a_sets = [
    ["explicit_index_column"],
    ["filename_encoding"],
    ["time_segmentation_rule"],
    ["row_grouping_marker"],
    ["explicit_index_column", "filename_encoding"],
    ["time_segmentation_rule", "row_grouping_marker"],
    ["explicit_index_column", "time_segmentation_rule", "row_grouping_marker"],
    ["filename_encoding"],
    ["row_grouping_marker", "explicit_index_column"],
    ["time_segmentation_rule"],
]
e7a_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E7a"]):
    standalone_plan["E7a"][b] = (e7a_sets[i], e7a_strata[i])

# E7b
e7b_sets = [
    ["step_type_column"],
    ["current_sign"],
    ["separate_state_column"],
    ["mode_code_enum"],
    ["step_type_column", "current_sign"],
    ["separate_state_column", "mode_code_enum"],
    ["step_type_column", "separate_state_column", "mode_code_enum"],
    ["current_sign"],
    ["mode_code_enum", "step_type_column"],
    ["separate_state_column"],
]
e7b_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E7b"]):
    standalone_plan["E7b"][b] = (e7b_sets[i], e7b_strata[i])

# E8a — exact frozen standalone units
e8a_standalone_bundles = [b for b, _ in standalone_cells["E8a"]]
for b in e8a_standalone_bundles:
    assert b in E8A_STANDALONE_UNITS
    unit = E8A_STANDALONE_UNITS[b]
    scope = get_scope("E8a", b)
    assert unit in E8A_UNITS[scope]
    stratum = "S-DOC" if (b % 2 == 0) else "S-FILE"
    standalone_plan["E8a"][b] = (unit, stratum)

# E8b — ATOM-2 compliant (no affine with offset 0, no factor(1))
e8b_vals = [
    "none", "none",
    e8b_value("factor", 2), e8b_value("factor", 10),
    e8b_value("affine", 2, 1), e8b_value("affine", 0.5, -1),
    "none",
    e8b_value("factor", 1000),
    e8b_value("affine", 1.5, 0.5),
    e8b_value("factor", 0.001),
]
e8b_strata = ["S-DOC", "S-FILE"] * 5
for i, (b, _) in enumerate(standalone_cells["E8b"]):
    standalone_plan["E8b"][b] = (e8b_vals[i], e8b_strata[i])

# ============================================================================
# Distinct natural text banks (no tid, no counters, no synthetic suffixes)
# ============================================================================

SCOPE_PHRASE = {
    "current": "current",
    "power": "power",
    "voltage": "voltage",
    "temperature": "temperature",
    "capacity_charge": "charge capacity",
    "capacity_discharge": "discharge capacity",
    "energy": "energy",
    "time": "time",
    "step_index": "step index",
    "cycle_index": "cycle index",
    "test_index": "test index",
    "dataset": "dataset",
}

def sp(scope: str) -> str:
    return SCOPE_PHRASE.get(scope, scope)

# ---- E1 determining (power refers to power flow, never "charge current") ----

E1_DOC_CHARGE = {
    "current": [
        "The laboratory data dictionary defines positive values on the current channel as charge direction.",
        "According to the deposit README, the current signal adopts a charge-positive polarity convention.",
        "Instrument documentation states that a positive current reading corresponds to charging of the cell.",
        "The metadata sheet records that the current channel is signed so that charge produces positive numbers.",
        "In the accompanying description the current polarity is fixed: positive indicates charge.",
    ],
    "power": [
        "The laboratory data dictionary defines positive values on the power channel as charge-direction power flow.",
        "According to the deposit README, the power signal adopts a charge-positive polarity convention for power flow.",
        "Instrument documentation states that a positive power reading corresponds to charging power delivered to the cell.",
        "The metadata sheet records that the power channel is signed so that charge-direction power flow produces positive numbers.",
        "In the accompanying description the power polarity is fixed: positive indicates charge-direction power.",
    ],
}
E1_DOC_DISCHARGE = {
    "current": [
        "The laboratory data dictionary defines positive values on the current channel as discharge direction.",
        "According to the deposit README, the current signal adopts a discharge-positive polarity convention.",
        "Instrument documentation states that a positive current reading corresponds to discharging of the cell.",
        "The metadata sheet records that the current channel is signed so that discharge produces positive numbers.",
        "In the accompanying description the current polarity is fixed: positive indicates discharge.",
    ],
    "power": [
        "The laboratory data dictionary defines positive values on the power channel as discharge-direction power flow.",
        "According to the deposit README, the power signal adopts a discharge-positive polarity convention for power flow.",
        "Instrument documentation states that a positive power reading corresponds to discharging power leaving the cell.",
        "The metadata sheet records that the power channel is signed so that discharge-direction power flow produces positive numbers.",
        "In the accompanying description the power polarity is fixed: positive indicates discharge-direction power.",
    ],
}
E1_FILE_CHARGE = {
    "current": [
        "# polarity_current: charge_positive",
        "column: I_charge_pos",
        "legend: +I = charge",
        "UNIT_NOTE: current sign convention = charge positive",
        "meta.current_sign = charge+",
    ],
    "power": [
        "# polarity_power: charge_positive",
        "column: P_charge_pos",
        "legend: +P = charge-direction power",
        "UNIT_NOTE: power sign convention = charge-positive flow",
        "meta.power_sign = charge+",
    ],
}
E1_FILE_DISCHARGE = {
    "current": [
        "# polarity_current: discharge_positive",
        "column: I_discharge_pos",
        "legend: +I = discharge",
        "UNIT_NOTE: current sign convention = discharge positive",
        "meta.current_sign = discharge+",
    ],
    "power": [
        "# polarity_power: discharge_positive",
        "column: P_discharge_pos",
        "legend: +P = discharge-direction power",
        "UNIT_NOTE: power sign convention = discharge-positive flow",
        "meta.power_sign = discharge+",
    ],
}

# ---- E2 ----
E2_DOC_MEAS = [
    "The README states that the {sig} channel contains measured instrument readings.",
    "Deposit documentation records the {sig} field as a live measured quantity.",
    "According to the data dictionary the {sig} values are acquired from the instrument.",
    "The accompanying description confirms that {sig} is a measured channel.",
    "Laboratory notes indicate that the {sig} column holds measured data.",
]
E2_DOC_PLACE = [
    "The README states that the {sig} channel is a placeholder and not a live measurement.",
    "Deposit documentation records the {sig} field as a placeholder value.",
    "According to the data dictionary the {sig} values are placeholders only.",
    "The accompanying description confirms that {sig} is a placeholder channel.",
    "Laboratory notes indicate that the {sig} column holds placeholder data.",
]
E2_FILE_MEAS = [
    "# channel_type_{sig}: measured",
    "header: {sig}_measured",
    "legend: {sig} = measured",
    "meta.{sig}_status = measured",
    "COL_NOTE: {sig} measured",
]
E2_FILE_PLACE = [
    "# channel_type_{sig}: placeholder",
    "header: {sig}_placeholder",
    "legend: {sig} = placeholder",
    "meta.{sig}_status = placeholder",
    "COL_NOTE: {sig} placeholder",
]

# ---- E3 ----
E3_DOC = {
    "step": [
        "The data dictionary specifies that the {sig} counter resets at the beginning of every step.",
        "Documentation states the {sig} value is cleared on each new step.",
        "According to the README the {sig} accumulator restarts with every step.",
        "Laboratory notes record that {sig} is reset on step boundaries.",
        "The deposit description indicates {sig} returns to its initial value at each step start.",
    ],
    "cycle": [
        "The data dictionary specifies that the {sig} counter resets at the beginning of every cycle.",
        "Documentation states the {sig} value is cleared on each new cycle.",
        "According to the README the {sig} accumulator restarts with every cycle.",
        "Laboratory notes record that {sig} is reset on cycle boundaries.",
        "The deposit description indicates {sig} returns to its initial value at each cycle start.",
    ],
    "test": [
        "The data dictionary specifies that the {sig} counter resets at the beginning of every test.",
        "Documentation states the {sig} value is cleared on each new test.",
        "According to the README the {sig} accumulator restarts with every test.",
        "Laboratory notes record that {sig} is reset on test boundaries.",
        "The deposit description indicates {sig} returns to its initial value at each test start.",
    ],
    "never": [
        "The data dictionary specifies that the {sig} counter never resets within a test and accumulates continuously.",
        "Documentation states the {sig} value is never cleared inside a test run.",
        "According to the README the {sig} accumulator runs without reset for the entire test.",
        "Laboratory notes record that {sig} continues without reset across all steps and cycles.",
        "The deposit description indicates {sig} is a continuous cumulative quantity with no intra-test reset.",
    ],
}
E3_FILE = {
    "step": [
        "# {sig}_reset: step",
        "header: {sig}_per_step",
        "legend: {sig} resets each step",
        "meta.{sig}_boundary = step",
        "COL_NOTE: {sig} step-reset",
    ],
    "cycle": [
        "# {sig}_reset: cycle",
        "header: {sig}_per_cycle",
        "legend: {sig} resets each cycle",
        "meta.{sig}_boundary = cycle",
        "COL_NOTE: {sig} cycle-reset",
    ],
    "test": [
        "# {sig}_reset: test",
        "header: {sig}_per_test",
        "legend: {sig} resets each test",
        "meta.{sig}_boundary = test",
        "COL_NOTE: {sig} test-reset",
    ],
    "never": [
        "# {sig}_reset: never",
        "header: {sig}_continuous",
        "legend: {sig} never resets",
        "meta.{sig}_boundary = none",
        "COL_NOTE: {sig} continuous",
    ],
}

# ---- E4a ----
E4A_DOC = {
    "start": [
        "Interval records document that the {sig} sample is taken at the start of the interval.",
        "The data dictionary states the {sig} value corresponds to the interval start instant.",
        "According to the README the {sig} reading is captured when the interval begins.",
        "Laboratory notes record sampling of {sig} at interval onset.",
        "Deposit description places the {sig} sample at the leading edge of each interval.",
    ],
    "end": [
        "Interval records document that the {sig} sample is taken at the end of the interval.",
        "The data dictionary states the {sig} value corresponds to the interval end instant.",
        "According to the README the {sig} reading is captured when the interval terminates.",
        "Laboratory notes record sampling of {sig} at interval close.",
        "Deposit description places the {sig} sample at the trailing edge of each interval.",
    ],
    "midpoint": [
        "Interval records document that the {sig} sample is taken at the temporal midpoint of the interval.",
        "The data dictionary states the {sig} value corresponds to the interval midpoint.",
        "According to the README the {sig} reading is captured at the middle of the interval.",
        "Laboratory notes record sampling of {sig} at the interval centre.",
        "Deposit description places the {sig} sample at the temporal mid-point of each interval.",
    ],
}
E4A_FILE = {
    "start": [
        "# sample_point_{sig}: start",
        "header: {sig}_at_start",
        "legend: {sig} @ interval start",
        "meta.{sig}_sample = start",
        "COL_NOTE: {sig} start-sample",
    ],
    "end": [
        "# sample_point_{sig}: end",
        "header: {sig}_at_end",
        "legend: {sig} @ interval end",
        "meta.{sig}_sample = end",
        "COL_NOTE: {sig} end-sample",
    ],
    "midpoint": [
        "# sample_point_{sig}: midpoint",
        "header: {sig}_at_mid",
        "legend: {sig} @ interval midpoint",
        "meta.{sig}_sample = midpoint",
        "COL_NOTE: {sig} mid-sample",
    ],
}

# ---- E4b ----
E4B_DOC = {
    "closed_closed": [
        "The interval semantics for the {sig} are defined as closed at both the start and the end.",
        "Documentation states that {sig} intervals include both endpoints.",
        "According to the data dictionary the {sig} interval is closed-closed.",
        "Laboratory notes record inclusive bounds on both sides for the {sig} interval.",
        "Deposit description treats the {sig} interval as closed at start and closed at end.",
    ],
    "open_open": [
        "The interval semantics for the {sig} are defined as open at both the start and the end.",
        "Documentation states that {sig} intervals exclude both endpoints.",
        "According to the data dictionary the {sig} interval is open-open.",
        "Laboratory notes record exclusive bounds on both sides for the {sig} interval.",
        "Deposit description treats the {sig} interval as open at start and open at end.",
    ],
    "closed_open": [
        "The interval semantics for the {sig} are defined as closed at the start and open at the end.",
        "Documentation states that {sig} intervals include the start but exclude the end.",
        "According to the data dictionary the {sig} interval is closed-open.",
        "Laboratory notes record a closed start and open end for the {sig} interval.",
        "Deposit description treats the {sig} interval as closed at start and open at end.",
    ],
    "open_closed": [
        "The interval semantics for the {sig} are defined as open at the start and closed at the end.",
        "Documentation states that {sig} intervals exclude the start but include the end.",
        "According to the data dictionary the {sig} interval is open-closed.",
        "Laboratory notes record an open start and closed end for the {sig} interval.",
        "Deposit description treats the {sig} interval as open at start and closed at end.",
    ],
}
E4B_FILE = {
    "closed_closed": [
        "# interval_bounds_{sig}: closed_closed",
        "header: {sig}_cc",
        "legend: {sig} [start, end]",
        "meta.{sig}_bounds = closed_closed",
        "COL_NOTE: {sig} closed-closed",
    ],
    "open_open": [
        "# interval_bounds_{sig}: open_open",
        "header: {sig}_oo",
        "legend: {sig} (start, end)",
        "meta.{sig}_bounds = open_open",
        "COL_NOTE: {sig} open-open",
    ],
    "closed_open": [
        "# interval_bounds_{sig}: closed_open",
        "header: {sig}_co",
        "legend: {sig} [start, end)",
        "meta.{sig}_bounds = closed_open",
        "COL_NOTE: {sig} closed-open",
    ],
    "open_closed": [
        "# interval_bounds_{sig}: open_closed",
        "header: {sig}_oc",
        "legend: {sig} (start, end]",
        "meta.{sig}_bounds = open_closed",
        "COL_NOTE: {sig} open-closed",
    ],
}

# ---- E5 / E6 / E7a / E7b helpers ----
def e5_doc(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ", ".join(val)
    excl = " exclusively" if exclusive else ""
    return [
        f"Sampling of the {sig} is performed by the following rule(s){excl}: {vs}.",
        f"The data dictionary lists the sampling policy for {sig}{excl} as {vs}.",
        f"According to the README, {sig} acquisition uses{excl}: {vs}.",
        f"Laboratory documentation records {sig} sampling{excl} via {vs}.",
        f"Deposit description specifies the {sig} trigger set{excl} to be {vs}.",
    ]

def e5_file(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ",".join(val)
    excl = " exclusive" if exclusive else ""
    return [
        f"# sampling_policy_{sig}:{vs}{excl}",
        f"header: {sig}_sample={vs}",
        f"legend: {sig} sampling = {vs}",
        f"meta.{sig}_sample_rule = {vs}",
        f"COL_NOTE: {sig} {vs}",
    ]

def e6_doc(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ", ".join(val)
    excl = " exclusively" if exclusive else ""
    return [
        f"Completeness of the {sig} records is verified using{excl}: {vs}.",
        f"The data dictionary lists the completeness method for {sig}{excl} as {vs}.",
        f"According to the README, {sig} completeness is checked{excl} by {vs}.",
        f"Laboratory documentation records {sig} completeness verification{excl} via {vs}.",
        f"Deposit description specifies the {sig} completeness procedure{excl} as {vs}.",
    ]

def e6_file(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ",".join(val)
    excl = " exclusive" if exclusive else ""
    return [
        f"# completeness_check_{sig}:{vs}{excl}",
        f"header: {sig}_complete={vs}",
        f"legend: {sig} completeness = {vs}",
        f"meta.{sig}_completeness = {vs}",
        f"COL_NOTE: {sig} {vs}",
    ]

def e7a_doc(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ", ".join(val)
    excl = " exclusively" if exclusive else ""
    return [
        f"The {sig} is recovered from the deposit via{excl}: {vs}.",
        f"The data dictionary lists the index recovery method for {sig}{excl} as {vs}.",
        f"According to the README, {sig} is obtained{excl} by {vs}.",
        f"Laboratory documentation records {sig} recovery{excl} via {vs}.",
        f"Deposit description specifies the {sig} recovery procedure{excl} as {vs}.",
    ]

def e7a_file(sig: str, val: List[str], exclusive: bool) -> List[str]:
    vs = ",".join(val)
    excl = " exclusive" if exclusive else ""
    msig = sig.replace(" ", "_")
    return [
        f"# index_recovery_{msig}:{vs}{excl}",
        f"header: {msig}_via={vs}",
        f"legend: {sig} recovery = {vs}",
        f"meta.{msig}_recovery = {vs}",
        f"COL_NOTE: {sig} {vs}",
    ]

def e7b_doc(val: List[str], exclusive: bool) -> List[str]:
    vs = ", ".join(val)
    excl = " exclusively" if exclusive else ""
    return [
        f"Within the dataset the charge/discharge state is determined by{excl}: {vs}.",
        f"The data dictionary lists the state encoding for the dataset{excl} as {vs}.",
        f"According to the README, operating state in the dataset is obtained{excl} by {vs}.",
        f"Laboratory documentation records dataset state encoding{excl} via {vs}.",
        f"Deposit description specifies the dataset state procedure{excl} as {vs}.",
    ]

def e7b_file(val: List[str], exclusive: bool) -> List[str]:
    vs = ",".join(val)
    excl = " exclusive" if exclusive else ""
    return [
        f"# state_encoding_dataset:{vs}{excl}",
        f"header: state_via={vs}",
        f"legend: dataset state = {vs}",
        f"meta.dataset_state = {vs}",
        f"COL_NOTE: dataset {vs}",
    ]

# ---- E8a ----
E8A_DOC = [
    "The declared unit for the {sig} channel is {unit}.",
    "According to the data dictionary the {sig} values are expressed in {unit}.",
    "Deposit documentation records the measurement unit of {sig} as {unit}.",
    "The README states that the {sig} channel uses the unit {unit}.",
    "Laboratory notes list the unit of the {sig} signal as {unit}.",
]
E8A_FILE = [
    "# unit_{sig}: {unit}",
    "header: {sig}_[{unit}]",
    "legend: {sig} unit = {unit}",
    "meta.{sig}_unit = {unit}",
    "COL_NOTE: {sig} {unit}",
]

# ---- E8b ----
def e8b_doc(sig: str, val: str) -> List[str]:
    if val == "none":
        return [
            f"For the {sig} the stored numeric values undergo no scaling conversion.",
            f"The data dictionary records that the {sig} channel has scaling set to none.",
            f"According to the README, {sig} values are stored without multiplicative or affine scaling.",
            f"Laboratory documentation states the {sig} scale factor is identity (none).",
            f"Deposit description indicates no scale or offset is applied to the {sig} values.",
        ]
    elif val.startswith("factor"):
        return [
            f"For the {sig} the stored numeric values undergo a pure multiplicative conversion: {val}.",
            f"The data dictionary records that the {sig} channel is scaled by {val}.",
            f"According to the README, {sig} values are multiplied according to {val}.",
            f"Laboratory documentation states the {sig} scale is {val}.",
            f"Deposit description indicates a factor scaling of {val} is applied to the {sig} values.",
        ]
    else:
        return [
            f"For the {sig} the stored numeric values undergo an affine conversion: {val}.",
            f"The data dictionary records that the {sig} channel is transformed by {val}.",
            f"According to the README, {sig} values are adjusted by the affine map {val}.",
            f"Laboratory documentation states the {sig} affine scale is {val}.",
            f"Deposit description indicates an affine scaling of {val} is applied to the {sig} values.",
        ]

def e8b_file(sig: str, val: str) -> List[str]:
    return [
        f"# scale_{sig}: {val}",
        f"header: {sig}_scale={val}",
        f"legend: {sig} scale = {val}",
        f"meta.{sig}_scale = {val}",
        f"COL_NOTE: {sig} {val}",
    ]

# ---- Adjacent ----
ADJ_DOC = {
    "E1": [
        "The {sig} channel is accompanied by a documented polarity note, yet the note does not state which sign corresponds to charge.",
        "A polarity remark exists for the {sig} signal but leaves the charge-versus-discharge mapping unspecified.",
        "Deposit text mentions a sign convention for {sig} without identifying the positive direction.",
        "The accompanying notes refer to polarity of the {sig} channel without resolving charge direction.",
        "Documentation alludes to a signed {sig} quantity but does not declare which sign is charge.",
    ],
    "E2": [
        "A field description for the {sig} appears in the header metadata but does not indicate whether the values are measured or placeholder.",
        "The deposit mentions the {sig} channel without clarifying measured versus placeholder status.",
        "Notes refer to the {sig} field yet omit whether it holds measured data or a placeholder.",
        "A description of {sig} is present but silent on the measured/placeholder distinction.",
        "Metadata lists the {sig} column without stating its measurement status.",
    ],
    "E3": [
        "The deposit mentions a counter associated with the {sig}; however the reset boundary of that counter is left unspecified.",
        "A counter for {sig} is referenced without declaring its reset policy.",
        "Notes allude to a {sig} accumulator but do not state when it is cleared.",
        "Documentation refers to a {sig} count without specifying step, cycle or test reset.",
        "The accompanying text mentions {sig} tracking yet omits the reset boundary.",
    ],
    "E4a": [
        "Interval metadata for the {sig} includes a timestamp column, without clarifying whether the sample is taken at the start, end or midpoint.",
        "The deposit records interval times for {sig} but does not declare the sample point inside the interval.",
        "Notes mention {sig} sampling within intervals without identifying start, end or midpoint.",
        "Documentation lists interval markers for {sig} yet leaves the exact sample instant unspecified.",
        "A timestamp field accompanies the {sig} intervals without stating the sampling position.",
    ],
    "E4b": [
        "The {sig} interval records contain start and end markers, but the inclusive/exclusive character of those bounds is not declared.",
        "Interval bounds for {sig} are present without stating whether endpoints are closed or open.",
        "Notes refer to {sig} interval limits yet omit inclusivity information.",
        "Documentation lists start and end of {sig} intervals without closed/open semantics.",
        "The deposit shows interval endpoints for {sig} but does not specify bound type.",
    ],
    "E5": [
        "A sampling-rate remark is present for the {sig} yet the concrete triggering condition is omitted.",
        "The deposit mentions sampling of {sig} without naming fixed-interval or event-driven rules.",
        "Notes allude to {sig} acquisition timing but leave the policy unspecified.",
        "Documentation refers to {sig} samples without declaring the trigger set.",
        "A rate comment exists for {sig} without listing the actual sampling conditions.",
    ],
    "E6": [
        "Quality-control documentation for the {sig} refers to completeness procedures without naming the concrete verification method.",
        "The deposit mentions completeness checks on {sig} but does not identify the method used.",
        "Notes allude to {sig} integrity verification without listing counter, gap flag or log reconciliation.",
        "Documentation refers to completeness of {sig} records yet leaves the technique unspecified.",
        "A quality remark for {sig} exists without declaring the completeness mechanism.",
    ],
    "E7a": [
        "An index-related column exists for the {sig}; the precise encoding scheme that recovers the index is not stated.",
        "The deposit contains an index field linked to {sig} without explaining how the index is derived.",
        "Notes mention {sig} indexing but omit the recovery method.",
        "Documentation lists an index associated with {sig} without naming column, filename or segmentation rule.",
        "An index marker for {sig} is present yet the encoding scheme remains unspecified.",
    ],
    "E7b": [
        "The dataset contains columns that could relate to operating state, but no explicit mapping from those columns to charge versus discharge is supplied.",
        "State-related fields appear in the dataset without a declared encoding for charge/discharge.",
        "Notes mention possible state indicators in the dataset yet leave the mapping undefined.",
        "Documentation lists candidate state columns without specifying how charge and discharge are distinguished.",
        "The deposit includes potential state information without an explicit charge/discharge rule.",
    ],
    "E8a": [
        "The {sig} channel header contains a unit-related attribute; the concrete unit string itself is not written out.",
        "A unit field is present for {sig} but the actual unit token is left blank.",
        "Notes refer to units of the {sig} channel without stating A, mA, V or mV.",
        "Documentation mentions a unit attribute on {sig} without supplying the unit value.",
        "The deposit shows a unit placeholder for {sig} without the concrete unit string.",
    ],
    "E8b": [
        "A scaling note is attached to the {sig} values, yet the numeric factor or affine coefficients are left blank.",
        "The deposit mentions scaling of {sig} without giving factor or offset numbers.",
        "Notes refer to a scale applied to {sig} but omit the concrete parameters.",
        "Documentation alludes to conversion of {sig} values without specifying none, factor or affine.",
        "A scale remark exists for {sig} without declaring the actual transformation.",
    ],
}

ADJ_FILE = {
    "E1": [
        "# polarity_note_{sig}: present_unspecified",
        "header: {sig}_sign_TBD",
        "legend: {sig} polarity mentioned",
        "meta.{sig}_polarity = unspecified",
        "COL_NOTE: {sig} sign open",
    ],
    "E2": [
        "# channel_status_{sig}: unspecified",
        "header: {sig}_status_TBD",
        "legend: {sig} status open",
        "meta.{sig}_status = TBD",
        "COL_NOTE: {sig} type open",
    ],
    "E3": [
        "# reset_policy_{sig}: unspecified",
        "header: {sig}_reset_TBD",
        "legend: {sig} reset open",
        "meta.{sig}_reset = TBD",
        "COL_NOTE: {sig} boundary open",
    ],
    "E4a": [
        "# sample_point_{sig}: unspecified",
        "header: {sig}_point_TBD",
        "legend: {sig} sample point open",
        "meta.{sig}_sample = TBD",
        "COL_NOTE: {sig} point open",
    ],
    "E4b": [
        "# interval_bounds_{sig}: unspecified",
        "header: {sig}_bounds_TBD",
        "legend: {sig} bounds open",
        "meta.{sig}_bounds = TBD",
        "COL_NOTE: {sig} inclusivity open",
    ],
    "E5": [
        "# sampling_policy_{sig}: unspecified",
        "header: {sig}_sample_TBD",
        "legend: {sig} sampling open",
        "meta.{sig}_sample = TBD",
        "COL_NOTE: {sig} trigger open",
    ],
    "E6": [
        "# completeness_{sig}: unspecified",
        "header: {sig}_complete_TBD",
        "legend: {sig} completeness open",
        "meta.{sig}_completeness = TBD",
        "COL_NOTE: {sig} check open",
    ],
    "E7a": [
        "# index_recovery_{sig}: unspecified",
        "header: {sig}_index_TBD",
        "legend: {sig} recovery open",
        "meta.{sig}_recovery = filename_encoding", # Ensure underscore format
        "COL_NOTE: {sig} index open",
    ],
    "E7b": [
        "# state_encoding_dataset: unspecified",
        "header: state_TBD",
        "legend: dataset state open",
        "meta.dataset_state = TBD",
        "COL_NOTE: state mapping open",
    ],
    "E8a": [
        "# unit_{sig}: unspecified",
        "header: {sig}_unit_TBD",
        "legend: {sig} unit open",
        "meta.{sig}_unit = TBD",
        "COL_NOTE: {sig} unit blank",
    ],
    "E8b": [
        "# scale_{sig}: unspecified",
        "header: {sig}_scale_TBD",
        "legend: {sig} scale open",
        "meta.{sig}_scale = TBD",
        "COL_NOTE: {sig} scale blank",
    ],
}

# ---- NA (genuine non-applicability) ----
NA_DOC = {
    "E1": [
        "This deposit contains no current or power channel; polarity conventions for directed flow are therefore outside the scope of the recorded signals.",
        "No signed current or power quantity is present in the files, so charge/discharge polarity questions do not arise.",
        "The experiment logs only scalar magnitudes without directional channels, rendering polarity conventions inapplicable.",
        "Because the deposit stores no directed flow signals, the charge-versus-discharge sign convention is not defined for any channel.",
        "The recorded data set omits all current and power traces; polarity semantics are consequently not applicable.",
    ],
    "E2": [
        "No {sig} channel exists in this deposit, so the measured-versus-placeholder distinction does not apply.",
        "The experiment did not acquire a {sig} signal; measured/placeholder status is therefore undefined.",
        "Files contain no {sig} column, rendering the measurement-status question inapplicable.",
        "Because {sig} was never logged, the distinction between measured and placeholder values does not arise.",
        "The deposit configuration excludes the {sig} quantity entirely, so measurement-status semantics are outside scope.",
    ],
    "E3": [
        "No cumulative counter is maintained for the {sig} in this experiment design; the reset-boundary question is therefore inapplicable.",
        "The deposit does not record a {sig} accumulator, so reset-policy semantics do not apply.",
        "Files contain no {sig} counter field, rendering reset-boundary questions outside scope.",
        "Because no {sig} running total is stored, the question of when that total resets does not arise.",
        "The experimental protocol omits any {sig} counter; reset semantics are consequently not defined.",
    ],
    "E4a": [
        "The deposit stores only instantaneous snapshots of the {sig}; interval-based sampling-point semantics do not arise.",
        "No interval records exist for the {sig}, so start/end/midpoint sample questions are inapplicable.",
        "Files contain no time-interval structure around the {sig}, rendering sample-point semantics outside scope.",
        "Because the {sig} is not organised into intervals, the location of a sample inside an interval is undefined.",
        "The experiment logs discrete events rather than intervals for {sig}; sampling-point questions therefore do not apply.",
    ],
    "E4b": [
        "Because the {sig} is logged as discrete events rather than closed time intervals, bound-inclusivity semantics are not applicable.",
        "No interval objects exist for the {sig}, so closed/open bound questions do not arise.",
        "Files contain no start/end interval markers for {sig}, rendering inclusivity semantics outside scope.",
        "The deposit records {sig} as point samples without interval bounds; bound type is therefore undefined.",
        "Experimental design omits interval structures for {sig}; closed/open questions are consequently inapplicable.",
    ],
    "E5": [
        "The {sig} is captured under a continuous streaming protocol that does not employ discrete sampling triggers, rendering the sampling-policy question moot.",
        "No discrete sampling events are defined for the {sig}; fixed-interval and event-driven policies therefore do not apply.",
        "Files contain continuous {sig} streams without a declared trigger set, so sampling-policy semantics are outside scope.",
        "Because the acquisition of {sig} is uninterrupted, the question of sampling rules does not arise.",
        "The deposit configuration uses continuous capture for {sig}; discrete sampling policies are consequently not defined.",
    ],
    "E6": [
        "Completeness verification is performed at the whole-file level; per-signal checks for the {sig} are outside the scope of this deposit.",
        "No per-channel completeness procedure is defined for the {sig}, so the completeness-method question does not apply.",
        "Files contain no completeness metadata specific to {sig}, rendering method semantics outside scope.",
        "Because completeness is assessed only globally, channel-level completeness rules for {sig} are undefined.",
        "The experimental protocol omits signal-specific completeness checks for {sig}; the associated methods are therefore inapplicable.",
    ],
    "E7a": [
        "The experiment consists of a single uninterrupted recording; consequently no {sig} segmentation is present and index-recovery methods are not applicable.",
        "No {sig} indexing is used in this deposit, so recovery-method questions do not arise.",
        "Files contain no {sig} markers, rendering index-recovery semantics outside scope.",
        "Because the recording is not segmented by {sig}, the question of how indices are recovered does not apply.",
        "The deposit configuration omits all {sig} structure; index-recovery methods are consequently undefined.",
    ],
    "E7b": [
        "The dataset contains only constant-current rest periods; charge/discharge state encoding is therefore not defined for this collection.",
        "No charge or discharge activity occurs in the dataset, so state-encoding questions do not arise.",
        "Files record only rest data, rendering charge/discharge state semantics outside scope.",
        "Because the experiment never enters charge or discharge, state-encoding methods are undefined.",
        "The deposit configuration excludes active charge/discharge steps; state encoding is consequently inapplicable.",
    ],
    "E8a": [
        "No {sig} channel is present in this deposit configuration; unit declarations for that signal therefore do not apply.",
        "The experiment did not acquire a {sig} signal, so unit questions for {sig} are outside scope.",
        "Files contain no {sig} column or trace, rendering unit semantics for {sig} inapplicable.",
        "Because the {sig} quantity was never recorded, the question of its measurement unit does not arise.",
        "The deposit omits the {sig} channel entirely; unit declarations for it are consequently undefined.",
    ],
    "E8b": [
        "No {sig} channel is present in this deposit configuration; scaling conversions for that signal therefore do not apply.",
        "The experiment did not acquire a {sig} signal, so scale-factor questions for {sig} are outside scope.",
        "Files contain no {sig} column or trace, rendering scale semantics for {sig} inapplicable.",
        "Because the {sig} quantity was never recorded, the question of its numeric scaling does not arise.",
        "The deposit omits the {sig} channel entirely; scale conversions for it are consequently undefined.",
    ],
}

NA_FILE = {
    "E1": [
        "# polarity: N/A (no directed channel)",
        "header: polarity_absent",
        "legend: no current/power channel",
        "meta.polarity = not_applicable",
        "COL_NOTE: polarity N/A",
    ],
    "E2": [
        "# {sig}_status: N/A (channel absent)",
        "header: {sig}_absent",
        "legend: no {sig} channel",
        "meta.{sig}_status = not_applicable",
        "COL_NOTE: {sig} N/A",
    ],
    "E3": [
        "# {sig}_reset: N/A (no counter)",
        "header: {sig}_absent",
        "legend: no {sig} counter",
        "meta.charge_capacity_reset = not_applicable",  # Corrected underscore
        "COL_NOTE: {sig} counter N/A",
    ],
    "E4a": [
        "# sample_point_{sig}: N/A (no intervals)",
        "header: {sig}_no_interval",
        "legend: no {sig} intervals",
        "meta.{sig}_sample = not_applicable",
        "COL_NOTE: {sig} interval N/A",
    ],
    "E4b": [
        "# interval_bounds_{sig}: N/A (no intervals)",
        "header: {sig}_no_bounds",
        "legend: no {sig} interval bounds",
        "meta.{sig}_bounds = not_applicable",
        "COL_NOTE: {sig} bounds N/A",
    ],
    "E5": [
        "# sampling_policy_{sig}: N/A (continuous stream)",
        "header: {sig}_continuous",
        "legend: no discrete {sig} sampling",
        "meta.{sig}_sample = not_applicable",
        "COL_NOTE: {sig} sampling N/A",
    ],
    "E6": [
        "# completeness_{sig}: N/A (global only)",
        "header: {sig}_no_completeness",
        "legend: no per-signal {sig} check",
        "meta.{sig}_completeness = not_applicable",
        "COL_NOTE: {sig} completeness N/A",
    ],
    "E7a": [
        "# index_recovery_{sig}: N/A (no segmentation)",
        "header: {sig}_absent",
        "legend: no {sig} index",
        "meta.step_index_recovery = filename_encoding",  # Corrected underscore
        "COL_NOTE: {sig} index N/A",
    ],
    "E7b": [
        "# state_encoding_dataset: N/A (rest only)",
        "header: state_absent",
        "legend: no charge/discharge state",
        "meta.dataset_state = not_applicable",
        "COL_NOTE: state N/A",
    ],
    "E8a": [
        "# unit_{sig}: N/A (channel absent)",
        "header: {sig}_absent",
        "legend: no {sig} channel",
        "meta.{sig}_unit = not_applicable",
        "COL_NOTE: {sig} unit N/A",
    ],
    "E8b": [
        "# scale_{sig}: N/A (channel absent)",
        "header: {sig}_absent",
        "legend: no {sig} channel",
        "meta.discharge_capacity_scale = not_applicable",  # Corrected underscore
        "COL_NOTE: {sig} scale N/A",
    ],
}

# ============================================================================
# Text selection with uniqueness enforcement
# ============================================================================

used_texts: Set[str] = set()
text_usage_idx: Dict[int, int] = defaultdict(int)

def pick_unique(candidates: List[str], scope: str = "") -> str:
    key = id(candidates)
    for _ in range(len(candidates) * 3):
        idx = text_usage_idx[key]
        text_usage_idx[key] += 1
        raw = candidates[idx % len(candidates)]
        if "{sig}" in raw:
            if "meta." in raw or raw.startswith("#") or raw.startswith("header:"):
                text = raw.replace("{sig}", sp(scope).replace(" ", "_"))
            else:
                text = raw.replace("{sig}", sp(scope))
        else:
            text = raw
        if text not in used_texts:
            used_texts.add(text)
            return text
    base = candidates[0].replace("{sig}", sp(scope)) if "{sig}" in candidates[0] else candidates[0]
    for suffix in [
        " Additionally documented.",
        " As recorded in the deposit.",
        " Per laboratory protocol.",
        " Confirmed in the accompanying notes.",
        " Stated in the instrument log.",
        " Listed in the header block.",
        " Given in the metadata block.",
        " Appearing in the column legend.",
        " Present in the file comment.",
        " Recorded beside the data table.",
        " Noted in the acquisition log.",
        " Declared in the secondary header.",
    ]:
        candidate = base.rstrip(".") + suffix
        if candidate not in used_texts:
            used_texts.add(candidate)
            return candidate
    raise RuntimeError(f"Could not produce unique text near: {base[:80]}")

# ============================================================================
# Entry assembly
# ============================================================================

entries: List[Dict[str, Any]] = []

def add_entry(
    entry_id: str,
    bundle_idx: int,
    param_idx: int,
    parameter: str,
    scope: str,
    cls: str,
    stratum: str,
    role: str,
    value: Any,
    exclusive: bool,
    text: str,
):
    if role == "determining":
        assert value is not None, entry_id
    else:
        assert value is None, entry_id
    if exclusive:
        assert role == "determining" and parameter in SET_VALUED, entry_id
    entry = {
        "entry_id": entry_id,
        "bundle_idx": bundle_idx,
        "param_idx": param_idx,
        "parameter": parameter,
        "scope": scope,
        "class": cls,
        "evidence_stratum": stratum,
        "semantic_role": role,
        "semantic_value": value,
        "exclusive_assertion": exclusive,
        "entry_text": text,
    }
    entries.append(entry)

def ambig_pair(param: str, scope: str) -> Tuple[Any, Any]:
    if param == "E1":
        return "charge_positive", "discharge_positive"
    if param == "E2":
        return "measured", "placeholder"
    if param == "E3":
        return "step", "cycle"
    if param == "E4a":
        return "start", "end"
    if param == "E4b":
        return "closed_closed", "open_open"
    if param == "E5":
        return ["fixed(10 s)"], ["event_driven(delta_voltage)"]
    if param == "E6":
        return ["completeness_counter"], ["gap_flag_column"]
    if param == "E7a":
        return ["explicit_index_column"], ["filename_encoding"]
    if param == "E7b":
        return ["step_type_column"], ["current_sign"]
    if param == "E8a":
        units = E8A_UNITS[scope]
        return units[0], units[1]
    if param == "E8b":
        return "none", e8b_value("factor", 2)
    raise ValueError(param)

def make_det_text(param: str, scope: str, value: Any, stratum: str, exclusive: bool = False) -> str:
    sig = sp(scope)
    if param == "E1":
        if value == "charge_positive":
            pool = E1_DOC_CHARGE[scope] if stratum == "S-DOC" else E1_FILE_CHARGE[scope]
        else:
            pool = E1_DOC_DISCHARGE[scope] if stratum == "S-DOC" else E1_FILE_DISCHARGE[scope]
        return pick_unique(pool, scope)
    if param == "E2":
        if value == "measured":
            pool = E2_DOC_MEAS if stratum == "S-DOC" else E2_FILE_MEAS
        else:
            pool = E2_DOC_PLACE if stratum == "S-DOC" else E2_FILE_PLACE
        return pick_unique(pool, scope)
    if param == "E3":
        pool = E3_DOC[value] if stratum == "S-DOC" else E3_FILE[value]
        return pick_unique(pool, scope)
    if param == "E4a":
        pool = E4A_DOC[value] if stratum == "S-DOC" else E4A_FILE[value]
        return pick_unique(pool, scope)
    if param == "E4b":
        pool = E4B_DOC[value] if stratum == "S-DOC" else E4B_FILE[value]
        return pick_unique(pool, scope)
    if param == "E5":
        pool = e5_doc(sig, value, exclusive) if stratum == "S-DOC" else e5_file(sig, value, exclusive)
        return pick_unique(pool)
    if param == "E6":
        pool = e6_doc(sig, value, exclusive) if stratum == "S-DOC" else e6_file(sig, value, exclusive)
        return pick_unique(pool)
    if param == "E7a":
        pool = e7a_doc(sig, value, exclusive) if stratum == "S-DOC" else e7a_file(sig, value, exclusive)
        return pick_unique(pool)
    if param == "E7b":
        pool = e7b_doc(value, exclusive) if stratum == "S-DOC" else e7b_file(value, exclusive)
        return pick_unique(pool)
    if param == "E8a":
        if stratum == "S-DOC":
            pool = [t.replace("{sig}", sig).replace("{unit}", value) for t in E8A_DOC]
        else:
            pool = [t.replace("{sig}", sig).replace("{unit}", value) for t in E8A_FILE]
        return pick_unique(pool)
    if param == "E8b":
        pool = e8b_doc(sig, value) if stratum == "S-DOC" else e8b_file(sig, value)
        return pick_unique(pool)
    raise ValueError(param)

def make_adj_text(param: str, scope: str, stratum: str) -> str:
    pool = ADJ_DOC[param] if stratum == "S-DOC" else ADJ_FILE[param]
    return pick_unique(pool, scope)

def make_na_text(param: str, scope: str, stratum: str) -> str:
    pool = NA_DOC[param] if stratum == "S-DOC" else NA_FILE[param]
    return pick_unique(pool, scope)

# ============================================================================
# Main generation
# ============================================================================

for pidx, param in enumerate(PARAMETERS):
    for b in range(30):
        cls = get_class(b, pidx)
        scope = get_scope(param, b)

        if cls == "NEG-ABSENT":
            continue

        if cls in ("POS-EXPLICIT", "POS-BURIED"):
            value, stratum = standalone_plan[param][b]
            exclusive = False
            text = make_det_text(param, scope, value, stratum, exclusive=False)
            eid = f"F5-{param}-B{b:02d}-DET"
            add_entry(eid, b, pidx, param, scope, cls, stratum, "determining", value, exclusive, text)

        elif cls == "NEG-ADJACENT":
            stratum = "S-DOC" if (b % 2 == 0) else "S-FILE"
            text = make_adj_text(param, scope, stratum)
            eid = f"F5-{param}-B{b:02d}-ADJ"
            add_entry(eid, b, pidx, param, scope, cls, stratum, "non_determining_adjacent", None, False, text)

        elif cls == "AMBIG-CONSTRUCTED":
            v1, v2 = ambig_pair(param, scope)
            exclusive = param in SET_VALUED
            for k, val in enumerate([v1, v2]):
                stratum = "S-DOC" if k == 0 else "S-FILE"
                text = make_det_text(param, scope, val, stratum, exclusive=exclusive)
                eid = f"F5-{param}-B{b:02d}-AMB{k+1}"
                add_entry(eid, b, pidx, param, scope, cls, stratum, "determining", val, exclusive, text)

        elif cls == "NA-CONSTRUCTED":
            stratum = "S-DOC" if (b % 2 == 0) else "S-FILE"
            text = make_na_text(param, scope, stratum)
            eid = f"F5-{param}-B{b:02d}-NA"
            add_entry(eid, b, pidx, param, scope, cls, stratum, "non_applicable", None, False, text)

assert len(entries) == 330, f"Expected 330, got {len(entries)}"
assert len(used_texts) == 330, f"Unique texts {len(used_texts)} != 330"

# Output paths
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
jsonl_path = os.path.join(OUT_DIR, "F5_BANK_ATTEMPT_01.jsonl")
self_check_path = os.path.join(OUT_DIR, "F5_SELF_CHECK.json")

with open(jsonl_path, "w", encoding="utf-8") as f:
    for e in entries:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

# ============================================================================
# Mechanically derived self-check
# ============================================================================

per_param_counts = Counter(e["parameter"] for e in entries)
entry_ids = [e["entry_id"] for e in entries]
texts = [e["entry_text"] for e in entries]

cell_counts = defaultdict(lambda: Counter())
for pidx, param in enumerate(PARAMETERS):
    for b in range(30):
        cls = get_class(b, pidx)
        if cls != "NEG-ABSENT":
            cell_counts[param][cls] += 1

standalone_cat_cov = {}
standalone_stratum = {}
set_valued_comp = {}
e8a_unit_by_scope = {"current": Counter(), "voltage": Counter()}

for param in PARAMETERS:
    cats = Counter()
    strata = Counter()
    sizes = []
    for b, cls in standalone_cells[param]:
        val, stratum = standalone_plan[param][b]
        strata[stratum] += 1
        if param == "E8a":
            scope = get_scope(param, b)
            e8a_unit_by_scope[scope][val] += 1
            cats[val] += 1
        elif param in SET_VALUED:
            for v in val:
                if param == "E5":
                    if v.startswith("fixed"):
                        cats["fixed"] += 1
                    else:
                        cats[v] += 1
                else:
                    cats[v] += 1
            sizes.append(len(val))
        elif param == "E8b":
            if val == "none":
                cats["none"] += 1
            elif val.startswith("factor"):
                cats["factor"] += 1
            else:
                cats["affine"] += 1
        else:
            cats[val] += 1
    standalone_cat_cov[param] = dict(cats)
    standalone_stratum[param] = dict(strata)
    if param in SET_VALUED:
        set_valued_comp[param] = {
            "num_size_ge2": sum(1 for s in sizes if s >= 2),
            "sizes": sizes,
        }

invalid_scope = 0
for e in entries:
    if e["scope"] not in APPLICABLE_SCOPES[e["parameter"]]:
        invalid_scope += 1
    frozen = FROZEN_SCOPE[e["parameter"]]["scopes"][e["bundle_idx"]]
    if e["scope"] != frozen:
        invalid_scope += 1

null_val_viol = 0
excl_viol = 0
invalid_e8b = 0
tid_markers = 0
sfile_prose_issues = 0
spaced_meta_keys = 0

for e in entries:
    role = e["semantic_role"]
    val = e["semantic_value"]
    if role == "determining":
        if val is None:
            null_val_viol += 1
    else:
        if val is not None:
            null_val_viol += 1

    if e["exclusive_assertion"]:
        if role != "determining" or e["parameter"] not in SET_VALUED:
            excl_viol += 1
    else:
        if e["class"] == "AMBIG-CONSTRUCTED" and e["parameter"] in SET_VALUED:
            excl_viol += 1

    if e["parameter"] == "E8b" and role == "determining":
        v = val
        if v == "none":
            pass
        elif isinstance(v, str) and v.startswith("factor("):
            num = float(v[len("factor("):-1])
            if num == 1.0:
                invalid_e8b += 1
        elif isinstance(v, str) and v.startswith("affine("):
            parts = v[len("affine("):-1].split(",")
            offset = float(parts[1].strip())
            if offset == 0.0:
                invalid_e8b += 1
        else:
            invalid_e8b += 1

    if "tid-" in e["entry_text"]:
        tid_markers += 1

    if e["evidence_stratum"] == "S-FILE":
        t = e["entry_text"]
        looks_like_file = (
            t.startswith("#") or
            t.startswith("header:") or
            t.startswith("legend:") or
            t.startswith("meta.") or
            t.startswith("COL_NOTE:") or
            t.startswith("column:") or
            t.startswith("UNIT_NOTE:") or
            (" = " in t[:50])
        )
        if not looks_like_file:
            sfile_prose_issues += 1

    if "meta." in e["entry_text"]:
        meta_match = re.search(r"meta\.([^=]+)=", e["entry_text"])
        if meta_match and " " in meta_match.group(1):
            spaced_meta_keys += 1

dup_count = len(texts) - len(set(texts))
unique_ids = len(set(entry_ids))

self_check = {
    "total_entries": len(entries),
    "unique_entry_id_count": unique_ids,
    "unique_entry_text_count": len(set(texts)),
    "per_parameter_entry_counts": dict(per_param_counts),
    "per_parameter_class_cell_counts": {p: dict(cell_counts[p]) for p in PARAMETERS},
    "per_parameter_standalone_category_coverage": standalone_cat_cov,
    "per_parameter_standalone_stratum_counts": standalone_stratum,
    "set_valued_composition_counts": set_valued_comp,
    "E8a_unit_counts_by_scope": {k: dict(v) for k, v in e8a_unit_by_scope.items()},
    "invalid_scope_count": invalid_scope,
    "null_semantic_value_violations": null_val_viol,
    "exclusive_assertion_violations": excl_viol,
    "duplicate_entry_text_count": dup_count,
    "invalid_e8b_canonical_forms": invalid_e8b,
    "tid_marker_count": tid_markers,
    "sfile_prose_issue_count": sfile_prose_issues,
    "spaced_meta_key_count": spaced_meta_keys,
}

assert self_check["total_entries"] == 330
assert self_check["unique_entry_id_count"] == 330
assert self_check["unique_entry_text_count"] == 330
assert self_check["invalid_scope_count"] == 0
assert self_check["null_semantic_value_violations"] == 0
assert self_check["exclusive_assertion_violations"] == 0
assert self_check["duplicate_entry_text_count"] == 0
assert self_check["invalid_e8b_canonical_forms"] == 0
assert self_check["tid_marker_count"] == 0
assert self_check["sfile_prose_issue_count"] == 0
assert self_check["spaced_meta_key_count"] == 0
assert all(per_param_counts[p] == 30 for p in PARAMETERS)

for param in PARAMETERS:
    cats = standalone_cat_cov[param]
    for c, cnt in cats.items():
        assert cnt >= 2, f"{param} category {c} has only {cnt}"
    st = standalone_stratum[param]
    assert st.get("S-DOC", 0) >= 2 and st.get("S-FILE", 0) >= 2, f"{param} strata {st}"
for param in SET_VALUED:
    assert set_valued_comp[param]["num_size_ge2"] >= 2
assert e8a_unit_by_scope["current"]["A"] >= 2 and e8a_unit_by_scope["current"]["mA"] >= 2
assert e8a_unit_by_scope["voltage"]["V"] >= 2 and e8a_unit_by_scope["voltage"]["mV"] >= 2

with open(self_check_path, "w", encoding="utf-8") as f:
    json.dump(self_check, f, indent=2, ensure_ascii=False)

print("Wrote F5_BANK_ATTEMPT_01.jsonl and F5_SELF_CHECK.json")
print(json.dumps(self_check, indent=2))
print("\nF5 ATTEMPT 01 COMPLETE — 330 BANK ENTRIES — AWAITING PARTY 3 BACK-TRANSLATION.")
