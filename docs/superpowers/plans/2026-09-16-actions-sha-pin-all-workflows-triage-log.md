# ARL triage log: plan 2026-09-16-actions-sha-pin-all-workflows

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 off-by-one insert count (+7 asserted, +6 actual) | R1 | R1 | Genuine | Parent-verified arithmetic: 6 comment lines per file with blank line preserved makes 22/25/32, 19/22/28, numstat 9/3, 9/3, 7/1, 18 insertions |
| M1 baseline HEAD asserted but never re-verified | R1 | R1 | Genuine | Intervening commits silently shift every line-number expectation; a git rev-parse check in Task 1 Step 1 is the missing enforcement actor |
| A1 no rate-limit note for unauthenticated GitHub API diagnosis | R1 | R1 | Advisory-skipped | Diagnostic text only; jq null already signals failure to a careful executor |
| A2 zero-match greps exit nonzero without guards | R1 | R1 | Genuine | Unguarded expected-zero greps abort the verification script with set -e style failure; || echo OK is cheap and clearly correct |
| A3 stop path cites undefined in-plan "spec Risk 3" | R1 | R1 | Advisory-skipped | Dangling pointer in a stop-path note; inline rewrite is optional polish |
| A4 no expected output for "12 months ago" boundary grep | R1 | R1 | Genuine | Verification grep lacks an expected value; corrected fact is one hit at post-insert line 28, not auditor's 29/31 two hits |
| A5 "first-step" wording wrong for setup-node | R1 | R1 | Advisory-skipped | Wording nit; both dash-form steps are already enumerated in the task |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Off-by-one insert count: +7 asserted, +6 actual (all line numbers, numstat, insertion totals) | saboteur, new_hire | CRITICAL | Genuine | Fixed (Round 1) |
| Baseline HEAD never re-verified | saboteur, new_hire | MAJ (promoted) | Genuine | Fixed (Round 1) |
| Zero-match greps unguarded | saboteur | ADV | Genuine | Fixed (Round 1) |
| No expected output for stale "12 months ago" grep | auditor | ADV | Genuine | Fixed (Round 1, corrected value: one hit at line 28) |
| No rate-limit note for unauthenticated API gate | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory (Round 1) |
| "spec Risk 3" dangling pointer | new_hire | ADV | Advisory-skipped | Fixed as cheap advisory (Round 1) |
| "first-step" wording for setup-node | auditor | ADV | Advisory-skipped | Fixed as cheap advisory (Round 1) |

Fixes applied: 7 (2 genuine CRITICAL/MAJOR, 2 genuine advisory, 3 cheap advisories)
Inflation rate: 0% (0 of 7 findings triaged FP/Recurring/Design)
Validation: SKIP (no associated script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (confirmation wave: constraints +6, HEAD gate, Tasks 2-4 expectations, Task 5 numstat/12-months, stop path) | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |
| Task 5 permissions grep unguarded (residual) | auditor | ADV | Advisory-skipped | Fixed as cheap advisory (Round 2) |

Fixes applied: 1 (advisory-grade)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 8
Document is ready.
