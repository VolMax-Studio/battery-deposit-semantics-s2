# F4 RATIFICATION WORDING CORRECTION 001

**F4 ratification commit:** `10fab281ffe89a4823364eb90245045d79a36919`

The ratified `F4_ROLE_STAFFING_RECORD.md` states operationally:

- `F4_STATUS = RATIFIED ON OPERATOR COMMIT`
- `F5_BANK_AUTHORING = AUTHORIZED ON OPERATOR COMMIT`
- F5 may begin only after the record is committed to `main`
- operator ratification occurs by committing the record to `main`

Two later sentences use the word `merge` rather than `commit`.

This is an editorial carry-over only.

For this instance those sentences are interpreted as:

`Commit to main is the ratification act.`

and

`F4_STATUS = RATIFIED and F5_BANK_AUTHORING = AUTHORIZED take effect on the Operator's commit to main.`

No role assignment, K5 determination, F4 decision, threshold, execution rule, or protected-input boundary is changed.

**Status:** CORRECTED APPEND-ONLY.
