# FCL triage log: 2026-09-17-models-and-case-studies

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 AC3 grep -c "example models" returns 4 | R1 | R1 | Genuine | README has 2 lowercase hits pre-edit (tagline+SYSMOD); Masterclass/Book capitalize. AC3 would fail correct implement. Fixed: count 2, SYSMOD+PLEML only. |
| M1 Normative 11 allows lowercase on Masterclass/Book | R1 | R1 | Genuine | Those lines use "Example models". Fixed casing rules. |
| M2 Approach groups four lines under lowercase token | R1 | R1 | Genuine | Same casing mismatch. Fixed Approach text. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| AC3 count 4 | skeptic | CRIT | Genuine | Fixed (Round 1) |
| Normative 11 casing | skeptic | MAJ | Genuine | Fixed (Round 1) |
| Approach casing | skeptic | MAJ | Genuine | Fixed (Round 1) |

Fixes applied: 3
Inflation rate: 0% (0/3 CRITICAL+MAJOR triaged FP/Design/Recurring)
Validation: SKIP

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| AC3 casing/count | skeptic, source, correspondent | CRIT | resolved by this change | Confirmed (Round 2) |
| Normative 11 casing | skeptic, source, correspondent | MAJ | resolved by this change | Confirmed (Round 2) |
| Approach casing | skeptic, source, correspondent | MAJ | resolved by this change | Confirmed (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 3
Document is ready.
