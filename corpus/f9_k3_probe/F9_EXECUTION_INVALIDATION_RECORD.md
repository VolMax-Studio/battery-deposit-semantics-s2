# Stage F9 Execution Invalidation Record

- **Instance:** `battery-deposit-semantics-s2`
- **Stage:** F9 K3 Formatting & Structural Leakage Probe
- **Date:** 2026-09-13
- **Action:** Formal Invalidation of Preliminary Execution

---

## 1. Adversarial Review Finding

- **Issuing Party:** Party 1 (Constructor / Adversarial Reviewer — Fable / Claude)
- **Finding Identifier:** `PARTY_1_F9_ADVERSARIAL_REVIEW: BLOCKING EXECUTION DEFECT — WRAPPER SUPPLIED EMPTY BUNDLE TEXT`
- **Defect Mechanism:** The external wrapper `run_stage_f9_k3.py` queried bundle JSON files for dictionary keys `article`, `readme`, `csv_header`, whereas the actual generated bundle artifacts on disk use filename keys `article.md`, `README.md`, `data.csv`. Consequently, all three components defaulted to empty strings (`""`), resulting in identical constant values across all 39 bundle-level features for all 330 cells.
- **Proof of Defect:** Party 1 reproduced the identical reported result (`A_obs = 0.154545`, `ge_count = 18/2000`, `p = 0.009495`) by running the probe with empty component strings.
- **Disposition:** The preliminary run did not execute the frozen §9.3 procedure over the prescribed bundle bytes. The observed result is declared **VOID and NON-VERDICT-BEARING**.

---

## 2. Invalidation & Non-Shopping Adjudication

- **Integrity Rule:** Voiding an execution caused by an objective failure to feed the prescribed input bytes does not constitute seed-shopping or hyperparameter search.
- **Exposure Disclosure:** Prior to the authoritative execution, Party 1 disclosed that an auxiliary run on authentic bundle text in an unpinned environment (scikit-learn 1.8) yielded an indicative trigger (`A_obs ≈ 0.1848, ge_count = 0, p ≈ 0.0005`).
- **Remediation:** The wrapper is corrected to query `article.md`, `README.md`, and `data.csv` with strict assertions enforcing non-empty, fully populated component text (`len > 100` / `len > 500`).

---

## 3. Status

- Preliminary run: **INVALIDATED / VOID**
- Authoritative first execution: **AUTHORIZED WITH REPAIRED BUNDLE LOADER**
