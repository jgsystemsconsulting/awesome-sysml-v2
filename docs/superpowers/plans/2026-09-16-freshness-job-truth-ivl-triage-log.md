# IVL triage log: plan 2026-09-16-freshness-job-truth

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|

## Check commands

- git show 695dd1b --numstat (expect stale.yml only, 9 5)
- grep -nE "12 months|12-month" .github/workflows/stale.yml (expect no matches)
- grep -cE "24 months|24-month" stale.yml (expect 3)
- python yaml.safe_load stale.yml (expect exit 0)
- bash -n on extracted run block; arithmetic one-liner

## Baseline

- numstat: 9 5 stale.yml, only file in commit
- window greps: no 12-month strings; 3x 24-month
- yaml safe_load: OK (reviewer and task-3 report both ran it)
- stub harness (task 3): mixed scan exit 0 with skip note count 2 last; all-skip footer+skip note last

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| (none — all three lenses clean with checks_run evidence) | behavior, regression, contract | - | - | - |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: PASS
Commands: numstat -> 9 5 stale.yml only; 12-month greps -> none; 24-month count -> 3; yaml -> OK; stub scans -> exit 0

## Converged: Round 1

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 1  |  Total fixes: 0
Implementation verification ready.
