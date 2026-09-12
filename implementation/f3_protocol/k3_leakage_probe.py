"""
K3 Leakage Probe Implementation.
Governing specification: construction/S2_CANDIDATE_SPEC_v0.11.md (§9.3).

TASK: Predict the class of each parameter-cell (0..5)
CLASSIFIER: Multinomial Logistic Regression, L2, C=1.0, max_iter=1000 (scikit-learn)
FEATURES: Exactly 62 features
FOLDS: 5 bundle-level folds (fold = bundle_idx % 5)
PERMUTATION TEST: N = 2000, seed 20260912, unit = bundle's 11-parameter-cell class vector
STATISTIC: A_obs = mean CV multiclass accuracy over 330 held-out parameter-cells
P-VALUE: p = (1 + #{A_perm >= A_obs}) / (1 + N)
FIRES IF: p < 0.01
"""

import re
import string
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from f2_corpus.constants import PARAMETERS, NUM_BUNDLES, NUM_PARAMETERS

# §4.2 Complete 12-element scope vocabulary in frozen order
ALL_SCOPES: List[str] = [
    "current",
    "voltage",
    "power",
    "capacity_charge",
    "capacity_discharge",
    "energy",
    "temperature",
    "time",
    "step_index",
    "cycle_index",
    "test_index",
    "dataset",
]

# §9.3 20 Frozen formatting markers
MARKER_NAMES: List[str] = [
    "atx_heading",             # 1  '#'
    "setext_underline",        # 2  '==='
    "bullet_dash",             # 3  '- '
    "bullet_star",             # 4  '* '
    "numbered_list",           # 5  '1.'
    "table_pipe",              # 6  '|'
    "code_fence",              # 7  '```'
    "inline_backtick",         # 8  '`'
    "blockquote",              # 9  '>'
    "footnote_marker",         # 10 '[^'
    "year_like",               # 11 '(20'
    "bracketed_ref",           # 12 '[1]'
    "http",                    # 13 'http'
    "doi_prefix",              # 14 '10.'
    "parenthesised_unit",      # 15 e.g. '(A)', '(V)'
    "colon_label_line",        # 16 colon-terminated label line
    "all_caps_token_ge_3",     # 17 ALL-CAPS token length >= 3
    "em_dash",                 # 18 '—' or '--'
    "semicolon",               # 19 ';'
    "line_initial_hash_csv",   # 20 line-initial '#' in CSV header
]


def check_marker_presence(marker_idx: int, article_text: str, readme_text: str, csv_header_text: str) -> float:
    """Check presence (1.0 or 0.0) of each of the 20 frozen formatting markers across the whole bundle."""
    combined = article_text + "\n" + readme_text + "\n" + csv_header_text
    
    if marker_idx == 1:   # ATX heading '#'
        return 1.0 if re.search(r"^#{1,6}\s", article_text + "\n" + readme_text, re.MULTILINE) else 0.0
    elif marker_idx == 2: # setext underline '==='
        return 1.0 if "===" in combined else 0.0
    elif marker_idx == 3: # bullet '- '
        return 1.0 if re.search(r"^\s*-\s", combined, re.MULTILINE) else 0.0
    elif marker_idx == 4: # bullet '* '
        return 1.0 if re.search(r"^\s*\*\s", combined, re.MULTILINE) else 0.0
    elif marker_idx == 5: # numbered list '1.'
        return 1.0 if re.search(r"^\s*1\.\s", combined, re.MULTILINE) else 0.0
    elif marker_idx == 6: # table pipe '|'
        return 1.0 if "|" in combined else 0.0
    elif marker_idx == 7: # code fence '```'
        return 1.0 if "```" in combined else 0.0
    elif marker_idx == 8: # inline backtick
        return 1.0 if "`" in combined else 0.0
    elif marker_idx == 9: # blockquote '>'
        return 1.0 if re.search(r"^\s*>", combined, re.MULTILINE) else 0.0
    elif marker_idx == 10: # footnote marker '[^'
        return 1.0 if "[^" in combined else 0.0
    elif marker_idx == 11: # year-like '(20'
        return 1.0 if "(20" in combined else 0.0
    elif marker_idx == 12: # bracketed ref '[1]'
        return 1.0 if "[1]" in combined else 0.0
    elif marker_idx == 13: # 'http'
        return 1.0 if "http" in combined else 0.0
    elif marker_idx == 14: # DOI prefix '10.'
        return 1.0 if "10." in combined else 0.0
    elif marker_idx == 15: # parenthesised unit token
        return 1.0 if re.search(r"\([A-Za-z°%]{1,5}\)", combined) else 0.0
    elif marker_idx == 16: # colon-terminated label line
        return 1.0 if re.search(r"^[A-Za-z0-9_\s]{2,40}:\s*$", combined, re.MULTILINE) else 0.0
    elif marker_idx == 17: # ALL-CAPS token length >= 3
        return 1.0 if re.search(r"\b[A-Z]{3,}\b", combined) else 0.0
    elif marker_idx == 18: # em dash
        return 1.0 if "—" in combined else 0.0
    elif marker_idx == 19: # semicolon
        return 1.0 if ";" in combined else 0.0
    elif marker_idx == 20: # line-initial '#' in CSV header
        return 1.0 if re.search(r"^#", csv_header_text, re.MULTILINE) else 0.0
    return 0.0


