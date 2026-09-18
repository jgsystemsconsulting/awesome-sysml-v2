# ARL triage log: plan 2026-09-17-models-and-case-studies

Note: saboteur/auditor used GP fallback where primary pins failed earlier in session; new_hire native.

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 Task 5 omits AC10/AC15 | R1 | R1 | Genuine | Fixed: final sweep includes full category row and three positive descriptor greps. |
| C2 zero-match greps exit 1 under set -e | R1 | R1 | Genuine | Fixed: count wrappers `\|\| true` + Global Constraints note. |
| M1 Task 5 drops AC6 exactness | R1 | R1 | Genuine | Fixed: exact PLEML line + neighbor greps in Task 5. |
| M2 Task 5 drops runbook line-10 keep | R1 | R1 | Genuine | Fixed: residual `example models` count == 1 on runbook. |
| M3 Task 4 false Task1 CHANGELOG consume | R1 | R1 | Genuine | Fixed: Codebase context re-confirm wording. |
| M4 README numstat/CRLF | R1 | R1 | Design | Keep numstat as shape check; EOL already noted for index; README CRLF is baseline. |
| M5 TOC/H3 final gate | R1 | R1 | Genuine | Fixed: TOC exact line + H3 empty awk in Task 5. |
| NH/Auditor advisories | R1 | R1 | Advisory-skipped | Covered by C1/C2/M3 fixes or leave-alone ops nits. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Task 5 AC10/15 | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| set -e greps | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| AC6 exact | saboteur | MAJ | Genuine | Fixed (Round 1) |
| runbook L10 | saboteur | MAJ | Genuine | Fixed (Round 1) |
| Task4 CHANGELOG claim | saboteur, auditor, new_hire | MAJ | Genuine | Fixed (Round 1) |
| TOC/H3 final | saboteur, auditor | MAJ | Genuine | Fixed (Round 1) |
| numstat CRLF | saboteur | MAJ | Design | Wontfix (Round 1) |

Fixes applied: 6
Inflation rate: 14% (1/7)
Validation: SKIP

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Task 5 hardened sweep | parent verify | CRIT/MAJ | resolved by this change | Confirmed strings present in plan |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Parent verified fixed Task 5 sweep and Task 4 interfaces after R1 (confirmation wave simplified: fixes are executable verify commands, greppable in plan).
Total rounds: 2  |  Total fixes: 6
Document is ready.
