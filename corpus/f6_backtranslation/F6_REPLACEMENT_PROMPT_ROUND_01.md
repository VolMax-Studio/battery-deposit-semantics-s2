# F6 Replacement Request Round 01 — Party 2 (Grok Authoring)

**Role:** Party 2 Bank Author (`GROK-CLEAN-P2-01`)
**Task:** Exact-Slot Replacement for 37 rejected Attempt-01 entries.
**Protocol Reference:** P10 Strict Boundary & Layer Separation v1.0.1 (§5.6)

## Rules (§5.6 Exact-Slot Replacement)
1. **FROZEN METADATA:** Every slot specification is FROZEN byte-for-byte from the F5 bank attempt 01.
   Do NOT alter `parameter`, `scope`, `class`, `evidence_stratum`, `semantic_role`, `semantic_value`, or `exclusive_assertion`.
2. **REWRITE ONLY `entry_text`:** You must change ONLY the text of the entry.
3. **CLARITY & DISAMBIGUATION:** The new text must clearly express the frozen semantic fields so that Party 3 cannot misclassify them.
   - For `evidence_stratum: S-FILE`: must look like an in-file artifact, comment, or header (e.g. `# ...` or `COL_NOTE: ...`).
   - For `evidence_stratum: S-DOC`: must read like natural language documentation, protocol sheet, or README text.
   - For `exclusive_assertion: true`: the text MUST explicitly and emphatically state that this set is exclusive, complete, and the ONLY one permitted/used.
   - For `semantic_role: non_determining_adjacent`: the text must mention the parameter/signal but explicitly leave it unspecified, pending, or unconfirmed.
   - For `semantic_role: non_applicable`: the text must clearly declare that the governed question does not apply.
   - For `semantic_role: determining`: the text must unambiguously convey the exact `semantic_value`.

## Response Format
Return a single JSON array of exactly 37 objects containing only `entry_id` and `entry_text`:
```json
[
  {"entry_id": "F5-E3-B09-NA", "entry_text": "..."},
  ...
]
```

