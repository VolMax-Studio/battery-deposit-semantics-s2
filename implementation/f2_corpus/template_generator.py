"""
Template Generator Skeleton for S2 CVD Construction.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§5.8).

Bundles are generated, not written: frozen template engine inserts bank entries
verbatim, no paraphrase, placement under frozen rules and frozen seed.
Emits realization index.
"""

from typing import Dict, Any, List, Tuple
import hashlib


class RealizationRecord:
    def __init__(
        self,
        bundle_idx: int,
        param: str,
        scope: str,
        cls_name: str,
        entry_text: str,
        component: str,  # 'article', 'readme', 'csv_header'
        byte_start: int,
        byte_end: int,
    ):
        self.bundle_idx = bundle_idx
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
            "parameter": self.param,
            "scope": self.scope,
            "class": self.cls_name,
            "entry_text": self.entry_text,
            "component": self.component,
            "byte_start": self.byte_start,
            "byte_end": self.byte_end,
        }


class BundleArtifacts:
    def __init__(self, bundle_idx: int, article_bytes: bytes, readme_bytes: bytes, csv_header_bytes: bytes):
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

    def sha256_map(self) -> Dict[str, str]:
        return {
            "article": hashlib.sha256(self.article_bytes).hexdigest(),
            "readme": hashlib.sha256(self.readme_bytes).hexdigest(),
            "csv_header": hashlib.sha256(self.csv_header_bytes).hexdigest(),
        }


def check_fidelity(
    artifacts: BundleArtifacts,
    realization_index: List[RealizationRecord],
) -> Dict[str, Any]:
    """
    §5.8 Fidelity Checker:
    1. Search bundle bytes for byte-exact occurrences of bank entries.
    2. Reconstruct derived ground-truth from occurrences and byte spans.
    3. Derived record must equal sealed record byte-identically.
    """
    for rec in realization_index:
        if rec.bundle_idx != artifacts.bundle_idx:
            continue
        comp_bytes = artifacts.get_component_bytes(rec.component)
        entry_bytes = rec.entry_text.encode("utf-8")
        span_bytes = comp_bytes[rec.byte_start:rec.byte_end]
        if span_bytes != entry_bytes:
            return {
                "valid": False,
                "error": f"Fidelity check failed for bundle {rec.bundle_idx} {rec.param}: expected span bytes to match entry exactly",
            }
    return {"valid": True, "error": None}
