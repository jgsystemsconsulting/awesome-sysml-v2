# ARL triage log: 2026-09-16-actions-sha-pin-all-workflows

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| M1: L59/L63 claim 5-line block and 18 added lines; verbatim block is 6 lines, true added total 21 | R1 | R1 | Advisory-skipped | Prose count error only; verbatim block at L62-L67 is authoritative, so no wrong code path. Cheap fix: change 5 to 6 and 18 to 21. |
| M2: L49 template shows only dashed `- uses:` form; named-step refs at L82-L83, L90 use bare `uses:` | R1 | R1 | FP | Per-file edits at L76-L91 give exact before/after strings with correct indentation for every ref, so the template shape cannot mislead the implementer. |
| A1: Risk 1 says implementer never re-resolves SHAs; Risk 3 mandates pre-commit commits-API re-check | R1 | R1 | Advisory-skipped | Risk 1 bars re-deriving values, Risk 3 verifies tag immutability; intent is readable. Cheap fix: rephrase Risk 1 as "copies values, never re-derives." |
| A2: L74-L91 per-file line numbers shift once the comment block is inserted | R1 | R1 | Advisory-skipped | Each edit carries a full before/after string, so line numbers are locating aids only. Cheap fix: note edits precede the insert. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Block count prose: 5-line/18 added vs verbatim 6-line/21 | saboteur, auditor | MAJ (promoted) | Advisory-skipped | Fixed as cheap advisory: 6-line/21 (Round 1) |
| Pin template shows only dashed form | new_hire, auditor | MAJ (promoted) | FP | Per-file edit strings authoritative (Round 1) |
| Risk 1 "never re-resolves" vs Risk 3 re-check | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: "never re-derives" (Round 1) |
| Line numbers shift after comment insert | new_hire | ADV | Advisory-skipped | Fixed as cheap advisory: edits-before-insert note (Round 1) |

Fixes applied: 3 (all advisory-grade)
Inflation rate: 25% (1 of 4 findings triaged FP; promoted MAJ M1 downgraded to advisory-skipped)
Validation: SKIP (no associated script)

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: no-unfixed-genuine. Round 1 genuine_fixes_needed was empty; advisory-grade polish applied, no CRITICAL/MAJOR remains.
Total rounds: 1  |  Total fixes: 3
Document is ready.

## Amendment 1 (in progress)

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| "21 added lines" diff count wrong: verbatim blocks keep the existing blank line, so added lines are 18 (6 comment lines x 3 files) | R1 2026-09-16 | A1 2026-09-16 | Genuine | Plan ARL round 1 found the +7 vs +6 off-by-one; the spec's round-1 M1 "fix" to 21 inherited the wrong arithmetic. Corrected to 18 with the blank-line rationale. |

Why: saboteur + new-hire lenses on the P9 plan proved net insert is +6 per file; the spec's diff-total prose is corrected to match. Advisory-grade numeric fix; no confirmation wave required.

## Amendment 1

Applied 2026-09-16.

## Converged: Round 1 (amended)

Track 3: diminishing-return halt. Predicate: no-unfixed-genuine. Amendment applied an advisory-grade numeric correction; no CRITICAL/MAJOR remains.
Total rounds: 1 (+1 amendment)  |  Total fixes: 4
Document is ready.
