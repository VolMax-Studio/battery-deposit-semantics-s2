# F4 Substitution 003 — Model Availability Correction 001

**Instance:** `battery-deposit-semantics-s2`  
**Role:** Party 3 — Bank Validator  
**Party:** `MISTRAL-CLEAN-P3-01`  
**Status:** ACCEPTED ON OPERATOR COMMIT  

`F4_ROLE_SUBSTITUTION_003.md` recorded the intended execution model as:
`mistral-large-2512`

Before any protected F6 exposure, account-level model availability was checked. That model was unavailable to the executing account.

No F6 blind input was submitted under `mistral-large-2512`. No Party-3 output was produced under that model.

The execution model is therefore pinned prospectively as:
`mistral-medium-2604`

This correction changes only the executable model identifier for Party 3. It does not change the Party-3 role, frozen §5.4 back-translation protocol, semantic fields, bank-loop rules, thresholds, F5 artifact, or methodology.

Fallback models are NOT authorized after protected execution begins without an additional disclosed execution decision.

`F4_SUB003_MODEL_AVAILABILITY_CORRECTION_001 = ACCEPTED ON OPERATOR COMMIT`
