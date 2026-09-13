# F6 Bank Integrity Closure Record

Instance: battery-deposit-semantics-s2
Stage: F6 role-aware back-translation
Status: PASS

Attempt 01:
- target entries: 330
- exact full matches: 293
- rejected attempts: 37

Attempt 02:
- target entries: 37
- exact full matches: 21
- rejected attempts: 16

Attempt 03:
- target entries: 16
- exact full matches: 16
- rejected attempts: 0

Final retained bank:
- 330 / 330 entries validated
- cumulative R_total = 53
- R_total ceiling = 99
- no slot incurred a third rejection

Final bank:
F5_BANK_ATTEMPT_03.jsonl
SHA256: 22fa12f14cbd0fda08293fd7c7886b7793d80bf7ec9dfa9cf2330e3b26e62859

Round-03 blind input SHA256:
2498f0fbb0084ff0579d53aae3e45fa7362ceebeb418ed23c7a3fdf7c235b017

Round-03 response SHA256:
cb6c238667c0a750922894fc52d60e1d557dae91a485777e99d300956b9ef472

Party 2:
GROK-CLEAN-P2-01

Party 3:
GROQ-CLEAN-P3-01
qwen/qwen3.8-27b

Recorded Party-3 execution runners did not load the F6 private-key
files. Party 3 received blind entry text plus frozen interrogatives,
answer vocabulary, strata definitions and scope vocabulary only.

F6_BANK_INTEGRITY = ESTABLISHED
NEXT_STAGE = F7
