# FCL triage log: 2026-09-16-pr-lint-gate-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| M1: v2.2.2 spell-check FP-fix example named without an inline citation (spec.md:L174) | R1 | R1 | Genuine | Claim is sourced in the research companion's Sources table (release URL v2.2.2, quote "Fix false-positives in spell-check rule"); the spec line must cite it or point at the research doc |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| v2.2.2 FP-fix example uncited | source | MAJ | Genuine | Fixed (Round 1): cited research companion source URL |

Fixes applied: 1
Inflation rate: 0% (0 of 1 CRITICAL+MAJOR findings triaged FP/Recurring/Design)
Validation: SKIP (no associated script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| L174 citation fix (confirmation wave) | source, skeptic, correspondent | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 1
Document is ready.