def extract_component_stats(text: str) -> List[float]:
    """Extract char count, line count, digit ratio, punctuation count for a component (4 features)."""
    char_count = float(len(text))
    line_count = float(len(text.splitlines())) if text else 0.0
    digit_count = sum(c.isdigit() for c in text)
    digit_ratio = (digit_count / char_count) if char_count > 0 else 0.0
    punct_count = float(sum(c in string.punctuation for c in text))
    return [char_count, line_count, digit_ratio, punct_count]


def compute_ttr_and_mean_sent_len(text: str) -> Tuple[float, float]:
    """Compute type-token ratio and mean sentence length (whitespace, lowercased, no stemming)."""
    tokens = text.lower().split()
    if not tokens:
        return 0.0, 0.0
    ttr = len(set(tokens)) / len(tokens)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    mean_sent_len = (len(tokens) / len(sentences)) if sentences else float(len(tokens))
    return mean_sent_len, ttr


def extract_bundle_features(article_text: str, readme_text: str, csv_header_text: str) -> List[float]:
    """
    Extract 39 bundle-level features:
    - per component (article, readme, csv_header): 3 x 4 = 12 features
    - heading/section/column counts: 3 features
    - mean sentence len (article, readme): 2 features
    - type-token ratio (article, readme): 2 features
    - 20 formatting markers: 20 features
    Total: 12 + 3 + 2 + 2 + 20 = 39 features.
    """
    feats: List[float] = []
    
    # 1. Per component stats (12 features)
    feats.extend(extract_component_stats(article_text))
    feats.extend(extract_component_stats(readme_text))
    feats.extend(extract_component_stats(csv_header_text))
    
    # 2. Heading / section / column counts (3 features)
    article_headings = float(len(re.findall(r"^#{1,6}\s", article_text, re.MULTILINE)))
    readme_sections = float(len(re.findall(r"^#{1,6}\s", readme_text, re.MULTILINE)))
    # CSV columns: count delimiters (commas or tabs in first line)
    first_csv_line = csv_header_text.splitlines()[0] if csv_header_text.splitlines() else ""
    csv_col_count = float(len(first_csv_line.split(","))) if "," in first_csv_line else 1.0
    feats.extend([article_headings, readme_sections, csv_col_count])
    
    # 3. Mean sentence length and TTR for article and readme (4 features)
    art_sent_len, art_ttr = compute_ttr_and_mean_sent_len(article_text)
    rdm_sent_len, rdm_ttr = compute_ttr_and_mean_sent_len(readme_text)
    feats.extend([art_sent_len, rdm_sent_len, art_ttr, rdm_ttr])
    
    # 4. 20 formatting markers (20 features)
    for m_idx in range(1, 21):
        feats.append(check_marker_presence(m_idx, article_text, readme_text, csv_header_text))
        
    assert len(feats) == 39
    return feats


