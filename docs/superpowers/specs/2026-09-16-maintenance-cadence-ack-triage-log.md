# ARL triage log: 2026-09-16-maintenance-cadence-ack

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| L50 lint text says awesome-lint and markdownlint both cover README.md and contributing.md | R1 | R1 | Genuine | awesome-lint runs on README.md only; markdownlint-cli2 covers both. Verbatim pinned text must state per-tool scope, AC 1 bar |
| L42 says links.yml checks every link in README.md | R1 | R1 | Genuine | lychee gets no file operand; action defaults scan ./**/*.md, .html, .rst tree-wide. Pinned text understates scope |
| workflow_dispatch trigger omitted from section text | R1 | R1 | Advisory-skipped | Minor omission; skip unless folded free into M2 fix, else bloats verbatim block |
| PR branches:[main] filter flattened in link-scan description | R1 | R1 | Advisory-skipped | Correct but low-value detail for a cadence summary; adding it lengthens pinned text |
| AC 1d should state per-tool lint scope | R1 | R1 | Advisory-skipped | Real clarity gain but subsumed by M1 fix to L50; fix M1 and AC 1d follows |
| Non-goal wording "No README entry content changes" ambiguous against README one-liner rewrite | R1 | R1 | Advisory-skipped | Wording could be tightened to "no README list entry changes"; non-blocking, one-word edit if cheap |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Lint file-scope conflation (awesome-lint is README-only) | auditor | MAJ | Genuine | Fixed (Round 1): per-tool scope in section text and AC 1d |
| Link-scan scope claim unsupported (bare lychee scans tree-wide defaults) | auditor | MAJ | Genuine | Fixed (Round 1): md/html/rst tree-wide wording |
| workflow_dispatch omitted from cadence text | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: "and on manual dispatch" (Round 1) |
| PR branches:[main] filter flattened | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: "targeting main" (Round 1) |
| Non-goal "README entry content" ambiguous | auditor | ADV | Advisory-skipped | Fixed as cheap advisory: awesome-list entry clarification (Round 1) |

Fixes applied: 5 (2 genuine MAJOR, 3 cheap advisories)
Inflation rate: 0% (0 of 2 CRITICAL+MAJOR triaged FP/Design)
Validation: SKIP (docs-only; markdownlint runs at execute)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (link-scan scope, lint per-tool scope, AC 1d, non-goal) | saboteur, auditor | - | Confirmed | Resolved by this change (Round 2) |
| Residual: freshness sentence omits manual dispatch | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory (Round 2) |

Fixes applied: 1 (advisory)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (docs-only; markdownlint runs at execute)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 6
Document is ready.
