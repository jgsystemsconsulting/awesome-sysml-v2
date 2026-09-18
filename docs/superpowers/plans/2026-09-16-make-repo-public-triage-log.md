# ARL triage log: plan 2026-09-16-make-repo-public

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| 403-body routing discarded (Task 3 Step 1) | R1 | R1 | Genuine | Step 1 sends body to /dev/null so the rate-limit routing rule has no body to read; promoted CRITICAL by 2 lenses |
| Step 4 unset PRE_DESC/PRE_TOPICS on rate-limit route | R1 | R1 | Genuine | Variables set in Step 2 are unset when Step 1 returns 403 and Step 4 runs first; promoted CRITICAL by 2 lenses |
| Run-report writer unnamed | R1 | R1 | Genuine | Plan never names the run report file path or which role appends, so Tasks 2-4 cannot reliably read back Task 1 artifacts |
| AC1 evidence rule false-FAILs sanctioned fallback | R1 | R1 | Genuine | Task 4 Step 1 requires anonymous payload proof, but the spec-sanctioned fallback proves anonymity via HTML 200 and fields via authenticated call |
| -f vs -F flip/rollback asymmetry | R1 | R1 | Genuine | Fallback flip uses -f (string) while rollback uses -F (typed boolean); same field should use the same form on both paths |
| PRE_DESC quote-escaping in shell variable paste | R1 | R1 | Advisory-skipped | Real edge; one-line note to single-quote and escape embedded quotes is enough if touched |
| Task 2 flag_path read-back not stated | R1 | R1 | Advisory-skipped | Task 2 assumes flag_path is available but the read-back line is implied by the run report convention; cheap one-line fix |
| Task 1 Interfaces overstates what later tasks consume | R1 | R1 | Advisory-skipped | Only PRE_DESC, PRE_TOPICS, HEAD, flag_path subsets are consumed per task; wording trim, non-blocking |
| AC4 stray-file rule relies on exact `?? docs/` line | R1 | R1 | Advisory-skipped | Any new untracked file would be flagged by prose comparison only; acceptable for a settings run |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| 403-body routing: Step 1 discards body it must classify | saboteur, new_hire | CRITICAL (promoted) | Genuine | Fixed (Round 1): body captured to file, rate-limit grep routes |
| Step 4 consumes vars only set in Step 2 (route skips Step 2) | saboteur, new_hire | CRITICAL (promoted) | Genuine | Fixed (Round 1): Step 4 self-contained, re-derives captures |
| Run report: two writers, no path | auditor (+new_hire path note) | MAJ | Genuine | Fixed (Round 1): path named, parent creates, executor appends |
| AC1 evidence false-FAIL on sanctioned fallback | auditor | MAJ | Genuine | Fixed (Round 1): fallback pair accepted |
| -f vs -F typed-boolean asymmetry | saboteur, auditor | MAJ | Genuine | Fixed (Round 1): -F with rationale |
| PRE_DESC paste escaping; Task 2 flag_path read-back; Task 1 interfaces overstatement; AC4 stray-file rule; 403 re-run note | saboteur, new_hire, auditor | ADV | Genuine/Advisory-skipped | Fixed as cheap advisories (Round 1) |

Fixes applied: 5 families (2 promoted CRITICAL, 3 MAJOR) + 5 advisory items
Inflation rate: 0% (0 findings triaged FP/Design)
Validation: SKIP (checks run at execution)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed families (403 capture, Step 4 self-contained, run-report path, AC1 fallback, -F, advisories) | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |
| Residual: api_body.json scratch vs AC4 sweep | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: delete-before-Task-4 note (Round 2) |

Fixes applied: 1 (advisory)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (checks run at execution)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 6
Document is ready.

## Amendment 1 (spec-side, mirrored)

The spec's secret-scan was amended (Amendment 1) to exclude `${{ secrets.` reference lines; the plan's Task 1 Step 4 command mirrors the spec verbatim. Plan unblocked: Task 1 Step 4 rerun with the amended command, then Tasks 2-4 proceed.
