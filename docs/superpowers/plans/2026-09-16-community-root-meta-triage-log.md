# ARL triage log: plan 2026-09-16-community-root-meta

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Attribution grep uses grep -qxF on mid-sentence fragment (L294) | R1 | R1 | Genuine | Whole-line match on a fragment fails unconditionally; drop -x for substring match. Saboteur C1 + auditor M1, promoted CRITICAL at 2 lenses |
| Substitution script text mode rewrites LF to CRLF on Windows (L128-136) | R1 | R1 | Genuine | Python text mode newline translation breaks anchored and byte-exact checks; open with newline='\n' or bytes mode |
| Translations tail anchor unpinned | R1 | R1 | Advisory-skipped | Verify anchor against fetched text or loosen; fix only if cheap |
| PyYAML fallback eyeballs AC4 | R1 | R1 | Advisory-skipped | Saboteur A2 + auditor A1; pin a scripted assertion if a one-liner fits, otherwise skip |
| Attribution .html URL diverges from spec outline item 5 | R1 | R1 | Advisory-skipped | Auditor A2; accepted deviation, note it in the plan |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Attribution grep -qxF whole-line on fragment; false-FAIL unconditional | saboteur, auditor | CRITICAL (promoted) | Genuine | Fixed (Round 1): grep -qF substring match |
| Windows python text-mode rewrites LF to CRLF, breaking anchored checks | auditor | MAJ | Genuine | Fixed (Round 1): newline="" on read/write + comment |
| Translations tail anchor unpinned | saboteur | ADV | Advisory-skipped | grep -qF on the URL substring tolerates ref-block variance (Round 1) |
| PyYAML fallback eyeballs AC4 | saboteur, auditor | ADV | Advisory-skipped | Accepted: PyYAML ships with the environment; fallback path is contingency only (Round 1) |
| AC7 text-half mapping + attribution .html URL deviation | auditor | ADV | Advisory-skipped | Noted in Task 3 scope and Task 2 redirect note (Round 1) |

Fixes applied: 2 genuine (1 promoted CRITICAL, 1 MAJOR) + advisory folds
Inflation rate: 0% (0 findings triaged FP/Design)
Validation: SKIP (battery runs at execute)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed checks (substring attribution grep, LF-preserving substitution, advisory folds) — verified | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (battery runs at execute)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 2
Document is ready.
