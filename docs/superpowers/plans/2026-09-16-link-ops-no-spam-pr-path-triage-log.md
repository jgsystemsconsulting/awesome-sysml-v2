# ARL triage log: plan 2026-09-16-link-ops-no-spam-pr-path

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| names[0] assertion expects bare SHA; yaml.safe_load returns full uses string, assert fails on correct file (saboteur+new_hire+auditor, plan.md:L403-407) | R1 | R1 | Genuine | Parent-verified: names[0] is `actions/checkout@11d5...`, never bare SHA |
| bash -n fails on raw run block: `${{ steps.lychee.outputs.exit_code }}` in double quotes is bad substitution at parse time (saboteur, plan.md:L410-414) | R1 | R1 | Genuine | Harness must strip GitHub expressions before bash -n; plan lacks that step |
| `--max-retries` args line cited as 27 but sits at 28 after inserting `pull_request:` at line 13 (auditor+new_hire, plan.md:L208,L392) | R1 | R1 | Genuine | Parent-verified line shift 27 to 28; sed/patch by line number misses target |
| grep -c prints 0 before OK; "last grep" wording ambiguous (saboteur+new_hire, plan.md:L388-392) | R1 | R1 | Advisory-skipped | Cosmetic output ordering and wording; fix cheap if touching block anyway |
| AC8 fail:false acceptance not mechanically checked (auditor, plan.md:L376) | R1 | R1 | Advisory-skipped | Acceptance criterion lacks a check command; add only if a one-line check suffices |
| links.yml content-line count 37 vs 36 stated (auditor, plan.md:L28) | R1 | R1 | Advisory-skipped | Off-by-one in stated count; harmless once line numbers are re-derived after fixes |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Task 4 Step 3 names assert compares bare SHA vs full uses string | saboteur, new_hire, auditor | CRITICAL | Genuine | Fixed (Round 1): full uses string expected |
| bash -n fails on ${{ }} in raw advisory run block | saboteur | MAJ | Genuine | Fixed (Round 1): re.sub strips GitHub expressions before bash -n |
| --max-retries expected line 27 vs actual 28 post-insert | auditor, new_hire | MAJ (promoted) | Genuine | Fixed (Round 1): line 28 |
| grep -c prints 0 before OK fallback | saboteur, new_hire | ADV | Genuine | Fixed (Round 1): expected output described |
| AC8 fail:false not mechanically checked | auditor | ADV | Genuine | Fixed as cheap advisory: grep added (Round 1) |
| links.yml 37 vs 36 content lines | auditor | ADV | Advisory-skipped | Fixed as cheap advisory (Round 1) |

Fixes applied: 6 (3 genuine CRITICAL/MAJOR, 3 genuine/cheap advisories)
Inflation rate: 0% (0 of 3 CRITICAL+MAJOR findings triaged FP/Recurring/Design)
Validation: SKIP (verification battery itself runs at execute time)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (names assert, ${{ }} strip, line 28, advisories) | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 6
Document is ready.
