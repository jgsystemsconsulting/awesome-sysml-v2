# ARL triage log: 2026-09-16-pr-lint-gate-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| AC2 grep check self-contradiction (spec.md:L186) | R1 | R1 | Genuine | Unscoped grep from root hits unpinned commands quoted in docs/superpowers/ records, so the criterion fails as written |
| Add --exclude-dir=.git to AC2 grep (spec.md:L186) | R1 | R1 | Advisory-skipped | grep -r does not match files under .git for this pattern in practice; adding the flag bloats the check |
| Line-number anchoring across two lint.yml edits (spec.md:L56-121) | R1 | R1 | Advisory-skipped | Anchor edits to step order or content, not line numbers; minor clarity gain, not blocking |
| Goal 4 overstates markdownlint CI-action vs local npx parity (spec.md:L22) | R1 | R1 | Design | Divergence between CI action and local pinned npx invocation is intentional; goal text stays as written |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| AC2 grep contradicts its docs/superpowers/ exemption | saboteur | MAJ | Genuine | Fixed (Round 1): scoped outside docs/ + .git |
| grep traverses .git | saboteur | ADV | Advisory-skipped | Fixed with same edit (--exclude-dir=.git) (Round 1) |
| Line-number anchoring across two lint.yml edits | new_hire | ADV | Advisory-skipped | Fixed as cheap advisory: HEAD-baseline note in Design (Round 1) |
| Goal 4 overstates markdownlint invariant | auditor | ADV | Advisory-skipped | Fixed as cheap advisory: narrowed to awesome-lint (Round 1) |

Fixes applied: 4 (1 genuine MAJOR, 3 cheap advisories)
Inflation rate: n/a (0 additional CRITICAL+MAJOR; the sole MAJOR was Genuine and fixed)
Validation: SKIP (no associated script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (AC2 grep scoping, HEAD-baseline note, goal-4 narrowing) | saboteur (+consolidated nh/aud) | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 4
Document is ready.
