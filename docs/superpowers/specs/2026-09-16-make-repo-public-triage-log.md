# ARL triage log: 2026-09-16-make-repo-public

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Topics shape mismatch: pre-flip gh `repositoryTopics` objects vs post-flip REST `topics` strings, literal equality unevaluable (L63-95, L66, L95, L119) | R1 | R1 | Genuine | Promoted MAJOR to CRITICAL, 2 lenses (new_hire M1 + auditor M1); comparison of mismatched shapes cannot be evaluated |
| Secret-scan gate unevaluable: prose-only, no recorded artifact or baseline SHA or scan command, ACs pass if skipped (L58-70, L68-69, L74) | R1 | R1 | Genuine | Merged new_hire M2 + auditor M3 + saboteur A1/A3; no artifact makes the gate unfalsifiable |
| Anonymity check single point of failure: api.github.com curl blocked or rate-limited leaves no fallback (L88-95, L118) | R1 | R1 | Genuine | Merged auditor M2 + saboteur A2 rate-limit note; single network dependency can void the check |
| isPrivate==false branch does not distinguish never-private from already-flipped repos (auditor A1) | R1 | R1 | Advisory-skipped | Cheap clarification if added in one line; otherwise skip |
| Workflow name "Freshness report" vs "freshness" match rule ambiguous (new_hire A1) | R1 | R1 | Advisory-skipped | One-line match rule fix; skip if it bloats |
| AC4 scope unclear vs docs/superpowers process artifacts (auditor A3) | R1 | R1 | Advisory-skipped | Clarity improvement only, non-blocking |
| a-09 citation path folds into secret-scan fix (auditor A2) | R1 | R1 | Advisory-skipped | Covered by M1 fix row; no separate change needed |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Topics shape mismatch (gh objects vs REST strings), literal equality unevaluable | new_hire, auditor | CRITICAL (promoted) | Genuine | Fixed (Round 1): sorted name-string normalization both sides |
| Secret-scan gate prose-only, no artifact/baseline/command | new_hire, auditor (+saboteur advisories) | MAJ | Genuine | Fixed (Round 1): baseline af07711, named grep command, recorded artifact required |
| Anonymity proof single-point (api.github.com curl) | auditor (+saboteur rate-limit note) | MAJ | Genuine | Fixed (Round 1): HTML fallback + rate-limit note |
| isPrivate==false branch ambiguity | auditor, saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: discrimination rule (Round 1) |
| Workflow name matching (freshness vs Freshness report) | new_hire | ADV | Advisory-skipped | Fixed as cheap advisory: exact names (Round 1) |
| AC4 scope vs process artifacts | auditor | ADV | Advisory-skipped | Fixed as cheap advisory: exemption stated (Round 1) |
| a-09 citation path | auditor | ADV | Advisory-skipped | Merged into secret-scan fix (Round 1) |

Fixes applied: 6 (3 genuine CRITICAL/MAJOR families, 4 advisory items folded)
Inflation rate: 0% (0 CRITICAL+MAJOR triaged FP/Design)
Validation: SKIP (checks run at execution)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed families (topics normalization, recorded secret-scan gate, anonymity fallback, advisories) | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |
| Residual advisory: delta-commit prose wording | saboteur | ADV | Advisory-skipped | Execution-time git log is the recorded authority; prose count verified accurate (contributing.md exists, lowercase) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (checks run at execution)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 6
Document is ready.

## Amendment 1 (in progress)

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Secret-scan gate unsatisfiable as written: bare `secret` pattern matches the standard `${{ secrets.GITHUB_TOKEN }}` Actions idiom, blocking every run | EXEC 2026-09-16 | A1 2026-09-16 | Genuine | The scan's bare `secret` term hit six workflow lines that reference (not leak) the built-in token; executor correctly blocked per the no-triage rule |

Why: the gate as written is a logical impossibility for this repo (any Actions repo trips it). Amendment narrows the scan to credential shapes and excludes `${{ secrets.` reference lines, preserving the gate's intent (no leaked credential values).

Why-line evidence: executor run report af07711..HEAD scan produced 6 hits, all `${{ secrets.GITHUB_TOKEN }}`.

Confirmation wave (Amendment 1): three lenses confirm the amended scan (reference lines excluded; credential shapes still caught; plan/spec identical). Residual line-granular exclusion noted in the spec text as an accepted residual.

## Amendment 1

Applied 2026-09-16.

## Converged: Round 2 (amended)

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2 (+1 amendment with confirmation)  |  Total fixes: 7
Document is ready.