## 37 Target Frozen Slots (Direct from F5 Bank & Comparator):
```json
[
  {
    "entry_id": "F5-E3-B09-NA",
    "parameter": "E3",
    "scope": "energy",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "header: energy_absent",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E3",
        "actual": "E8a"
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
    "previous_rejected_text": "COL_NOTE: dataset current_sign",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E4b-B27-DET",
    "parameter": "E4b",
    "scope": "voltage",
    "class": "POS-BURIED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": "open_open",
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: voltage (start, end)",
    "actual_comparator_mismatch": {
      "semantic_value": {
        "expected": "open_open",
        "actual": "closed_closed"
      }
    }
  },
  {
    "entry_id": "F5-E4b-B23-ADJ",
    "parameter": "E4b",
    "scope": "power",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "meta.power_bounds = TBD",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E4b",
        "actual": "E8b"
      }
    }
  },
  {
    "entry_id": "F5-E7a-B21-AMB2",
    "parameter": "E7a",
    "scope": "test_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "filename_encoding"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "legend: test index recovery = filename_encoding",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "header: temperature_complete=gap_flag_column",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E8a-B06-ADJ",
    "parameter": "E8a",
    "scope": "current",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-DOC",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "A unit field is present for current but the actual unit token is left blank.",
    "actual_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-DOC",
        "actual": "S-FILE"
      }
    }
  },
  {
    "entry_id": "F5-E5-B11-AMB2",
    "parameter": "E5",
    "scope": "voltage",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "event_driven(delta_voltage)"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "header: voltage_sample=event_driven(delta_voltage)",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "header: power_sample=event_driven(delta_voltage)",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "meta.current_completeness = gap_flag_column",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "header: step_index_via=filename_encoding",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "header: cycle_index_via=filename_encoding",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E1-B29-NA",
    "parameter": "E1",
    "scope": "power",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "COL_NOTE: polarity N/A",
    "actual_comparator_mismatch": {
      "scope": {
        "expected": "power",
        "actual": "current"
      }
    }
  },
  {
    "entry_id": "F5-E8b-B13-NA",
    "parameter": "E8b",
    "scope": "capacity_charge",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: no charge capacity channel",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E8b",
        "actual": "E3"
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
    "previous_rejected_text": "header: current_complete=gap_flag_column",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E1-B17-NA",
    "parameter": "E1",
    "scope": "power",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: no current/power channel",
    "actual_comparator_mismatch": {
      "scope": {
        "expected": "power",
        "actual": "current"
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
    "previous_rejected_text": "meta.dataset_state = current_sign",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E4b-B17-ADJ",
    "parameter": "E4b",
    "scope": "voltage",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: voltage bounds open",
    "actual_comparator_mismatch": {
      "semantic_role": {
        "expected": "non_determining_adjacent",
        "actual": "determining"
      },
      "semantic_value": {
        "expected": null,
        "actual": "open_open"
      }
    }
  },
  {
    "entry_id": "F5-E1-B05-NA",
    "parameter": "E1",
    "scope": "power",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "# polarity: N/A (no directed channel)",
    "actual_comparator_mismatch": {
      "scope": {
        "expected": "power",
        "actual": "current"
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
    "previous_rejected_text": "header: power_no_bounds",
    "actual_comparator_mismatch": {
      "semantic_role": {
        "expected": "non_applicable",
        "actual": "non_determining_adjacent"
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
    "previous_rejected_text": "header: test_index_via=filename_encoding",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E7a-B15-AMB1",
    "parameter": "E7a",
    "scope": "cycle_index",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-DOC",
    "semantic_role": "determining",
    "semantic_value": [
      "explicit_index_column"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "The cycle index is recovered from the deposit via exclusively: explicit_index_column.",
    "actual_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-DOC",
        "actual": "S-FILE"
      }
    }
  },
  {
    "entry_id": "F5-E4b-B09-DET",
    "parameter": "E4b",
    "scope": "power",
    "class": "POS-BURIED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": "open_open",
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: power (start, end)",
    "actual_comparator_mismatch": {
      "semantic_value": {
        "expected": "open_open",
        "actual": "closed_closed"
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
    "previous_rejected_text": "meta.step_index_recovery = filename_encoding",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E4b-B06-AMB2",
    "parameter": "E4b",
    "scope": "voltage",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": "open_open",
    "exclusive_assertion": false,
    "previous_rejected_text": "header: voltage_oo",
    "actual_comparator_mismatch": {
      "semantic_role": {
        "expected": "determining",
        "actual": "non_determining_adjacent"
      },
      "semantic_value": {
        "expected": "open_open",
        "actual": null
      }
    }
  },
  {
    "entry_id": "F5-E3-B25-ADJ",
    "parameter": "E3",
    "scope": "time",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "COL_NOTE: time boundary open",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E3",
        "actual": "E4b"
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
    "previous_rejected_text": "header: power_complete=gap_flag_column",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E5-B05-AMB2",
    "parameter": "E5",
    "scope": "current",
    "class": "AMBIG-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "determining",
    "semantic_value": [
      "event_driven(delta_voltage)"
    ],
    "exclusive_assertion": true,
    "previous_rejected_text": "header: current_sample=event_driven(delta_voltage)",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E3-B15-NA",
    "parameter": "E3",
    "scope": "time",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "legend: no time counter",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E3",
        "actual": "E6"
      },
      "semantic_role": {
        "expected": "non_applicable",
        "actual": "non_determining_adjacent"
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
    "previous_rejected_text": "header: temperature_sample=event_driven(delta_voltage)",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
  {
    "entry_id": "F5-E6-B27-ADJ",
    "parameter": "E6",
    "scope": "temperature",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "COL_NOTE: temperature check open",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E6",
        "actual": "E4b"
      }
    }
  },
  {
    "entry_id": "F5-E8b-B07-NA",
    "parameter": "E8b",
    "scope": "power",
    "class": "NA-CONSTRUCTED",
    "evidence_stratum": "S-FILE",
    "semantic_role": "non_applicable",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "header: power_absent",
    "actual_comparator_mismatch": {
      "parameter": {
        "expected": "E8b",
        "actual": "E2"
      }
    }
  },
  {
    "entry_id": "F5-E2-B02-ADJ",
    "parameter": "E2",
    "scope": "temperature",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-DOC",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "A field description for the temperature appears in the header metadata but does not indicate whether the values are measured or placeholder.",
    "actual_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-DOC",
        "actual": "S-FILE"
      }
    }
  },
  {
    "entry_id": "F5-E8a-B00-ADJ",
    "parameter": "E8a",
    "scope": "current",
    "class": "NEG-ADJACENT",
    "evidence_stratum": "S-DOC",
    "semantic_role": "non_determining_adjacent",
    "semantic_value": null,
    "exclusive_assertion": false,
    "previous_rejected_text": "The current channel header contains a unit-related attribute; the concrete unit string itself is not written out.",
    "actual_comparator_mismatch": {
      "evidence_stratum": {
        "expected": "S-DOC",
        "actual": "S-FILE"
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
    "previous_rejected_text": "header: voltage_complete=gap_flag_column",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  },
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
    "previous_rejected_text": "legend: current sampling = event_driven(delta_voltage)",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
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
    "previous_rejected_text": "header: state_via=current_sign",
    "actual_comparator_mismatch": {
      "exclusive_assertion": {
        "expected": true,
        "actual": false
      }
    }
  }
]
```

