"""
Deterministic CVD Bundle Generator for S2 Qualification.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.1, §5.2, §5.8, §11).

Implements frozen placement rules across 30 bundles:
- Mechanically invertible prominent vs buried regions:
  * article.md: '## Overview and Experimental Specification' (prominent) vs
                '## Supplementary Appendix: Operational Details and Notes' (buried)
  * README.md:  '## Primary Metadata and File Inventory' (prominent) vs
                '## Supplemental Archive Notes' (buried)
  * data.csv:   Header comments block (prominent) vs
                '# --- Extended File Annotations ---' (buried)
- Natural scientific document formatting with zero adjudicator class-bearing markers.
- Emits BundleArtifacts, bundle_manifest, and realization_index.
"""

import os
import json
from typing import Dict, Any, List, Tuple, Optional

from .constants import (
    PARAMETERS,
    NUM_BUNDLES,
)
from .template_generator import (
    BankEntry,
    BundleArtifacts,
    RealizationRecord,
    reconstruct_derived_ground_truth,
    serialize_ground_truth_canonically,
    get_placement_in_component,
)


def load_bank_from_jsonl(bank_path: str) -> List[BankEntry]:
    """Load BankEntry objects from a JSONL bank file."""
    entries: List[BankEntry] = []
    with open(bank_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            entries.append(
                BankEntry(
                    entry_id=data["entry_id"],
                    parameter=data["parameter"],
                    scope=data["scope"],
                    evidence_stratum=data["evidence_stratum"],
                    semantic_role=data["semantic_role"],
                    semantic_value=data.get("semantic_value"),
                    entry_text=data["entry_text"],
                    exclusive_assertion=data.get("exclusive_assertion", False),
                )
            )
    return entries


def generate_single_bundle(
    bundle_idx: int,
    bundle_entries: List[BankEntry],
    scope_table: Dict[str, Any],
) -> Tuple[BundleArtifacts, Dict[str, Any], List[RealizationRecord]]:
    """
    Generate bundle artifacts (article, readme, csv_header), manifest, and realization index
    for a single bundle index.
    """
    realization_records: List[RealizationRecord] = []

    # Segregate entries by stratum and class placement
    # S-DOC entries go to article.md
    s_doc_prominent: List[BankEntry] = []
    s_doc_buried: List[BankEntry] = []

    # S-FILE entries go to data.csv
    s_file_prominent: List[BankEntry] = []
    s_file_buried: List[BankEntry] = []

    for entry in bundle_entries:
        # Determine target placement from class
        # POS-BURIED is placed in the buried region; all others in prominent region
        is_buried = (entry.entry_id.endswith("-DET") and "BURIED" in entry.entry_id) or ("BURIED" in getattr(entry, "class", ""))
        # To be robust, check entry ID pattern or class
        # In F5 bank, entries have class in data or ID: e.g. F5-E1-B01-DET where B01 is POS-BURIED
        # Let's inspect entry:
        if getattr(entry, "target_class", None) == "POS-BURIED" or "BURIED" in getattr(entry, "class", ""):
            is_buried = True

        if entry.evidence_stratum == "S-DOC":
            if is_buried:
                s_doc_buried.append(entry)
            else:
                s_doc_prominent.append(entry)
        else:  # S-FILE
            if is_buried:
                s_file_buried.append(entry)
            else:
                s_file_prominent.append(entry)

    # 1. Build article.md with multi-structural XOR realization (§5)
    # Section depth (## level 2 vs ### level 3) x Ordinal position (early block vs late block)
    # (shallow + early) -> prominent, (shallow + late) -> buried
    # (deep + early) -> buried, (deep + late) -> prominent
    article_lines: List[str] = [
        f"# Battery Cell Performance Characterization - Test Dataset B{bundle_idx:02d}",
        "",
        "## 1. Operating Specifications and Protocol",
        "This experimental report documents the electrochemical cycling, thermal behavior, and",
        "operational parameters for commercial lithium-ion test cells evaluated under laboratory validation protocols.",
        "",
    ]

    # Half of prominent go to (shallow, early)
    doc_prom_1 = s_doc_prominent[:len(s_doc_prominent)//2 + 1]
    doc_prom_2 = s_doc_prominent[len(s_doc_prominent)//2 + 1:]

    # Half of buried go to (shallow, late)
    doc_bur_1 = s_doc_buried[:len(s_doc_buried)//2 + 1]
    doc_bur_2 = s_doc_buried[len(s_doc_buried)//2 + 1:]

    # Shallow + Early: block 2 (block <= 2 -> prominent)
    # Emit all doc_prom_1 entries in one paragraph block
    if doc_prom_1:
        for entry in doc_prom_1:
            article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    # Spacer block to transition to late: block 3 (block >= 3)
    article_lines.append("Baseline environmental chamber temperature was maintained at 25.0 C across all test runs.")
    article_lines.append("")

    # Shallow + Late: block 4+ (block >= 3 -> buried)
    if doc_bur_1:
        for entry in doc_bur_1:
            article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    # Subsection: ### 1.1 Detailed Instrumentation & Channel Mapping (level 3 -> deep)
    article_lines.extend([
        "### 1.1 Detailed Instrumentation and Channel Mapping",
        "Galvanostatic cycling was conducted using an automated multi-channel battery test system.",
        "",
    ])

    # Deep + Early: block 2 (block <= 2 -> buried)
    if doc_bur_2:
        for entry in doc_bur_2:
            article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    # Spacer block to transition to late: block 3 (block >= 3)
    article_lines.extend([
        "Channel voltages were calibrated against secondary standards prior to dataset acquisition.",
        "",
    ])

    # Deep + Late: block 4+ (block >= 3 -> prominent)
    if doc_prom_2:
        for entry in doc_prom_2:
            article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    article_lines.extend([
        "## 2. Archival Summary and End of Report",
        f"Validation dataset B{bundle_idx:02d} concluded without hardware interrupt flags.",
        "",
        "---",
        f"End of Report B{bundle_idx:02d}.",
        "",
    ])

    article_text = "\n".join(article_lines)
    article_bytes = article_text.encode("utf-8")

    # 2. Build README.md
    readme_lines: List[str] = [
        f"# README - Battery Dataset B{bundle_idx:02d}",
        "",
        "## Primary Metadata and File Inventory",
        "This deposit contains the following components:",
        "- `article.md`: Technical report and measurement specification.",
        "- `README.md`: Deposit metadata and archival file inventory.",
        "- `data.csv`: Time-series acquisition records.",
        "",
        "## Supplemental Archive Notes",
        "Archival packaging generated under Protocol P10 CVD qualification standards.",
        f"Deposit identifier: B{bundle_idx:02d}",
        "",
    ]
    readme_text = "\n".join(readme_lines)
    readme_bytes = readme_text.encode("utf-8")

    # 3. Build data.csv with multi-structural XOR realization (§5)
    # Shallow region (before time_s):
    #   comment_block_idx = 1: Title (shallow + early)
    #   comment_block_idx = 2: Shallow + early capacity = EXACTLY 1 line -> prominent
    #   comment_block_idx >= 3: Shallow + late -> buried
    # Deep region (after time_s):
    #   comment_block_idx = 1: Deep + early (idx <= 2) -> buried
    #   comment_block_idx = 2: Deep + early (idx <= 2) capacity = EXACTLY 1 bank entry -> buried
    #   comment_block_idx = 3: Spacer comment to transition to late
    #   comment_block_idx >= 4: Deep + late (idx >= 3) -> prominent
    #
    # Distribute entries according to mechanical capacity:
    # Prominent S-FILE entries:
    #   Entry 0 -> shallow early (comment_block_idx = 2)
    #   Entries 1+ -> deep late (comment_block_idx >= 4)
    file_prom_shallow_early = s_file_prominent[:1]
    file_prom_deep_late = s_file_prominent[1:]

    # Buried S-FILE entries:
    #   Entry 0 -> deep early (comment_block_idx = 2 in trailer)
    #   Entries 1+ -> shallow late (comment_block_idx >= 3 in header)
    file_bur_deep_early = s_file_buried[:1]
    file_bur_shallow_late = s_file_buried[1:]

    # Line 1: Header line (comment_block_idx = 1)
    csv_lines: List[str] = [
        f"# Battery Test Time-Series Acquisition Data — Dataset B{bundle_idx:02d}",
    ]

    # Line 2: Shallow + Early (comment_block_idx = 2 -> prominent)
    for entry in file_prom_shallow_early:
        csv_lines.append(f"{entry.entry_text}")

    # Line 3+: Spacer comment to transition to late (comment_block_idx = 3 if file_prom_shallow_early else 2)
    csv_lines.append("# System: Dual-Channel High-Precision Battery Cycler")

    # Shallow + Late (comment_block_idx >= 3 -> buried)
    for entry in file_bur_shallow_late:
        csv_lines.append(f"{entry.entry_text}")

    csv_lines.extend([
        "time_s,current_A,voltage_V,power_W,temperature_C",
        "0.0,0.0,3.600,0.0,25.0",
        "1.0,1.5,3.650,5.475,25.1",
        "2.0,1.5,3.680,5.520,25.2",
        "3.0,1.5,3.710,5.565,25.3",
        "4.0,1.5,3.730,5.595,25.4",
        "5.0,0.0,3.725,0.0,25.3",
    ])

    # Trailer comments (deep): early (idx <= 2) -> buried; late (idx >= 3) -> prominent
    # Trailer line 1 (idx = 1):
    csv_lines.append("# Post-Run Operational Verification Log")
    # Trailer line 2 (idx = 2): Deep + Early -> buried
    for entry in file_bur_deep_early:
        csv_lines.append(f"{entry.entry_text}")

    # Trailer line 3+ (idx >= 3): Spacer comment to transition to late -> prominent
    csv_lines.append("# Acquisition log reconciliation completed.")
    for entry in file_prom_deep_late:
        csv_lines.append(f"{entry.entry_text}")

    csv_lines.append("")
    csv_text = "\n".join(csv_lines)
    csv_bytes = csv_text.encode("utf-8")


    artifacts = BundleArtifacts(
        bundle_idx=bundle_idx,
        article_bytes=article_bytes,
        readme_bytes=readme_bytes,
        csv_header_bytes=csv_bytes,
    )

    # Compute exact realization records by locating byte spans in the generated artifacts
    for entry in bundle_entries:
        target_bytes = entry.entry_text.encode("utf-8")
        found = False
        for comp_name, comp_bytes in artifacts.components():
            pos = comp_bytes.find(target_bytes)
            if pos != -1:
                # Fail-fast generation assertion (§5):
                # Verify that no entry silently spills across its intended structural placement boundary
                entry_cls = getattr(entry, "class", "UNKNOWN")
                if entry_cls in ("POS-EXPLICIT", "POS-BURIED"):
                    expected_placement = "buried" if entry_cls == "POS-BURIED" else "prominent"
                    actual_placement = get_placement_in_component(comp_name, pos, comp_bytes)
                    if actual_placement != expected_placement:
                        raise AssertionError(
                            f"Bundle {bundle_idx}: Entry {entry.entry_id} (class {entry_cls}) "
                            f"placed at byte {pos} in {comp_name} mechanically derived as '{actual_placement}', "
                            f"expected '{expected_placement}'. Region capacity boundary violated!"
                        )

                realization_records.append(
                    RealizationRecord(
                        bundle_idx=bundle_idx,
                        entry_id=entry.entry_id,
                        param=entry.parameter,
                        scope=entry.scope,
                        cls_name=entry_cls,
                        entry_text=entry.entry_text,
                        component=comp_name,
                        byte_start=pos,
                        byte_end=pos + len(target_bytes),
                    )
                )
                found = True
                break
        if not found:
            raise ValueError(f"Bundle {bundle_idx}: entry {entry.entry_id} not found in generated bundle bytes!")

    # Sort realization records by (component, byte_start)
    realization_records.sort(key=lambda r: (r.component, r.byte_start))

    # Manifest satisfying §4.3 and §5.8 item 6
    manifest = {
        "bundle_idx": bundle_idx,
        "e3_structure": {
            "num_tests": 2,
            "cycles_per_test": [2, 1],
            "steps_per_cycle": [3, 1, 1],
        },
        "interval_duration_seconds": 1.0,
    }

    return artifacts, manifest, realization_records


def generate_all_corpus_bundles(
    bank_path: str,
    scope_table_path: str,
) -> List[Tuple[BundleArtifacts, Dict[str, Any], List[RealizationRecord]]]:
    """
    Generate all 30 bundles for the complete CVD corpus.
    """
    bank_entries = load_bank_from_jsonl(bank_path)

    with open(scope_table_path, "r", encoding="utf-8") as f:
        scope_table = json.load(f)

    # Index bank entries by bundle_idx
    # In F5 bank, bank entry lines contain "bundle_idx"
    entries_by_bundle: Dict[int, List[BankEntry]] = {i: [] for i in range(NUM_BUNDLES)}

    with open(bank_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            raw = json.loads(line)
            b_idx = raw["bundle_idx"]
            entry = BankEntry(
                entry_id=raw["entry_id"],
                parameter=raw["parameter"],
                scope=raw["scope"],
                evidence_stratum=raw["evidence_stratum"],
                semantic_role=raw["semantic_role"],
                semantic_value=raw.get("semantic_value"),
                entry_text=raw["entry_text"],
                exclusive_assertion=raw.get("exclusive_assertion", False),
            )
            # Attach class attribute from bank
            entry.class_name = raw["class"]
            setattr(entry, "class", raw["class"])
            entries_by_bundle[b_idx].append(entry)

    results = []
    for i in range(NUM_BUNDLES):
        artifacts, manifest, records = generate_single_bundle(
            bundle_idx=i,
            bundle_entries=entries_by_bundle[i],
            scope_table=scope_table,
        )
        results.append((artifacts, manifest, records))

    return results


if __name__ == "__main__":
    import sys
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    bank_p = os.path.join(base_dir, "corpus", "f5_bank", "F5_BANK_ATTEMPT_03.jsonl")
    scope_p = os.path.join(base_dir, "implementation", "f2_corpus", "frozen_scope_table.json")
    print(f"Generating all 30 bundles from {bank_p}...")
    corpus = generate_all_corpus_bundles(bank_p, scope_p)
    print(f"Generated {len(corpus)} bundles successfully.")
    total_records = sum(len(records) for _, _, records in corpus)
    print(f"Total realization records: {total_records} / 330 bank entries placed.")