def extract_62_features(
    bundle_features_39: List[float],
    param_id: str,
    scope_id: str,
) -> List[float]:
    """
    Combine 39 bundle features with 23 parameter-cell features:
    - parameter ID one-hot: 11
    - scope ID one-hot: 12
    Total: 39 + 11 + 12 = 62 features.
    """
    # Parameter one-hot (11)
    param_one_hot = [1.0 if p == param_id else 0.0 for p in PARAMETERS]
    # Scope one-hot (12)
    scope_one_hot = [1.0 if s == scope_id else 0.0 for s in ALL_SCOPES]
    
    full_feats = list(bundle_features_39) + param_one_hot + scope_one_hot
    assert len(full_feats) == 62
    return full_feats


def run_k3_leakage_probe(
    X: np.ndarray,  # shape (330, 62)
    y: np.ndarray,  # shape (330,) integer classes 0..5
    n_permutations: int = 2000,
    seed: int = 20260912,
) -> Dict[str, Any]:
    """
    Execute §9.3 K3 permutation test:
    - 5 bundle-level folds: bundle_idx % 5.
    - Standardize on train folds only.
    - Multinomial Logistic Regression, L2, C=1.0, max_iter=1000.
    - Observed accuracy A_obs.
    - N = 2000 permutations of bundle-level 11-cell class vectors.
    - p = (1 + #{A_perm >= A_obs}) / (1 + N).
    - Fires if p < 0.01.
    """
    rng = np.random.RandomState(seed)
    num_cells = len(y)
    assert num_cells == 330
    assert X.shape == (330, 62)
    
    # Fold assignments for 330 cells: cell index i // 11 is bundle_idx
    bundle_indices = np.array([idx // NUM_PARAMETERS for idx in range(num_cells)])
    folds = bundle_indices % 5

    def eval_cv(target_y: np.ndarray) -> float:
        correct = 0
        for f in range(5):
            train_mask = (folds != f)
            test_mask = (folds == f)

            X_train, y_train = X[train_mask], target_y[train_mask]
            X_test, y_test = X[test_mask], target_y[test_mask]

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            clf = LogisticRegression(
                penalty="l2",
                C=1.0,
                multi_class="multinomial",
                solver="lbfgs",
                max_iter=1000,
                random_state=seed,
            )
            clf.fit(X_train_scaled, y_train)
            preds = clf.predict(X_test_scaled)
            correct += np.sum(preds == y_test)
        return float(correct) / float(num_cells)

    # Observed accuracy
    a_obs = eval_cv(y)

    # Permutations: unit = bundle's whole 11-parameter-cell class vector (shape (30, 11))
    y_bundles = y.reshape((NUM_BUNDLES, NUM_PARAMETERS))
    ge_count = 0

    for _ in range(n_permutations):
        # Permute bundles
        perm_bundle_order = rng.permutation(NUM_BUNDLES)
        perm_y = y_bundles[perm_bundle_order].reshape(num_cells)
        a_perm = eval_cv(perm_y)
        if a_perm >= a_obs:
            ge_count += 1

    p_value = (1.0 + float(ge_count)) / (1.0 + float(n_permutations))
    fires = (p_value < 0.01)

    return {
        "A_obs": a_obs,
        "null_acc": 1.0 / 6.0,
        "n_permutations": n_permutations,
        "ge_count": ge_count,
        "p_value": p_value,
        "fires": fires,
        "verdict": "K3_TRIGGERED_LEAKAGE_DETECTED" if fires else "K3_PASSED_NO_LEAKAGE_DETECTED",
    }
