"""
Template Generator and Fidelity Checker for S2 CVD Construction.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.8).

§5.8 Fidelity Checker:
The fidelity checker receives the bundle bytes and the frozen bank, and NOT
the realization index as an authority:
1. Search bundle bytes for byte-exact occurrences of bank entries.
2. Reconstruct a derived ground-truth record from the occurrences and byte spans.
   MUST NOT read expected class/verdict from sealed record to derive them.
3. The derived record must equal the sealed record byte-identically.
4. For every NEG-ABSENT parameter-cell: no determining entry for that (parameter, scope)
   — of any value — occurs anywhere in the bundle.
5. For every NEG-ADJACENT parameter-cell: the present entry is the keyed adjacent entry
   and no determining entry for that (parameter, scope) occurs.
6. Every bundle carrying an E3 parameter-cell declares the §4.3 structure; every bundle
   carrying an E4a/E4b parameter-cell declares a strictly positive interval length.
7. The realization index is a cross-check only. Index–bytes disagreement halts at F8.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
import hashlib
import json

from .constants import PARAMETERS
from .structural_validators import (
    validate_e3_structure,
    validate_e4_positive_duration,
    check_incompatibility,
)

try:
    from ..f3_protocol.canonical_serializer import (
        canonicalize_semantic_value,
        serialize_canonical_semantic_value_string,
    )
except (ImportError, ValueError):
    from f3_protocol.canonical_serializer import (
        canonicalize_semantic_value,
        serialize_canonical_semantic_value_string,
    )


class BankEntry:
    def __init__(
        self,
        entry_id: str,
        parameter: str,
        scope: str,
        evidence_stratum: str,
        semantic_role: str,  # 'determining', 'non_determining_adjacent', 'non_applicable'
        semantic_value: Any,
        entry_text: str,
        exclusive_assertion: bool = False,
    ):
        self.entry_id = entry_id
        self.parameter = parameter
        self.scope = scope
        self.evidence_stratum = evidence_stratum
        self.semantic_role = semantic_role
        self.semantic_value = semantic_value
        self.entry_text = entry_text
        self.exclusive_assertion = exclusive_assertion

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "parameter": self.parameter,
            "scope": self.scope,
            "evidence_stratum": self.evidence_stratum,
            "semantic_role": self.semantic_role,
            "semantic_value": self.semantic_value,
            "entry_text": self.entry_text,
            "exclusive_assertion": self.exclusive_assertion,
        }


class RealizationRecord:
    def __init__(
        self,
        bundle_idx: int,
        entry_id: str,
        param: str,
        scope: str,
        cls_name: str,
        entry_text: str,
        component: str,  # 'article', 'readme', 'csv_header'
        byte_start: int,
        byte_end: int,
    ):
        self.bundle_idx = bundle_idx
        self.entry_id = entry_id
        self.param = param
        self.scope = scope
        self.cls_name = cls_name
        self.entry_text = entry_text
        self.component = component
        self.byte_start = byte_start
        self.byte_end = byte_end

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundle_idx": self.bundle_idx,
            "entry_id": self.entry_id,
            "parameter": self.param,
            "scope": self.scope,
            "class": self.cls_name,
            "entry_text": self.entry_text,
            "component": self.component,
            "byte_start": self.byte_start,
            "byte_end": self.byte_end,
        }


class BundleArtifacts:
    def __init__(
        self,
        bundle_idx: int,
        article_bytes: bytes,
        readme_bytes: bytes,
        csv_header_bytes: bytes,
    ):
        self.bundle_idx = bundle_idx
        self.article_bytes = article_bytes
        self.readme_bytes = readme_bytes
        self.csv_header_bytes = csv_header_bytes

    def get_component_bytes(self, component: str) -> bytes:
        if component == "article":
            return self.article_bytes
        elif component == "readme":
            return self.readme_bytes
        elif component == "csv_header":
            return self.csv_header_bytes
        raise ValueError(f"Unknown component {component}")

    def components(self) -> List[Tuple[str, bytes]]:
        return [
            ("article", self.article_bytes),
            ("readme", self.readme_bytes),
            ("csv_header", self.csv_header_bytes),
        ]

    def sha256_map(self) -> Dict[str, str]:
        return {
            "article": hashlib.sha256(self.article_bytes).hexdigest(),
            "readme": hashlib.sha256(self.readme_bytes).hexdigest(),
            "csv_header": hashlib.sha256(self.csv_header_bytes).hexdigest(),
        }


class DiscoveredOccurrence:
    def __init__(
        self,
        entry: BankEntry,
        component: str,
        byte_start: int,
        byte_end: int,
    ):
        self.entry = entry
        self.component = component
        self.byte_start = byte_start
        self.byte_end = byte_end


def search_bundle_bytes_for_bank_entries(
    artifacts: BundleArtifacts,
    frozen_bank: List[BankEntry],
) -> List[DiscoveredOccurrence]:
    """
    Independently search bundle bytes for byte-exact occurrences of bank entries.
    """
    discovered: List[DiscoveredOccurrence] = []
    for comp_name, comp_bytes in artifacts.components():
        for entry in frozen_bank:
            target_bytes = entry.entry_text.encode("utf-8")
            start = 0
            while True:
                pos = comp_bytes.find(target_bytes, start)
                if pos == -1:
                    break
                discovered.append(
                    DiscoveredOccurrence(
                        entry=entry,
                        component=comp_name,
                        byte_start=pos,
                        byte_end=pos + len(target_bytes),
                    )
                )
                start = pos + len(target_bytes)
    return discovered


def get_placement_in_component(component: str, pos: int, comp_bytes: bytes) -> str:
    """
    Mechanically determine whether byte offset `pos` is in prominent or buried region.
    Independent of expected class or slot metadata.

    Prominent and buried regions are defined by natural document section structure:
    - In 'article': text before '## Supplementary Appendix' is prominent; text at or after is buried.
    - In 'readme': text before '## Supplemental Archive Notes' is prominent; text at or after is buried.
    - In 'csv_header': text before '# --- Extended File Annotations ---' is prominent; text at or after is buried.
    """
    if component == "article":
        marker = b"## Supplementary Appendix"
        idx = comp_bytes.find(marker)
        if idx != -1 and pos >= idx:
            return "buried"
        return "prominent"
    elif component == "readme":
        marker = b"## Supplemental Archive Notes"
        idx = comp_bytes.find(marker)
        if idx != -1 and pos >= idx:
            return "buried"
        return "prominent"
    elif component == "csv_header":
        marker = b"# --- Extended File Annotations ---"
        idx = comp_bytes.find(marker)
        if idx != -1 and pos >= idx:
            return "buried"
        return "prominent"
    return "prominent"


def reconstruct_derived_ground_truth(
    discovered: List[DiscoveredOccurrence],
    bundle_slots: Dict[str, Dict[str, Any]],
    artifacts: Optional[BundleArtifacts] = None,
    bundle_idx: int = 0,
) -> Dict[str, Any]:
    """
    Reconstruct derived ground truth from discovered occurrences and byte spans.
    MUST NOT read expected class or verdict from a sealed record.

    - Derives POS-EXPLICIT vs POS-BURIED strictly from actual byte placement in bundle bytes.
    - Emits location-independent readings: (entry_id, semantic_value, evidence_stratum,
      exclusive_assertion, verbatim_excerpt) without component or byte spans.
    - Populates support_entry_ids (canonically sorted bank entry IDs).
    - Preserves iteration over all parameter-cells in bundle_slots (including NEG-ABSENT).
    """
    derived: Dict[str, Any] = {}

    # Index discovered occurrences by (parameter, scope)
    occurrences_by_param_scope: Dict[Tuple[str, str], List[DiscoveredOccurrence]] = {}
    for occ in discovered:
        key = (occ.entry.parameter, occ.entry.scope)
        if key not in occurrences_by_param_scope:
            occurrences_by_param_scope[key] = []
        occurrences_by_param_scope[key].append(occ)

    for param, slot_info in bundle_slots.items():
        scope = slot_info["scope"]
        matching_occs = occurrences_by_param_scope.get((param, scope), [])

        det_occs = [occ for occ in matching_occs if occ.entry.semantic_role == "determining"]
        adj_occs = [occ for occ in matching_occs if occ.entry.semantic_role == "non_determining_adjacent"]
        na_occs = [occ for occ in matching_occs if occ.entry.semantic_role == "non_applicable"]

        if len(det_occs) == 1:
            det = det_occs[0]
            stratum = det.entry.evidence_stratum
            vc = "EXPLICIT_DOC" if stratum == "S-DOC" else "EXPLICIT_FILE"

            # IC-2: Class derived strictly from actual occurrence position in bundle bytes
            if artifacts is not None:
                comp_bytes = artifacts.get_component_bytes(det.component)
                placement = get_placement_in_component(det.component, det.byte_start, comp_bytes)
                cls_name = "POS-BURIED" if placement == "buried" else "POS-EXPLICIT"
            else:
                slot_placement = slot_info.get("placement", "prominent")
                cls_name = "POS-BURIED" if slot_placement == "buried" else "POS-EXPLICIT"

            canon_val = canonicalize_semantic_value(det.entry.semantic_value)
            readings = [{
                "entry_id": det.entry.entry_id,
                "semantic_value": canon_val,
                "evidence_stratum": stratum,
                "exclusive_assertion": det.entry.exclusive_assertion,
                "verbatim_excerpt": det.entry.entry_text,
            }]
            support_entry_ids = [det.entry.entry_id]

            derived[param] = {
                "bundle_idx": bundle_idx,
                "parameter": param,
                "scope": scope,
                "class": cls_name,
                "verdict_class": vc,
                "readings": readings,
                "support_entry_ids": support_entry_ids,
            }

        elif len(det_occs) >= 2:
            # Ambiguity: check incompatibility under §5.7
            incompatible = False
            for i in range(len(det_occs)):
                for j in range(i + 1, len(det_occs)):
                    chk = check_incompatibility(param, scope, det_occs[i].entry.to_dict(), det_occs[j].entry.to_dict())
                    if chk["incompatible"]:
                        incompatible = True
                        break
                if incompatible:
                    break

            cls_name = "AMBIG-CONSTRUCTED"
            vc = "AMBIGUOUS" if incompatible else ("EXPLICIT_DOC" if det_occs[0].entry.evidence_stratum == "S-DOC" else "EXPLICIT_FILE")
            readings = [
                {
                    "entry_id": occ.entry.entry_id,
                    "semantic_value": canonicalize_semantic_value(occ.entry.semantic_value),
                    "evidence_stratum": occ.entry.evidence_stratum,
                    "exclusive_assertion": occ.entry.exclusive_assertion,
                    "verbatim_excerpt": occ.entry.entry_text,
                }
                for occ in det_occs
            ]
            readings.sort(key=lambda x: serialize_canonical_semantic_value_string(x["semantic_value"]))
            support_entry_ids = sorted([occ.entry.entry_id for occ in det_occs])

            derived[param] = {
                "bundle_idx": bundle_idx,
                "parameter": param,
                "scope": scope,
                "class": cls_name,
                "verdict_class": vc,
                "readings": readings,
                "support_entry_ids": support_entry_ids,
            }

        else:  # 0 determining occurrences
            if len(adj_occs) >= 1:
                derived[param] = {
                    "bundle_idx": bundle_idx,
                    "parameter": param,
                    "scope": scope,
                    "class": "NEG-ADJACENT",
                    "verdict_class": "ABSENT",
                    "readings": [],
                    "support_entry_ids": sorted([occ.entry.entry_id for occ in adj_occs]),
                }
            elif len(na_occs) >= 1:
                derived[param] = {
                    "bundle_idx": bundle_idx,
                    "parameter": param,
                    "scope": scope,
                    "class": "NA-CONSTRUCTED",
                    "verdict_class": "NOT_APPLICABLE",
                    "readings": [],
                    "support_entry_ids": sorted([occ.entry.entry_id for occ in na_occs]),
                }
            else:
                derived[param] = {
                    "bundle_idx": bundle_idx,
                    "parameter": param,
                    "scope": scope,
                    "class": "NEG-ABSENT",
                    "verdict_class": "ABSENT",
                    "readings": [],
                    "support_entry_ids": [],
                }

    return derived


def serialize_ground_truth_canonically(gt: Any) -> bytes:
    """
    Produce deterministic canonical bytes for ground truth comparison (§6.6).
    Supports:
    - Dict mapping param -> cell
    - List of parameter-cell dicts (11 cells for bundle or 330 cells for corpus)
    """
    if isinstance(gt, list):
        def cell_sort_key(c: Any) -> Tuple[int, int]:
            if isinstance(c, dict):
                b_idx = c.get("bundle_idx", 0)
                p_str = c.get("parameter", "")
                p_idx = PARAMETERS.index(p_str) if p_str in PARAMETERS else 0
                return (b_idx, p_idx)
            return (0, 0)
        gt_sorted = sorted(gt, key=cell_sort_key)
        return json.dumps(gt_sorted, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")
    elif isinstance(gt, dict):
        return json.dumps(gt, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return json.dumps(gt, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")


def check_fidelity(
    artifacts: BundleArtifacts,
    frozen_bank: List[BankEntry],
    sealed_ground_truth_bytes: bytes,
    bundle_slots: Dict[str, Dict[str, Any]],
    bundle_manifest: Dict[str, Any],
    realization_index: Optional[List[RealizationRecord]] = None,
) -> Dict[str, Any]:
    """
    §5.8 Fidelity Checker:
    1. Search bundle bytes for byte-exact bank entry occurrences.
    2. Run NEG-ABSENT / NEG-ADJACENT invariant checks FIRST (observable violations).
    3. Invoke E3 structural validator when bundle carries E3.
    4. Invoke E4 positive-duration validator when bundle carries E4a/E4b.
    5. Reconstruct derived ground-truth record without borrowing from sealed record.
    6. Compare actual canonical derived bytes against actual sealed record bytes.
    7. Cross-check against realization_index (if provided).
    """
    # 1. Independently search bundle bytes
    discovered = search_bundle_bytes_for_bank_entries(artifacts, frozen_bank)

    # 2. Invariant checks for NEG-ABSENT and NEG-ADJACENT (§5.8 items 4 and 5)
    for param, slot_info in bundle_slots.items():
        scope = slot_info["scope"]
        expected_class = slot_info.get("class")
        keyed_adj_id = slot_info.get("keyed_adjacent_entry_id")

        found_det = [
            occ for occ in discovered
            if occ.entry.parameter == param and occ.entry.scope == scope and occ.entry.semantic_role == "determining"
        ]
        found_adj = [
            occ for occ in discovered
            if occ.entry.parameter == param and occ.entry.scope == scope and occ.entry.semantic_role == "non_determining_adjacent"
        ]

        # §5.8 Item 4: NEG-ABSENT: no determining entry for (parameter, scope) may occur anywhere in the bundle
        if expected_class == "NEG-ABSENT":
            if len(found_det) > 0:
                return {
                    "valid": False,
                    "error": f"NEG-ABSENT violation for {param} ({scope}): determining entry found in bundle bytes",
                }

        # §5.8 Item 5: NEG-ADJACENT: keyed adjacent entry occurs AND no determining entry occurs
        if expected_class == "NEG-ADJACENT":
            if len(found_det) > 0:
                return {
                    "valid": False,
                    "error": f"NEG-ADJACENT violation for {param} ({scope}): determining entry found in bundle bytes",
                }
            if len(found_adj) == 0:
                return {
                    "valid": False,
                    "error": f"NEG-ADJACENT violation for {param} ({scope}): adjacent entry was not found in bundle bytes",
                }
            if keyed_adj_id is not None:
                if not any(occ.entry.entry_id == keyed_adj_id for occ in found_adj):
                    return {
                        "valid": False,
                        "error": f"NEG-ADJACENT violation for {param} ({scope}): specifically keyed adjacent entry '{keyed_adj_id}' not found in bundle bytes",
                    }

    # 3. Invoke E3 structural validator when bundle carries E3 (§5.8 item 6)
    if "E3" in bundle_slots:
        e3_res = validate_e3_structure(bundle_manifest)
        if not e3_res["valid"]:
            return {
                "valid": False,
                "error": f"E3 structural validation failed: {e3_res.get('reason')}",
            }

    # 4. Invoke E4 positive-duration validator when bundle carries E4a or E4b (§5.8 item 6)
    if "E4a" in bundle_slots or "E4b" in bundle_slots:
        e4_res = validate_e4_positive_duration(bundle_manifest)
        if not e4_res["valid"]:
            return {
                "valid": False,
                "error": f"E4 positive-duration validation failed: {e4_res.get('reason')}",
            }

    # 5. Reconstruct derived ground truth independently
    derived_gt = reconstruct_derived_ground_truth(discovered, bundle_slots, artifacts, bundle_idx=artifacts.bundle_idx)

    # Check if sealed_ground_truth_bytes decodes to a list of cells
    try:
        sealed_data = json.loads(sealed_ground_truth_bytes.decode("utf-8"))
        if isinstance(sealed_data, list):
            derived_list = [derived_gt[p] for p in PARAMETERS if p in derived_gt]
            derived_bytes = serialize_ground_truth_canonically(derived_list)
        else:
            derived_bytes = serialize_ground_truth_canonically(derived_gt)
    except Exception:
        derived_bytes = serialize_ground_truth_canonically(derived_gt)

    # 6. Compare actual canonical derived bytes against actual sealed record bytes (§5.8 item 3)
    if derived_bytes != sealed_ground_truth_bytes:
        return {
            "valid": False,
            "error": "Derived ground truth bytes do not equal sealed ground truth bytes",
            "derived_bytes": derived_bytes,
        }

    # 7. Cross-check against realization_index (§5.8 item 7)
    if realization_index is not None:
        discovered_keys: Set[Tuple[str, str, int, int]] = {
            (occ.entry.entry_id, occ.component, occ.byte_start, occ.byte_end)
            for occ in discovered
        }
        index_keys: Set[Tuple[str, str, int, int]] = {
            (rec.entry_id, rec.component, rec.byte_start, rec.byte_end)
            for rec in realization_index
            if rec.bundle_idx == artifacts.bundle_idx
        }
        if discovered_keys != index_keys:
            diff_extra = discovered_keys - index_keys
            diff_missing = index_keys - discovered_keys
            return {
                "valid": False,
                "error": f"Realization index disagreement: extra={diff_extra}, missing={diff_missing}",
            }

    return {"valid": True, "error": None}
