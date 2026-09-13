# F6 Replacement Request Round 03 — Party 2 (Grok Authoring) [FINAL ATTEMPT]

**Role:** Party 2 Bank Author (`GROK-CLEAN-P2-01`)
**Task:** Final Exact-Slot Replacement for exactly 16 rejected Attempt-02 entries.
**Protocol Reference:** P10 Strict Boundary & Layer Separation v1.0.1 (§5.6)
**Warning:** This is the 3rd and final permitted attempt for these 16 slots. If any slot fails, Bank Integrity cannot be established.

## CRITICAL FINAL-ATTEMPT RULES (§5.6)
1. **DO NOT INFER, IMPROVE, SUBSTITUTE, OR CHOOSE `semantic_value`:**
   The supplied frozen `semantic_value` in each target slot is 100% authoritative.
   Your only task is to write `entry_text` that expresses EXACTLY that supplied `semantic_value`, scope, role, stratum, and exclusivity.
   If `previous_rejected_text` contains a different apparent value, IGNORE IT. The frozen metadata in the target object governs.

2. **STRICT FORMATTING BY STRATUM:**
   - **For `S-FILE` targets:**
     * Use terse, machine-readable in-file artifact / header syntax (e.g. `# <key>=<value>; exclusive=true`).
     * NO explanatory natural language prose or conversational sentences.
     * NO README / documentation wording.
     * Explicitly name the scope and governed semantic.
     * When `exclusive_assertion=true`, include an explicit machine exclusivity marker (e.g. `; exclusive=true; alternatives=none`).
   - **For `S-DOC` targets:**
     * Use descriptive natural language documentation / README / protocol prose.

3. **RETURN FORMAT:**
   Return a single JSON array of exactly 16 objects containing only `entry_id` and `entry_text`:
   ```json
   [
     {"entry_id": "F5-E5-B29-AMB2", "entry_text": "..."},
     ...
   ]
   ```

## 16 Target Frozen Slots (Direct from F5 Bank Attempt 02 & Comparator):
```json
[
  {
    "entry_id": "F5-E5-B29-AMB2",
    "parameter": "E5",
    "scope": "current",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "event_driven(delta_voltage)"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# sampling_policy_current: fixed(5 s) ONLY — exclusive sole sampling rule; no other trigger permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "event_driven(delta_voltage)"
        ],
        "actual": [
          "fixed(5 s)"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E6-B10-AMB2",
    "parameter": "E6",
    "scope": "voltage",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "gap_flag_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# completeness_check_voltage: completeness_counter ONLY — exclusive sole verification method; no other method permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "gap_flag_column"
        ],
        "actual": [
          "completeness_counter"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E4b-B07-NA",
    "parameter": "E4b",
    "scope": "power",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "Interval bound-inclusivity semantics do not apply to the power signal because this deposit records power only as discrete point samples without any interval structure.",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E7a-B09-AMB2",
    "parameter": "E7a",
    "scope": "step_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "filename_encoding"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# index_recovery_step_index: time_segmentation_rule ONLY — exclusive sole recovery method; nothing else permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "filename_encoding"
        ],
        "actual": [
          "time_segmentation_rule"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E7a-B27-AMB2",
    "parameter": "E7a",
    "scope": "step_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "filename_encoding"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# index_recovery_step_index: row_grouping_marker ONLY — exclusive sole recovery method; nothing else allowed",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "filename_encoding"
        ],
        "actual": [
          "row_grouping_marker"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E7b-B08-AMB2",
    "parameter": "E7b",
    "scope": "dataset",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "current_sign"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# state_encoding_dataset: step_type_column ONLY — exclusive and complete; no other state method permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "current_sign"
        ],
        "actual": [
          "step_type_column"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E7a-B15-AMB2",
    "parameter": "E7a",
    "scope": "cycle_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "filename_encoding"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# index_recovery_cycle_index: explicit_index_column ONLY — exclusive and complete; no other recovery method allowed",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "filename_encoding"
        ],
        "actual": [
          "explicit_index_column"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E6-B22-AMB2",
    "parameter": "E6",
    "scope": "temperature",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "gap_flag_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# completeness_check_temperature: gap_flag_column ONLY — exclusive and complete verification method",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E6-B04-AMB2",
    "parameter": "E6",
    "scope": "current",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "gap_flag_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# completeness_check_current: completeness_counter ONLY — exclusive sole verification method; no other method permitted",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      },
      "semantic_value": {
        "expected": [
          "gap_flag_column"
        ],
        "actual": [
          "completeness_counter"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E6-B28-AMB2",
    "parameter": "E6",
    "scope": "current",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "gap_flag_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# completeness_check_current: gap_flag_column ONLY — exclusive sole method; no other completeness check permitted",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E7b-B14-AMB2",
    "parameter": "E7b",
    "scope": "dataset",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "current_sign"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# state_encoding_dataset: current_sign ONLY — exclusive and complete; no other method permitted",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E7b-B02-AMB2",
    "parameter": "E7b",
    "scope": "dataset",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "current_sign"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# state_encoding_dataset: step_type_column ONLY — exclusive and complete; no other state-encoding method allowed",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      },
      "semantic_value": {
        "expected": [
          "current_sign"
        ],
        "actual": [
          "step_type_column"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E5-B17-AMB2",
    "parameter": "E5",
    "scope": "power",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "event_driven(delta_voltage)"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# sampling_policy_power: event_driven(delta_voltage) ONLY — exclusive and complete; no other trigger allowed",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E5-B23-AMB2",
    "parameter": "E5",
    "scope": "temperature",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "event_driven(delta_voltage)"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# sampling_policy_temperature: event_driven(delta_voltage) ONLY — exclusive and complete; no other trigger permitted",
    "observed_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-FILE",
        "actual": "S-DOC"
      }
    }
  },
  {
    "entry_id": "F5-E7a-B03-AMB2",
    "parameter": "E7a",
    "scope": "test_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "filename_encoding"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# index_recovery_test_index: explicit_index_column ONLY — exclusive sole method; no other recovery permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "filename_encoding"
        ],
        "actual": [
          "explicit_index_column"
        ]
      }
    }
  },
  {
    "entry_id": "F5-E6-B16-AMB2",
    "parameter": "E6",
    "scope": "power",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "gap_flag_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "# completeness_check_power: acquisition_log_reconciliation ONLY — exclusive sole method; no other verification permitted",
    "observed_comparator_mismatch": {
      "semantic_value": {
        "expected": [
          "gap_flag_column"
        ],
        "actual": [
          "acquisition_log_reconciliation"
        ]
      }
    }
  }
]
```

