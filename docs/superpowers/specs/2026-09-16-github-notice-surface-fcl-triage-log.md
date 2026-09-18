# FCL triage log: 2026-09-16-github-notice-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1: PR title contains forbidden word Awesome | R1 | R1 | Genuine | pull_request_template.md bad example "Add Awesome Swift"; PR titled with Awesome is declined on sight, blocking submission. Fix: PR title becomes `Add SysML V2`; Contents entry name stays. |
| M1: banner quote incomplete | R1 | R1 | Genuine | Quote is truncated, so the notice surface misstates the source text. Fix: complete the banner quote. |
| M2: review-4-PRs and unicorn attributed to wrong doc | R1 | R1 | Genuine | Both rules come from pull_request_template.md, not create-list.md. Fix: attribute them to pull_request_template.md; keep create-list.md for 30-day age and duplicate search. |
| A1: #4093 quote truncated while marked verbatim | R1 | R1 | Genuine | Label "verbatim" contradicts the truncation. Fix: extend the quote or drop the word "verbatim". |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| PR title contains forbidden word Awesome (upstream bad example: Add Awesome Swift) | skeptic | CRIT | Genuine | Fixed (Round 1): title `Add SysML V2`; Contents entry name unchanged |
| Banner quote incomplete (omits "with the existing ones") | skeptic | MAJ | Genuine | Fixed (Round 1) |
| review-4-PRs + unicorn mis-attributed to create-list.md | skeptic | MAJ | Genuine | Fixed (Round 1): attributed to pull_request_template.md |
| #4093 Claude quote truncated | skeptic | ADV | Genuine | Fixed as cheap advisory: full span quoted (Round 1) |

Fixes applied: 4 (1 genuine CRITICAL, 2 genuine MAJOR, 1 advisory)
Inflation rate: 0% (0 of 3 CRITICAL+MAJOR triaged FP)
Validation: SKIP (docs-only)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (PR title, banner quote, attribution, #4093 span) — confirmed against primaries | skeptic, source | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (docs-only)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 4
Document is ready.
