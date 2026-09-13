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

    # 1. Build article.md
    article_lines: List[str] = [
        f"# Battery Cell Performance Characterization - Test Dataset B{bundle_idx:02d}",
        "",
        "## Executive Summary",
        "This experimental report documents the electrochemical cycling, thermal behavior, and",
        "operational parameters for commercial lithium-ion test cells evaluated under laboratory validation protocols.",
        "",
        "## Overview and Experimental Specification",
        "The following parameters and conventions govern the primary test channel acquisition and analysis:",
    ]

    for entry in s_doc_prominent:
        article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    article_lines.extend([
        "## Experimental Procedure and Measurement Methodology",
        "Galvanostatic cycling was conducted using an automated multi-channel battery test system inside a temperature-controlled chamber.",
        "Voltage, current, and cell surface temperature were logged continuously throughout all charge, discharge, and rest periods.",
        "",
        "## Supplementary Appendix: Operational Details and Notes",
        "The following supplementary technical notes and low-level channel definitions apply to this deposit:",
    ])

    for entry in s_doc_buried:
        article_lines.append(f"{entry.entry_text}")
        article_lines.append("")

    article_lines.extend([
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

    # 3. Build data.csv
    csv_lines: List[str] = [
        f"# Battery Test Time-Series Acquisition Data — Dataset B{bundle_idx:02d}",
        "# System: Dual-Channel High-Precision Battery Cycler",
    ]

    for entry in s_file_prominent:
        csv_lines.append(f"{entry.entry_text}")

    csv_lines.extend([
        "time_s,current_A,voltage_V,power_W,temperature_C",
        "0.0,0.0,3.600,0.0,25.0",
        "1.0,1.5,3.650,5.475,25.1",
        "2.0,1.5,3.680,5.520,25.2",
        "3.0,1.5,3.710,5.565,25.3",
        "4.0,1.5,3.730,5.595,25.4",
        "5.0,0.0,3.725,0.0,25.3",
        "# --- Extended File Annotations ---",
    ])

    for entry in s_file_buried:
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
                realization_records.append(
                    RealizationRecord(
                        bundle_idx=bundle_idx,
                        entry_id=entry.entry_id,
                        param=entry.parameter,
                        scope=entry.scope,
                        cls_name=getattr(entry, "class", "UNKNOWN"),
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
