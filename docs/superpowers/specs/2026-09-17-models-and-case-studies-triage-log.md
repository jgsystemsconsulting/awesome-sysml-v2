# ARL triage log: 2026-09-17-models-and-case-studies

Note: arl-saboteur and arl-auditor primary types failed model-not-found; GP fallback used (log: ARL type missing, GP fallback, same-model). arl-new-hire native succeeded.

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 Runbook SHOULD vs In-scope/AC13 MUST | R1 | R1 | Genuine | Severity mismatch. Fixed: req 13 MUST. |
| C2 Relative README.md# href vs live absolute blob URL | R1 | R1 | Genuine | Pages would 404 on relative. Fixed full absolute href in Exact edits + AC10. |
| M1 Approach three surfaces omit CHANGELOG | R1 | R1 | Genuine | Fixed four surfaces including CHANGELOG and runbook. |
| M2 Exact-string Before was fragment only | R1 | R1 | Genuine | Fixed full live href Before/After. |
| M3 Global substitution scope undefined | R1 | R1 | Genuine | Fixed: only Exact-edits cells; no whole-file README replace. |
| Auditor: AC miss positive descriptor substrings | R1 | R1 | Genuine | Added AC15 positive substring checks. |
| Auditor: AC11 not exact CHANGELOG strings | R1 | R1 | Genuine | AC11 now requires exact bullets. |
| NH A1 href abbreviated | R1 | R1 | Genuine | Same as C2/M2; fixed. |
| NH A2 base branch unnamed | R1 | R1 | Genuine | AC12 names origin/main or PR base. |
| A1 insert after line 82 | R1 | R1 | Advisory-skipped | Fixed cheaply: neighbor-keyed insert. |
| A2 Req11 already vs new PLEML | R1 | R1 | Advisory-skipped | Fixed cheaply: including new PLEML line. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Runbook SHOULD vs MUST | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| Absolute href | saboteur, new_hire, auditor | CRIT | Genuine | Fixed (Round 1) |
| Approach four surfaces | saboteur | MAJ | Genuine | Fixed (Round 1) |
| Exact href strings | saboteur | MAJ | Genuine | Fixed (Round 1) |
| Substitution scope | saboteur | MAJ | Genuine | Fixed (Round 1) |
| Positive descriptor ACs | auditor | MAJ | Genuine | Fixed (Round 1) |
| Exact CHANGELOG AC | auditor | MAJ | Genuine | Fixed (Round 1) |
| base branch named | new_hire | ADV | Genuine | Fixed (Round 1) |

Fixes applied: 8
Inflation rate: 0%
Validation: SKIP

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Approach four surfaces | saboteur, new_hire, auditor | MAJ | resolved by this change | Confirmed (Round 2) |
| Absolute href | saboteur, new_hire, auditor | CRIT | resolved by this change | Confirmed (Round 2) |
| Req 10-13 MUST/scope | saboteur, new_hire, auditor | CRIT/MAJ | resolved by this change | Confirmed (Round 2) |
| AC10-15 | saboteur, new_hire, auditor | MAJ | resolved by this change | Confirmed (Round 2) |
| PLEML neighbor insert | saboteur | ADV | resolved by this change | Confirmed (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 8
Document is ready.
