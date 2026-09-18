# ARL triage log: 2026-09-16-freshness-job-truth

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| A1 G1 "always finishes" vs step-2 gh abort (spec.md:L25) | R1 | R1 | Genuine | Wording overstates guarantee; scope G1 to fetch failures |
| A2 footer after skip note reads as clean bill when found=0 (spec.md:L162-L167) | R1 | R1 | Advisory-skipped | Presentation ordering only; fix if cheap, not blocking |
| A3 stale.yml line ref 13-16 should be 14-16 (spec.md:L43) | R1 | R1 | Advisory-skipped | Off-by-one citation; one-line fix, apply if touching spec anyway |
| A4 skip note vacuous when skipped>0 and found=0 (spec.md:L103) | R1 | R1 | FP | Duplicate of A2 condition; same state, one fix covers both |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| G1 "always finishes" overstates (step-2 gh failure fatal) | saboteur | ADV | Genuine | Fixed (Round 1): scoped to fetch failures |
| Skip note before footer reads as clean bill | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: note moved last (Round 1) |
| Permissions cited :13-16, actual :14-16 | auditor | ADV | Advisory-skipped | Fixed as cheap advisory (Round 1) |
| Skip note vacuous when found=0 | auditor | ADV | FP | Covered by A2/A4 consolidated reword (Round 1) |

Fixes applied: 4 (1 genuine advisory-grade, 3 cheap advisories)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: no-unfixed-genuine. Round 1 fixes applied; no CRITICAL/MAJOR remains; advisory-grade fixes all landed.
Total rounds: 1  |  Total fixes: 4
Document is ready.
