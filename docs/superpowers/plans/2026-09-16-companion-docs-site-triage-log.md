# ARL triage log: plan 2026-09-16-companion-docs-site

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Wrap-count gate expects 1, mandated site.css yields 3 (`.wrap{`, `.masthead .wrap{`, `nav.site .wrap{`) at L387 and L324-326 | R1 | R1 | Genuine | Expect-1 count contradicts the mandated CSS, so the Task 4 gate deadlocks on a correct build |
| No-counts regex `[0-9]+ (entries|tools|...)` matches mandated HTML ("v2 resources" x4, "v1 models" x1) at L396 | R1 | R1 | Genuine | Regex is unanchored, so section headings match and the expect-0 check fails on the plan's own required text |
| "Roughly 115" line-count spot-check vs 118-line transcription at L237 | R1 | R1 | Advisory-skipped | "Roughly" already tolerates 118; tightening the number is cheap but adds nothing |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| .wrap{ count expects 1, mandated CSS has 3 matching lines | auditor | CRITICAL | Genuine | Fixed (Round 1): anchored ^\.wrap{ count in Task 3 + Task 4 |
| No-counts regex matches mandated "v2 resources"/"v1 models" phrases | auditor, saboteur | CRITICAL (promoted) | Genuine | Fixed (Round 1): negative-lookbehind-style [^v0-9] prefix |
| "roughly 115 lines" soft expectation vs 118-line transcription | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: exact 118 (Round 1) |

Fixes applied: 3 (2 genuine CRITICAL families, 1 advisory)
Inflation rate: 0% (0 findings triaged FP/Design)
Validation: SKIP (battery runs at execute)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed checks (anchored .wrap, no-counts regex, wc 118) — simulation-verified | saboteur, auditor | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (battery runs at execute)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 3
Document is ready.
